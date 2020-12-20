# -*- encoding: UTF-8 -*-

import talib as tl
import pandas as pd
import logging


# 持续上涨（MA30向上）
def check(code_name, data, end_date=None, threshold=30):
    if len(data) < threshold:
        logging.debug("{0}:样本小于{1}天...\n".format(code_name, threshold))
        return -2
    data['ma30'] = pd.Series(tl.MA(data['close'].values, 30), index=data.index.values)
    begin_date = data.iloc[0].date
    if end_date is not None:
        if end_date < begin_date:  # 该股票在end_date时还未上市
            logging.debug("{}在{}时还未上市".format(code_name, end_date))
            return -1

    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]

    data = data.tail(n=threshold)
    step1 = round(threshold/3)
    step2 = round(threshold*2/3)

    v1 = (data.iloc[step1]['ma30'] - data.iloc[0]['ma30']) / data.iloc[0]['ma30']
    v2 = (data.iloc[step2]['ma30'] - data.iloc[step1]['ma30']) / data.iloc[step1]['ma30']
    v3 = (data.iloc[-1]['ma30'] - data.iloc[step2]['ma30']) / data.iloc[step2]['ma30']
    v4 = (data.iloc[-1]['ma30'] - 1.2*data.iloc[0]['ma30']) / data.iloc[0]['ma30']
    return round(v1 * v2 * v3 * v4, 3)

