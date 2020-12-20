# -*- coding: UTF-8 -*-
from pandas.tseries.offsets import *
from api_modules.server.utils.config import ConfigUtils
import baostock as bs
import pandas as pd
import numpy as np
import tqdm
import datetime
import xlrd
import os

market_map = {'主板':0, '中小板':1}
exchange_map = {'SZSE':0, 'SSE':1}
is_hs_map = {'S':0, 'N':1, 'H':2}
area_map = {'深圳': 0, '北京': 1, '吉林': 2, '江苏': 3, '辽宁': 4, '广东': 5, '安徽': 6, '四川': 7, '浙江': 8,'湖南': 9, '河北': 10, '新疆': 11, '山东': 12, '河南': 13, '山西': 14, '江西': 15, '青海': 16, '湖北': 17, '内蒙': 18, '海南': 19, '重庆': 20, '陕西': 21, '福建': 22, '广西': 23, '天津': 24, '云南': 25, '贵州': 26, '甘肃': 27, '宁夏': 28, '黑龙江': 29, '上海': 30, '西藏': 31}


ONE_HOUR_SECONDS = 60 * 60

# 获取股票代码列表
def get_stocks(config=None):
    if config:
        data = xlrd.open_workbook(config)
        table = data.sheets()[0]
        rows_count = table.nrows
        codes = table.col_values(0)[1:rows_count - 1]
        names = table.col_values(1)[1:rows_count - 1]
        return list(zip(codes, names))
    else:
        data_files = os.listdir(ConfigUtils.get_stock('DATA_DIR'))
        stocks = []
        for file in data_files:
            code_name = file.split(".")[0]
            code = code_name.split("-")[0]
            name = code_name.split("-")[1]
            appender = (code, name)
            stocks.append(appender)
        return stocks


def clean_files():
    for the_file in os.listdir(ConfigUtils.get_stock("DATA_DIR")):
        file_path = os.path.join(ConfigUtils.get_stock("DATA_DIR"), the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


# 读取本地数据文件
def read_data(code_name):
    code = code_name[0]
    name = code_name[1]
    df = None
    file_name = str(code) + '_' + str(name) + '.csv'
    file_path = ConfigUtils.get_stock("DATA_DIR") + "/" + file_name
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError as e:
            df = None
            pass
    if df is not None and not df.empty:
        # print(df.keys())
        df["open"] = df['open'].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)
        df["close"] = df["close"].astype(float)
        df["preclose"] = df["preclose"].astype(float)
        df["volume"] = df["volume"].astype(float)
        df["pctChg"] = df["pctChg"].astype(float)
        return df
    return None


def get_price(code, name, date):

    tmp_df = read_data((code, name))
    tmp_df = tmp_df[tmp_df.date == date]
    if len(tmp_df):
        return float(tmp_df['close'].values[0])
    else:
        return None

def buy_stock(code, price, code_name, money, ):
    
    total_num = int(money /(100 * price))
    buy_num = 0
    if total_num > 6:
        buy_num = int(total_num/3)
    elif total_num > 4:
        buy_num = int(total_num/2)
    elif total_num > 1:
        buy_num = 1
    
    # 股票
    cost = buy_num * 100 * price
    # 过户
    transfer = 0.0
    if code.startswith('sh'):
        transfer = int((buy_num * 100 + 999) / 1000)
    # 佣金
    brokers = cost * 0.002
    brokers = brokers if brokers >= 5 else 5
    return buy_num, cost + transfer + brokers


# 是否是工作日
def is_weekday():
    return datetime.datetime.today().weekday() < 5


def next_weekday(date):
    return pd.to_datetime(date) + BDay()


