# -*- encoding: UTF-8 -*-
import random
import datetime
import pandas as pd
import numpy as np
from sklearn import metrics

from common import stock_utils
from common.config import ConfigUtils
from common.stock_utils import get_recently_trade_date
from strategy_modules.models.lightgbm import LGB

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

history_close_cols = ['close_shift_1', 'close_shift_2', 'close_shift_3', 'close_shift_4', 'close_shift_5', 'close_shift_10', 'close_shift_20', 'close_shift_30',
                      'close_shift_40', 'close_shift_50', 'close_shift_60', 'close_shift_80', 'close_shift_100', 'close_shift_120', 'close_shift_150',
                      'close_shift_180', 'close_shift_200', 'close_shift_250']

history_volume_cols = []
feature_cols = ['close_transform', 'open_transform', 'high_transform', 'low_transform']
trn_col = ['open', 'high', 'low', 'close', 'preclose', 'change', 'volume', 'amount', 'turn',
           'ts_code_id'] + feature_cols + history_close_cols
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

    def run_lgb_train(self, ):
        lgb = LGB(self.trn, self.trn_label, self.val, self.val_label, model_name)
        lgb.train()
        print("train over, save model path: {}!".format(lgb.path))

    def predict_stocks(self):
        lgb = LGB(self.trn, self.trn_label, self.val, self.val_label, model_name)
        lgb.load()
        predict_probs = lgb.predict(self.test)
        result = np.argmax(predict_probs, axis=1)
        print('[probs]', result)
        oof_test_final = result >= 5
        print('[oof]', oof_test_final)
        test_postive_idx = np.argwhere(np.array(oof_test_final) == 1).reshape(-1)
        print('[idx]', test_postive_idx)
        test_all_idx = np.argwhere(self.test_data_idx.values).reshape(-1)
        tmp_col = ['code', 'code_name', 'date', 'open', 'high', 'low', 'close', 'preclose', 'change', 'pctChg',
                   'amount', 'isST', 'label_max', 'label_min', 'label_final']
        tmp_df = self.stock_info[tmp_col].iloc[test_all_idx[test_postive_idx]].reset_index()
        tmp_df['label'] = [result[i] for i in test_postive_idx]
        tmp_df = tmp_df[tmp_df.date == test_date_min].sort_values('label', ascending=False).reset_index()
        return [row.to_dict() for i, row in tmp_df.iterrows()]

    def run_lgb_predict(self, ):
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
        tmp_col = ['code', 'code_name', 'date', 'open', 'high', 'low', 'close', 'preclose', 'change', 'pctChg',
                   'amount', 'isST', 'label_max', 'label_min', 'label_final']
        tmp_df = self.stock_info[tmp_col].iloc[test_all_idx[test_postive_idx]].reset_index()
        tmp_probs = [predict_labels[i] for i in test_postive_idx]
        tmp_df['label_prob'] = tmp_probs
        tmp_df['is_limit_up'] = tmp_df['close'] == tmp_df['high']

        buy_df = tmp_df[(tmp_df['is_limit_up'] == False)].reset_index()
        buy_df.drop(['index', 'level_0'], axis=1, inplace=True)
        print(len(buy_df), sum(buy_df['label_final']))


def train():
    global trn_date_min, trn_date_max, val_date_min, val_date_max, test_date_min, test_date_max, model_name
    trn_date_min = '2019-01-01'
    trn_date_max = '2020-11-17'

    val_date_min = '2020-11-01'
    val_date_max = '2020-11-17'

    test_date_min = '2020-11-17'
    test_date_max = '2020-11-17'

    stg = Stg()
    stg.build()
    cur_date = datetime.datetime.date(datetime.datetime.strptime(test_date_min, '%Y-%m-%d'))
    while cur_date < datetime.date.today():
        cal_date = get_recently_trade_date(cur_date)
        if str(cur_date) == cal_date:
            print("while train date:", cur_date, cal_date)
            model_name = 'lgb_{}.pkl'.format(str(cur_date))
            print('[Train date {}]'.format(cur_date))
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
    trn_date_max = '2020-11-17'
    val_date_min = '2020-11-06'
    val_date_max = '2020-11-17'
    test_date_min = '2020-11-17'
    test_date_max = '2020-11-17'

    stg = Stg()
    stg.build()

    model_name = 'lgb_{}.pkl'.format('2020-11-13')
    print("[Predict {}]".format(model_name))
    stocks = stg.predict_stocks()
    for ele in stocks:
        print(ele['code'], ele['code_name'], ele['close'], ele['label'])


if __name__ == "__main__":
    # simulation(rand=False)
    train()
    # predict()
