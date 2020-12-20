# -*- coding: UTF-8 -*-
import logging
import math
import talib as tl

# 总市值
BALANCE = 200000


# 最后一个交易日收市价为指定区间内最高价
def check_enter(code_name, data, end_date=None, threshold=10):
    code, name = code_name[0], code_name[1]
    max_price = 0
    min_price = 999999
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return -2
    data = data.tail(n=threshold)
    if len(data) < threshold:
        return -2
    for index, row in data.iterrows():
        if row['close'] > max_price:
            max_price = float(row['close'])
        if row['close'] < min_price:
            min_price = float(row['close'])

    last_close = data.iloc[-1]['close']
    if last_close >= max_price:
        return round(1.0 * (last_close - min_price) / min_price, 3)
    return -1

def continue_inc(code_name, data, end_date=None, threshold=3):
    code, name = code_name[0], code_name[1]
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return -2
    data = data.tail(n=threshold)
    if len(data) < threshold:
        return -1

    flags = []
    val = 0.0
    for index, row in data.iterrows():
        tmp = (float(row['close']) - float(row['preclose'])) / float(row['preclose'])
        val += tmp
        if tmp > 0:
            flags.append(True)
        else:
            flags.append(False)

    if False in flags:
        return 0.0
    else:
        return val


def continue_increase3(code_name, data, end_date=None, threshold=3):
    return continue_inc(code_name, data, end_date=end_date, threshold=threshold)


def continue_increase5(code_name, data, end_date=None, threshold=5):
    return continue_inc(code_name, data, end_date=end_date, threshold=threshold)


def continue_increase7(code_name, data, end_date=None, threshold=7):
    return continue_inc(code_name, data, end_date=end_date, threshold=threshold)

def big_inc(code_name, data, end_date=None, threshold=3):
    code, name = code_name[0], code_name[1]
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return -2
    data = data.tail(n=threshold)
    if len(data) < threshold:
        return -1

    flags = []
    inc = 0.0
    for index, row in data.iterrows():
        tmp_inc = (float(row['close']) - float(row['preclose'])) / float(row['preclose'])
        inc += tmp_inc
        if index == 0 and row['close'] == row['high'] and tmp_inc > 0.05:
            flags.append(True)
        if index == 2 and tmp_inc > 0.05:
            flags.append(True)
    
    if False in flags:
        return 0.0
    else:
        return inc

def continue_cyin(code_name, data, end_date=None, threshold=5, num=1):
    code, name = code_name[0], code_name[1]
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return -2
    data = data.tail(n=threshold)
    if len(data) < threshold:
        return -1

    flags = []
    val = 0.0
    for index, row in data.iterrows():
        tmp = (float(row['close']) - float(row['open'])) / float(row['open'])
        val += tmp
        if tmp > 0:
            flags.append(True)
        else:
            flags.append(False)

    if flags.count(False) > num:
        return 0.0
    else:
        return val

def demon_inc(code_name, data, end_date=None, threshold=20):
    code, name = code_name[0], code_name[1]
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return -2
    data = data.tail(n=threshold)
    if len(data) < threshold:
        return -1
    
    row_list = list(data.iterrows())
    start_r = row_list[0][1]
    mid_r = row_list[9][1]
    end_r = row_list[19][1]

    s_pre_close = float(start_r['preclose'])
    s_price = float(start_r['close'])

    m_pre_close = float(mid_r['preclose'])
    m_price = float(mid_r['close'])

    e_price = float(end_r['close'])

    inc1 = (m_price - s_pre_close) * 1.0 / s_pre_close
    inc2 = (e_price - m_pre_close) * 1.0 / m_pre_close
    if  inc1 > 0.1 and inc1 < 0.2 and  inc2 > 0.1 and inc2 < 0.2:
        return inc1 + inc2
    else:
        return 0

