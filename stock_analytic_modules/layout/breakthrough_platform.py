# -*- encoding: UTF-8 -*-

import talib as tl
import pandas as pd
import logging
from stock_analytic_modules.layout import enter


# 平台突破策略
def check(code_name, data, end_date=None, threshold=60):
    origin_data = data
    if len(data) < threshold:
        logging.debug("{0}:样本小于{1}天...\n".format(code_name, threshold))
        return -2
    data['ma60'] = pd.Series(tl.MA(data['close'].values, 60), index=data.index.values)

    begin_date = data.iloc[0].date
    if end_date is not None:
        if end_date < begin_date:  # 该股票在end_date时还未上市
            logging.debug("{}在{}时还未上市".format(code_name, end_date))
            return -2

    if end_date is not None:
        mask = (data['date'] <= end_date)
        data = data.loc[mask]

    data = data.tail(n=threshold)

    breakthrough_row = None

    for index, row in data.iterrows():
        if row['open'] < row['ma60'] <= row['close']:
            if enter.check_volume(code_name, origin_data, row['date'], threshold):
                breakthrough_row = row

    if breakthrough_row is None:
        return -1

    data_front = data.loc[(data['date'] < breakthrough_row['date'])]
    data_end = data.loc[(data['date'] >= breakthrough_row['date'])]

    r = 0.0
    for index, row in data_front.iterrows():
        r = (row['ma60'] - row['close']) / row['ma60']
        if not (-0.05 < r < 0.2):
            break

    logging.info("股票{0} 突破日期：{1}".format(code_name, breakthrough_row['date']))

    return round(r, 3)






