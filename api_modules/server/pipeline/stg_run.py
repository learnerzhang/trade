# -*- encoding: UTF-8 -*-
import random
import datetime
import pandas as pd
import numpy as np
from sklearn import metrics
from api_modules.server.utils import stock_utils
from api_modules.server.utils.config import ConfigUtils
from api_modules.server.sequoia.stg import LGB
from api_modules.server.models import get_recently_trade_date, Account
from api_modules.server.apis import user_api
from api_modules.server.apis import account_api

root = ConfigUtils.get_stock("DATA")
model_root = ConfigUtils.get_stock("MODELS")
model_name = 'lgb.pkl'
thresh_hold = 0.6

trn_date_min = '2010-01-01'
trn_date_max = '2020-07-31'

val_date_min = '2020-08-03'
val_date_max = '2020-08-07'

test_date_min = '2020-08-08'
test_date_max = '2020-08-21'

feature_cols = ['close_transform', 'open_transform', 'high_transform', 'low_transform']
trn_col = ['open', 'high', 'low', 'close', 'preclose', 'change', 'volume', 'amount', 'turn', 'ts_code_id'] + feature_cols
label = 'label_final'

class Stg:
    
    def __init__(self):
        """可以考虑加入回测数据
        """
        self.stock_info = pd.read_csv(ConfigUtils.get_stock("STOCKS_DATESET"), encoding='utf-8', low_memory=False)
        print("finish load dataset.")
        self.build()
        

    def build(self):
        self.trn_data_idx = (self.stock_info['date'] >= trn_date_min) & (self.stock_info['date'] <= trn_date_max)
        self.val_data_idx = (self.stock_info['date'] >= val_date_min) & (self.stock_info['date'] <= val_date_max)
        self.test_data_idx = (self.stock_info['date'] >= test_date_min) & (self.stock_info['date'] <= test_date_max)

        self.trn = self.stock_info[self.trn_data_idx][trn_col].values
        self.trn_label = self.stock_info[self.trn_data_idx][label].values

        self.val = self.stock_info[self.val_data_idx][trn_col].values
        self.val_label = self.stock_info[self.val_data_idx][label].values

        self.test = self.stock_info[self.test_data_idx][trn_col].values
        self.test_label = self.stock_info[self.test_data_idx][label].values
    
    def run_lgb_train(self,):
        
        lgb = LGB(self.trn, self.trn_label, self.val, self.val_label, model_name)
        lgb.train()
        print("train over, save model path: {}!".format(lgb.path))

    def predict_stocks(self):
        lgb = LGB(self.trn, self.trn_label, self.val, self.val_label, model_name)
        lgb.load()
        predict_probs = lgb.predict(self.test)
        print('[probs]', predict_probs)
        oof_test_final = predict_probs >= thresh_hold
        test_postive_idx = np.argwhere(np.array(oof_test_final) == 1).reshape(-1)
        test_all_idx = np.argwhere(self.test_data_idx.values).reshape(-1)
        tmp_col = ['code', 'code_name', 'date', 'open', 'high', 'low', 'close', 'preclose', 'change', 'pctChg', 'amount', 'isST', 'label_max', 'label_min', 'label_final']
        tmp_df = self.stock_info[tmp_col].iloc[test_all_idx[test_postive_idx]].reset_index()
        tmp_df['prob'] = [predict_probs[i] for i in test_postive_idx]
        tmp_df = tmp_df[tmp_df.date == test_date_min].sort_values('prob', ascending=False).reset_index()
        return [row.to_dict() for i, row in tmp_df.iterrows() if not stock_utils.is_chuangyeban(row['code']) and 'ST' not in row['code_name']]

    def run_lgb_predict(self,):
        lgb = LGB(self.trn, self.trn_label, self.val, self.val_label, model_name)
        lgb.load()
        predict_labels = lgb.predict(self.test)
        print(len(predict_labels), predict_labels)
        
        oof_test_final = predict_labels >= thresh_hold
        print(metrics.accuracy_score(self.test_label, oof_test_final))
        print(metrics.confusion_matrix(self.test_label, oof_test_final))
        tp = np.sum(((oof_test_final == 1) & (self.test_label == 1)))
        pp = np.sum(oof_test_final == 1)
        print('sensitivity:%.3f' % (tp / (pp)))

        oof_test_final = np.array(oof_test_final)
        test_postive_idx = np.argwhere(oof_test_final == 1).reshape(-1)

        test_all_idx = np.argwhere(self.test_data_idx.values).reshape(-1)
        # 查看选了哪些股票
        tmp_col = ['code', 'code_name', 'date', 'open', 'high', 'low', 'close', 'preclose', 'change', 'pctChg', 'amount', 'isST', 'label_max', 'label_min', 'label_final']
        tmp_df = self.stock_info[tmp_col].iloc[test_all_idx[test_postive_idx]].reset_index()
        tmp_probs = [predict_labels[i] for i in test_postive_idx]
        tmp_df['label_prob'] = tmp_probs
        tmp_df['is_limit_up'] = tmp_df['close'] == tmp_df['high']

        buy_df = tmp_df[(tmp_df['is_limit_up']==False)].reset_index()
        buy_df.drop(['index', 'level_0'], axis=1, inplace=True)
        print(len(buy_df), sum(buy_df['label_final']))

        # 回测
        # 读取指数信息
        # index_df = pd.read_csv(os.path.join(ConfigUtils.get_stock("DATA_DIR"), 'sh.000001_上证综合指数.csv'), encoding='utf-8')
        # tmp_idx = (index_df['date'] >= test_date_min) & (index_df['date'] <= test_date_max)
        # # print(index_df[tmp_idx])
        # index_df = index_df[tmp_idx]
        # index_df = index_df.reset_index()
        # close1 = 0.0
        # close2 = 0.0
        # for i, row in index_df.iterrows():
        #     if i == 0:
        #         close1 = float(row['close'])
        #     if i == len(index_df) - 1:
        #         close2 = float(row['close'])

        # money_init = 100000
        # account = Account(money_init)
        # account.BackTest(buy_df, self.stock_info, index_df)

        # account_profit = (account.market_value - money_init) / money_init
        # index_profit = (close2 - close1) / close1
        # win_rate = account.victory / (account.victory + account.defeat)
        # print('账户盈利情况:%.4f' % account_profit)
        # print('上证指数浮动情况:%.4f' % index_profit)
        # print('交易胜率:%.4f' % win_rate)
        # print('最大回撤率:%.4f' % account.max_retracement)

        # # draw
        # index_value = list(index_df[index_df['date'] == test_date_min]['preclose']) + list(index_df.sort_values('date')['close'])
        # print("length: ", len(account.market_value_all), len(index_value))
        # draw_market_value_change(0, account.market_value_all[1:], index_value)


