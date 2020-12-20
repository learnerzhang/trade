import datetime
import sys

import pandas as pd
import numpy as np
import tqdm
import os
from common.config import ConfigUtils
from common.stock_utils import is_jiucaiban, is_index


def filter_stock(df, code, name):
    if len(df) < 60 or is_jiucaiban(code) or is_index(code, name):  # 去除一些上市不久的企业 688 300 399
        return True
    else:
        return False


def select_stock():
    pass


def generate_feature():
    start_dt = '2019-01-01'
    date_info = pd.read_csv(ConfigUtils.get_stock("STOCKS_DATE"), encoding='utf-8')
    company_info = pd.read_csv(ConfigUtils.get_stock("HS_300_STOCK_NAME"), encoding='utf-8')

    # 时序处理
    dt = datetime.date.today()
    tmp_list = sorted([row['calendar_date'] for idx, row in date_info.iterrows() if
                       row['calendar_date'] < str(dt) and row['calendar_date'] >= start_dt and row[
                           'is_trading_day'] == 1], reverse=True)
    date_map = dict(zip(tmp_list, range(len(tmp_list))))
    # 读取股票交易信息
    remove_stock = []
    tmp_list = []

    for i, row in tqdm.tqdm(company_info.iterrows()):
        code, name = row["code"], row["code_name"]
        path = os.path.join(ConfigUtils.get_stock("DATA_DIR"), code + "_" + name + ".csv")
        if not os.path.exists(path):
            continue
        tmp_df = pd.read_csv(path)
        tmp_df = tmp_df[tmp_df.date >= start_dt]

        if filter_stock(tmp_df, code, name):
            remove_stock.append(code)
            continue
        tmp_df = tmp_df.sort_values('date', ascending=True).reset_index()
        tmp_list.append(tmp_df)

    stock_info = pd.concat(tmp_list)
    ts_code_map = dict(zip(stock_info['code'].unique(), range(stock_info['code'].nunique())))
    stock_info = stock_info.reset_index()
    stock_info['ts_code_id'] = stock_info['code'].map(ts_code_map)
    stock_info.drop('index', axis=1, inplace=True)
    stock_info['trade_date_id'] = stock_info['date'].map(date_map)
    stock_info['ts_date_id'] = (10000 + stock_info['ts_code_id']) * 10000 + stock_info['trade_date_id']

    # 特征工程
    col = ['close', 'open', 'high', 'low']
    feature_col = []
    for tmp_col in col:
        stock_info[tmp_col + '_' + 'transform'] = (stock_info[tmp_col] - stock_info['preclose']) / stock_info[
            'preclose']
        feature_col.append(tmp_col + '_' + 'transform')

    print('stock_info 占据内存约: {:.2f} GB'.format(sys.getsizeof(stock_info) / (1024 ** 3)))
    # 提取前5天收盘价与今天收盘价的盈亏比, 增加10, 20, 30, 40, 50, 60, 120, 180
    for i in [0, 1, 2, 3, 4, 9, 19, 29, 39, 49, 59, 79, 99, 119, 149, 179, 199, 249]:
        tmp_df = pd.DataFrame(stock_info, columns=['ts_date_id', 'close'], dtype='float32')
        tmp_df = tmp_df.rename(columns={'close': 'close_shift_{}'.format(i + 1)})
        feature_col.append('close_shift_{}'.format(i + 1))
        tmp_df['ts_date_id'] = tmp_df['ts_date_id'] + i + 1

        stock_info = pd.merge(stock_info, tmp_df, how='left', on='ts_date_id')
        stock_info.drop_duplicates(subset=['ts_date_id'], keep='last', inplace=True)

    stock_info.drop('level_0', axis=1, inplace=True)
    for i in [0, 1, 2, 3, 4, 9, 19, 29, 39, 49, 59, 79, 99, 119, 149, 179, 199, 249]:
        stock_info['close_shift_{}'.format(i + 1)] = (stock_info['close'] - stock_info[
            'close_shift_{}'.format(i + 1)]) / stock_info['close_shift_{}'.format(i + 1)]

    # print(stock_info)
    # stock_info.dropna(inplace=True)
    # 标签制作

    # make_label  未来2天的涨幅
    use_col = []
    for i in range(3):
        tmp_df = stock_info[['ts_date_id', 'high', 'low']]
        tmp_df = tmp_df.rename(columns={'high': 'high_shift_{}'.format(i + 1), 'low': 'low_shift_{}'.format(i + 1)})
        use_col.append('high_shift_{}'.format(i + 1))
        use_col.append('low_shift_{}'.format(i + 1))
        tmp_df['ts_date_id'] = tmp_df['ts_date_id'] - i - 1
        stock_info = stock_info.merge(tmp_df, how='left', on='ts_date_id')

    # stock_info.dropna(inplace=True)
    for i in range(3):
        stock_info['high_shift_{}'.format(i + 1)] = (stock_info['high_shift_{}'.format(i + 1)] - stock_info['close']) / \
                                                    stock_info['close']
        stock_info['low_shift_{}'.format(i + 1)] = (stock_info['low_shift_{}'.format(i + 1)] - stock_info['close']) / \
                                                   stock_info['close']

    tmp_array = stock_info[use_col].values
    max_increse = np.max(tmp_array, axis=1)
    min_increse = np.min(tmp_array, axis=1)
    stock_info['label_max'] = max_increse
    stock_info['label_min'] = min_increse
    stock_info['change'] = (stock_info['high'] - stock_info['low']) / stock_info['preclose']
    # stock_info['label_final'] = (stock_info['label_max'] > 0.06) & (stock_info['label_min'] > -0.03)
    stock_info['label_final'] = (stock_info['label_max'] - stock_info['label_min']) * 100
    stock_info = stock_info.dropna(subset=['label_final'])

    def label_fun(x):
        if x >= 20:
            return 20
        else:
            return x

    stock_info['label_final'] = stock_info['label_final'].apply(lambda x: label_fun(x))

    stock_info['label_final'] = stock_info['label_final'].apply(lambda x: int(x))
    print("正负样本：", stock_info['label_final'].value_counts())
    # print(stock_info[stock_info.date == '2020-08-21'])
    # print(stock_info[stock_info.label_final == 1])
    # stock_info = stock_info.reset_index()
    stock_info = stock_info.reset_index()
    stock_info.drop('index', axis=1, inplace=True)
    stock_info.to_csv(ConfigUtils.get_stock("STOCKS_DATESET"), index=False)


if __name__ == '__main__':
    generate_feature()
