# -*- encoding: UTF-8 -*-

import talib as tl
import pandas as pd
import logging
from datetime import datetime, timedelta


#  市盈率
def check(code_name, data, end_date=None, threshold=60):
    # pctChg,pbMRQ,peTTM,psTTM,pcfNcfTTM,isST
    data['pe25'] = pd.Series(tl.MA(data['peTTM'].values, 25), index=data.index.values)
    print(data['pe25'])
    return True