def train():
    global trn_date_min, trn_date_max, val_date_min, val_date_max, test_date_min, test_date_max, model_name
    trn_date_min = '2020-01-01'
    trn_date_max = '2020-11-09'

    val_date_min = '2020-11-01'
    val_date_max = '2020-11-09'

    test_date_min = '2020-11-09'
    test_date_max = '2020-11-09'

    stg = Stg()
    stg.build()  
    cur_date = datetime.datetime.date(datetime.datetime.strptime(test_date_min, '%Y-%m-%d'))
    while cur_date < datetime.date.today():
        cal_date = get_recently_trade_date(cur_date=cur_date, update_flag=0)[0]
        dt = datetime.datetime.date(cal_date.calendar_date)
        if cur_date == dt:
            model_name = 'lgb_{}.pkl'.format(str(cur_date))
            print('[Train date {}]'.format(dt))
            stg.build()
            stg.run_lgb_train()

        trn_date_min = stock_utils.next_date(trn_date_min)
        trn_date_max = stock_utils.next_date(trn_date_max)
        val_date_min = stock_utils.next_date(val_date_min)
        val_date_max = stock_utils.next_date(val_date_max)
        test_date_min = stock_utils.next_date(test_date_min)
        test_date_max = stock_utils.next_date(test_date_max)
        cur_date = datetime.datetime.date(datetime.datetime.strptime(test_date_min, '%Y-%m-%d'))

def predict():
    global trn_date_min, trn_date_max, val_date_min, val_date_max, test_date_min, test_date_max, model_name
    trn_date_min = '2019-01-01'
    trn_date_max = '2020-11-06'
    
    val_date_min = '2020-11-06'
    val_date_max = '2020-11-06'

    test_date_min = '2020-11-06'
    test_date_max = '2020-11-06'

    stg = Stg()
    stg.build()
    print("[Predict {}]".format(test_date_max))
    model_name = 'lgb_{}.pkl'.format(trn_date_max)
    stocks = stg.predict_stocks()
    for ele in stocks:
        print(ele['code'], ele['code_name'], ele['close'], ele['prob'])


