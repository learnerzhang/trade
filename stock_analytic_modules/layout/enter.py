# -*- encoding: UTF-8 -*-
import numpy as np
import talib as tl
import pandas as pd
import logging


# TODO 真实波动幅度（ATR）放大
# 最后一个交易日收市价从下向上突破指定区间内最高价
def check_breakthrough(code_name, data, end_date=None, threshold=30):
    max_price = 0
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    data = data.tail(n=threshold + 1)
    if len(data) < threshold + 1:
        logging.debug("{0}:样本小于{1}天...\n".format(code_name, threshold))
        return False

    # 最后一天收市价
    last_close = float(data.iloc[-1]['close'])
    last_open = float(data.iloc[-1]['open'])

    data = data.head(n=threshold)
    second_last_close = data.iloc[-1]['close']

    for index, row in data.iterrows():
        if row['close'] > max_price:
            max_price = float(row['close'])

    if last_close > max_price > second_last_close and max_price > last_open and last_close / last_open > 1.06:
        return True
    else:
        return False


# 收盘价高于N日均线
def check_ma(code_name, data, end_date=None, ma_days=250):
    if data is None or len(data) < ma_days:
        logging.debug("{0}:样本小于{1}天...\n".format(code_name, ma_days))
        return False

    ma_tag = 'ma' + str(ma_days)
    data['close'] = data['close'].astype(float)
    close = np.array(data['close'], dtype=np.object)
    data[ma_tag] = pd.Series(tl.MA(data['close'].values, ma_days), index=data.index.values)

    begin_date = data.iloc[0].date
    if end_date is not None:
        if end_date < begin_date:  # 该股票在end_date时还未上市
            logging.debug("{}在{}时还未上市".format(code_name, end_date))
            return False
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]

    last_close = data.iloc[-1]['close']
    last_ma = data.iloc[-1][ma_tag]
    if last_close > last_ma:
        return True
    else:
        return False


# 上市日小于60天
def check_new(code_name, data, end_date=None, threshold=60):
    size = len(data.index)
    if size < threshold:
        return True
    else:
        return False


def check_volume(code_name, data, end_date=None, threshold=60):
    # # 流通市值不低于300亿
    # if code_name[2] < 3000000:
    #     return False

    volume_data = np.array([float(x) for x in data['volume']])
    data['vol_ma5'] = pd.Series(tl.MA(volume_data, 5), index=data.index.values)
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data.empty:
        return -4
    p_change = data.iloc[-1]['pctChg']
    if p_change < 2 or data.iloc[-1]['close'] < data.iloc[-1]['open']:
        return -3
    data = data.tail(n=threshold + 1)
    if len(data) < threshold + 1:
        logging.debug("{0}:样本小于{1}天...\n".format(code_name, threshold))
        return -2

    # 最后一天收盘价
    last_close = data.iloc[-1]['close']
    # 最后一天成交量
    last_vol = data.iloc[-1]['volume']

    amount = last_close * last_vol * 100
    # 成交额不低于2亿
    if amount < 200000000:
        return -1

    data = data.head(n=threshold)
    mean_vol = data.iloc[-1]['vol_ma5']

    vol_ratio = last_vol / mean_vol
    if vol_ratio >= 1.5:
        msg = "*{0}\n量比：{1:.2f}\t涨幅：{2}%\n".format(code_name, vol_ratio, p_change)
        logging.debug(msg)
        return round(vol_ratio, 2)
    else:
        return 0


# 量比大于3.0
def check_continuous_inc(code_name, data, end_date=None, threshold=1, window_size=3):
    stock = code_name[0]
    name = code_name[1]
    data['vol_ma5'] = pd.Series(tl.MA(data['volume'].values, 5), index=data.index.values)
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]

    data = data.tail(n=threshold)
    if len(data) < threshold:
        return -1

    flags = []
    val = 0.0
    for index, row in data.iterrows():
        tmp = (float(row['close']) - float(row['preclose'])) / float(row['preclose'])
        val += tmp
        if tmp > 0.06:
            flags.append(True)
        else:
            flags.append(False)

    if False in flags:
        return 0.0
    else:
        return val