def next_date(date):
    """下一天"""
    cur_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return (cur_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

def persist(strategy, results):
    if not os.path.exists(ConfigUtils.get_stock("OUTPUT")):
        os.mkdir(ConfigUtils.get_stock("OUTPUT"))

    with open(ConfigUtils.get_stock("OUTPUT") + "/" + strategy + ".txt", 'w') as wf:
        for e in results:
            wf.write(e[0] + "-" + e[1] + "-" + str(e[2]) + '\n')


def prepare():
    dirs = [ConfigUtils.get_stock("DATA_DIR"), ConfigUtils.get_stock("DB_DIR")]
    for dir in dirs:
        if os.path.exists(dir):
            clean_files()
            return
        else:
            os.makedirs(dir)


def is_chuangyeban(code):
    if code:
        return code.split('.')[1].startswith('300') or code.split('.')[1].startswith('688')
    return False


def init_trade_date():
    # 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)

    # 获取交易日信息 ####
    st = ConfigUtils.get_stock("START_DATE")
    et = ConfigUtils.get_stock("END_DATE")
    print(st, et)
    rs = bs.query_trade_dates(start_date=st, end_date=et)
    print('query_trade_dates respond error_code:' + rs.error_code)
    print('query_trade_dates respond  error_msg:' + rs.error_msg)

    # 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    result.to_csv(ConfigUtils.get_stock("STOCKS_DATE"), index=False)
    # 结果集输出到csv文件 ####import ujson
    bs.logout()


def get_recently_trade_date():
    dt = datetime.date.today()
    if os.path.exists(ConfigUtils.get_stock("STOCKS_DATE")):
        trade_dates = pd.read_csv(ConfigUtils.get_stock("STOCKS_DATE"), header=0)
        trade_date_dict = trade_dates.set_index("calendar_date")['is_trading_day'].to_dict()
        tmp_dt = str(dt)
        if tmp_dt in trade_date_dict:
            if trade_date_dict[tmp_dt] == 1:
                return tmp_dt
            else:
                dt_num = 1
                dt_pass = str(dt - datetime.timedelta(days=dt_num))
                while dt_pass in trade_date_dict and trade_date_dict[dt_pass] == 0:
                    dt_num += 1
                    dt_pass = str(dt - datetime.timedelta(days=dt_num))
                if dt_pass in trade_date_dict:
                    return dt_pass
            print("Date Is Not Exist !!!, Reload Trade Dates. ")
    else:
        print("Date Is Not Exist, Reloading Trade Dates. ")
        init_trade_date()
        print("Date Loading Finish. ")
    return None


def gen_dataset():

    start_dt = '2019-01-01'
    date_info = pd.read_csv(ConfigUtils.get_stock("STOCKS_DATE"), encoding='utf-8')
    industry_info = pd.read_csv(ConfigUtils.get_stock("STOCK_INDUSTRY"), encoding='utf-8')
    company_info = pd.read_csv(ConfigUtils.get_stock("STOCK_NAME"), encoding='utf-8')
    company_info = company_info.merge(industry_info, how='left', on=['code', 'code_name'])

    # 时序处理
    dt = datetime.date.today()
    tmp_list = sorted([row['calendar_date'] for idx, row in date_info.iterrows() if row['calendar_date'] < str(dt) and row['calendar_date'] >= start_dt and row['is_trading_day'] == 1], reverse=True)
    date_map = dict(zip(tmp_list, range(len(tmp_list))))
    # 读取股票交易信息
    stock_info = pd.DataFrame()
    remove_stock = []
    tmp_list = []

    for i, row in tqdm.tqdm(company_info.iterrows()):
        code, name = row["code"], row["code_name"]
        path = os.path.join(ConfigUtils.get_stock("DATA_DIR"), code + "_" + name + ".csv")
        if not os.path.exists(path):
                continue
        tmp_df = pd.read_csv(path)
        tmp_df = tmp_df[tmp_df.date >= start_dt]
        if len(tmp_df) < 60 or code.startswith('sz.300') or code.startswith('sh.688'):# 去除一些上市不久的企业 688 300
                remove_stock.append(code)
                continue
        tmp_df = tmp_df.sort_values('date', ascending=True).reset_index()
        tmp_list.append(tmp_df)

    stock_info = pd.concat(tmp_list)
    ts_code_map = dict(zip(stock_info['code'].unique(), range(stock_info['code'].nunique())))
    stock_info = stock_info.reset_index()
    stock_info['ts_code_id'] = stock_info['code'].map(ts_code_map)
    stock_info['trade_date_id'] = stock_info['date'].map(date_map)
    stock_info['ts_date_id'] = (10000 + stock_info['ts_code_id']) * 10000 + stock_info['trade_date_id']
    stock_info = stock_info.merge(company_info, how='left', on='code')
    # 特征工程
    col = ['close', 'open', 'high', 'low']
    feature_col = []
    for tmp_col in col:
        stock_info[tmp_col+'_'+'transform'] = (stock_info[tmp_col] - stock_info['preclose']) / stock_info['preclose']
        feature_col.append(tmp_col+'_'+'transform')
    
    # 提取前5天收盘价与今天收盘价的盈亏比
    for i in range(5):
        tmp_df = pd.DataFrame(stock_info, columns=['ts_date_id', 'close'])
        tmp_df = tmp_df.rename(columns={'close':'close_shift_{}'.format(i+1)})
        feature_col.append('close_shift_{}'.format(i+1))
        tmp_df['ts_date_id'] = tmp_df['ts_date_id'] + i + 1
        stock_info = stock_info.merge(tmp_df, how='left', on='ts_date_id')
    
    stock_info.drop('level_0', axis=1, inplace=True)
    for i in range(5):
        stock_info['close_shift_{}'.format(i+1)] = (stock_info['close'] - stock_info['close_shift_{}'.format(i+1)]) / stock_info['close_shift_{}'.format(i+1)]
    # print(stock_info)
    # stock_info.dropna(inplace=True)
    # 标签制作

    # make_label
    use_col = []
    for i in range(5):
        tmp_df = stock_info[['ts_date_id', 'high', 'low']]
        tmp_df = tmp_df.rename(columns={'high':'high_shift_{}'.format(i+1), 'low':'low_shift_{}'.format(i+1)})
        use_col.append('high_shift_{}'.format(i+1))
        use_col.append('low_shift_{}'.format(i+1))
        tmp_df['ts_date_id'] = tmp_df['ts_date_id'] - i - 1
        stock_info = stock_info.merge(tmp_df, how='left', on='ts_date_id')
    
    #stock_info.dropna(inplace=True)
    for i in range(5):
        stock_info['high_shift_{}'.format(i+1)] = (stock_info['high_shift_{}'.format(i+1)] - stock_info['close']) / stock_info['close']
        stock_info['low_shift_{}'.format(i+1)] = (stock_info['low_shift_{}'.format(i+1)] - stock_info['close']) / stock_info['close']

    tmp_array = stock_info[use_col].values
    max_increse = np.max(tmp_array, axis=1)
    min_increse = np.min(tmp_array, axis=1)
    stock_info['label_max'] = max_increse
    stock_info['label_min'] = min_increse
    stock_info['change'] = (stock_info['high'] - stock_info['low']) / stock_info['preclose']
    stock_info['label_final'] = (stock_info['label_max'] > 0.06) & (stock_info['label_min'] > -0.03)
    stock_info['label_final'] = stock_info['label_final'].apply(lambda x: int(x))

    # print(stock_info[stock_info.date == '2020-08-21'])
    # print(stock_info[stock_info.label_final == 1])
    # stock_info = stock_info.reset_index()
    stock_info = stock_info.reset_index()
    stock_info.drop('index', axis=1, inplace=True)
    stock_info.to_csv(ConfigUtils.get_stock("STOCKS_DATESET"),  index=False)
    
if __name__ == '__main__':
    # init_trade_date()
    # dt = get_recently_trade_date()
    gen_dataset()
    # print(get_price('sz.300111', '向日葵', '2020-08-20'))