def simulation(rand=False):
    global trn_date_min, trn_date_max, val_date_min, val_date_max, test_date_min, test_date_max, model_name
    
    trn_date_min = '2019-01-01'
    trn_date_max = '2020-07-10'

    val_date_min = '2020-07-20'
    val_date_max = '2020-07-31'

    test_date_min = '2020-08-01'
    test_date_max = '2020-08-01'

    stg = Stg()
    cur_date = datetime.datetime.date(datetime.datetime.strptime(test_date_min, '%Y-%m-%d'))
    while cur_date < datetime.date.today():
        cal_date = get_recently_trade_date(cur_date=cur_date, update_flag=0)[0]
        dt = datetime.datetime.date(cal_date.calendar_date)
        if cur_date == dt:
            print('[Simulation date {}]'.format(dt))
            # s1 train
            stg.build()
            # s2 buy or sell
            # user
            user = user_api.get_user(name='niu_x')
            if user is None:
                raise Exception("No User.")
            model_name = 'lgb_{}.pkl'.format(str(cur_date))
            stocks = stg.predict_stocks()
            if rand:
                random.shuffle(stocks)
            
            flag = 1
            # sell
            accounts = account_api.be_acts({"flag": flag, "sell_date": dt})
            cash = user.cash
            dynamic_profit = 0.0
            for acc in accounts:
                profit = 0.0
                price = stock_utils.get_price(acc.code, acc.code_name, str(dt))
                # print(acc, price)
                if (price - acc.price) * 1.0 / acc.price > 0.07:
                    print('# 止赢卖出 {}/{} 价格：{} {}手, 盈利: {}'.format(acc.code, acc.code_name, price, acc.num, price * acc.num * 100 - acc.amount))
                    acc.sell()
                if (acc.price - price) * 1.0 / acc.price > 0.03:
                    print('# 止损卖出 {}/{} 价格：{} {}手, 亏损: {}'.format(acc.code, acc.code_name, price, acc.num, acc.amount - price * acc.num * 100))
                    acc.sell()
                if acc.flag == 0:
                    # 卖出盈利情况
                    profit = price * acc.num * 100
                    transfer = 0.0
                    if acc.code.startswith('sh'):
                        transfer = int((acc.num * 100 + 999) / 1000)
                    stamp = profit * 0.001
                    brokers = profit * 0.002
                    brokers = brokers if brokers >= 5 else 5
                    profit = profit - brokers - stamp - transfer
                    user.set_cash(cash + profit)

                    user_api.update_user()
                    account_api.update_act()
                else:
                    dynamic_profit += price * acc.num * 100
            
            # buy
            dynamic_buy = 0.0
            for ele in stocks:
                cash = user.cash
                code = ele['code']
                close = ele['close']
                prob = ele['prob']
                code_name = ele['code_name']
                # print("[*]", code, code_name, close, prob)
                if close * 100 + 5000 < user.cash \
                    and len(account_api.be_acts({"flag": 1})) < 4 \
                    and not account_api.be_acts({"code":code, "flag": flag, "date": dt}):
                    buy_num, cost = stock_utils.buy_stock(code, close, code_name, user.cash)
                    if buy_num > 0: # 可买入
                        user.set_cash(cash - cost)
                        dynamic_buy += buy_num * close * 100
                        account_api.add_act(Account(user.id, code, code_name, close, buy_num, cost, flag=flag, date=dt))
                        print(u"[买入{}/{}价格{},{}手]".format(code, code_name, close, buy_num))
            
            # s3 calucate profit
            # 账户 + 持仓 / 回撤
            print("[{}] 账户市值: {}\n".format(dt, user.cash + dynamic_profit + dynamic_buy))

        # results = stg.predict_next_trade()
        # 1. 判断当前是否交易日, 有无持仓
        # 2. 符合买入 卖出标准
        # 3. 更新交易数据
        # 4. 更新时间
        #print('[train: {} - {}, valide: {} - {}, test: {} - {}]'.format(trn_date_min, trn_date_max, val_date_min, val_date_max, test_date_min, test_date_max))
        trn_date_min = stock_utils.next_date(trn_date_min)
        trn_date_max = stock_utils.next_date(trn_date_max)
        val_date_min = stock_utils.next_date(val_date_min)
        val_date_max = stock_utils.next_date(val_date_max)
        test_date_min = stock_utils.next_date(test_date_min)
        test_date_max = stock_utils.next_date(test_date_max)
        cur_date = datetime.datetime.date(datetime.datetime.strptime(test_date_min, '%Y-%m-%d'))


if __name__ == "__main__":
    # simulation(rand=False)
    # train()
    predict()