def big_inc(code_name, data, end_date=None, threshold=3):
    code, name = code_name[0], code_name[1]
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return -2
    data = data.tail(n=threshold)
    if len(data) < threshold:
        return -1

    flags = []
    inc = 0.0
    for index, row in data.iterrows():
        tmp_inc = (float(row['close']) - float(row['preclose'])) / float(row['preclose'])
        inc += tmp_inc
        if index == 0 and row['close'] == row['high'] and tmp_inc > 0.05:
            flags.append(True)
        if index == 2 and tmp_inc > 0.05:
            flags.append(True)
    
    if False in flags:
        return 0.0
    else:
        return inc

def break_inc(code_name, data, end_date=None, threshold=10,):
    code, name = code_name[0], code_name[1]
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return -2
    # 新高
    close_max = data.max()['close']
    
    data = data.tail(n=threshold)
    # 放量
    volume_max = data.max()['volume']
    if len(data) < threshold:
        return -1
    
    flag = False
    turn = 0.0
    open = 0.0
    close = 0.0
    pre_close = 0.0
    volume = 0.0
    pchg = 0.0

    for index, row in data.iterrows():
        pre_close = float(row['preclose'])
        close = float(row['close'])
        open = float(row['open'])
        turn = float(row['turn'])
        volume = float(row['volume'])
    
    if turn > 4.5 and close == close_max and volume >= volume_max*0.7 and close > open:
        return (close - pre_close) / pre_close
    return 0

def inc_cyin1(code_name, data, end_date=None, threshold=5, n=1):
    return continue_cyin(code_name, data, end_date=end_date, threshold=threshold, num=n)


def inc_cyin2(code_name, data, end_date=None, threshold=5, n=2):
    return continue_cyin(code_name, data, end_date=end_date, threshold=threshold, num=n)


# 最后一个交易日收市价为指定区间内最低价
def check_exit(code_name, data, end_date=None, threshold=10):
    if data is None:
        return True
    min_price = 999999
    max_price = 0
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    data = data.tail(n=threshold)
    if len(data) < threshold:
        logging.debug("{0}:样本小于{1}天...\n".format(code_name, threshold))
        return -2
    for index, row in data.iterrows():
        if row['close'] < min_price:
            min_price = float(row['close'])
        if row['close'] > max_price:
            max_price = float(row['close'])

    last_close = data.iloc[-1]['close']
    if last_close <= min_price:
        return round(1.0 * (max_price - last_close) / max_price, 3)
    return -1


def feedback_inc(code_name, data, end_date=None, threshold=50,):
    code, name = code_name[0], code_name[1]
    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]
    if data is None:
        return -2
    # 新高
    data = data.tail(n=threshold)
    max_close_idx = data["close"].idxmax()
    max_close = data["close"].max()
    min_close_idx = data["close"].idxmin()
    min_close = data["close"].min()

    min_low_idx = data["low"].idxmin()
    min_low = data["low"].min()
    min_low_close = 0.0

    min_volume_idx = data['volume'].idxmin()
    min_volume = data['volume'].min()

    de_inc_duration = 0
    inc_duration = 0

    for index, row in data.iterrows():
        pre_close = float(row['preclose'])
        close = float(row['close'])
        open = float(row['open'])
        turn = float(row['turn'])
        volume = float(row['volume'])

        if min_low_close < close < open and index < min_close_idx:
            de_inc_duration += 1
        if close > min_low_close and index > min_close_idx and open < close:
            inc_duration += 1

        if index == min_low_idx:
            min_low_close = close

    result = 0.0
    if (min_low_close - min_low)/min_low > 0.05:
        result += (min_low_close - min_low)/min_low

    if 10 > len(data) - min_low_idx > 5:
        result += (close - min_close) / min_close

    # if de_inc_duration > inc_duration > 3:
    #     result += (close - min_close) / min_close
    return result

# 绝对波动幅度
def real_atr(n, amount):
    return n * amount

