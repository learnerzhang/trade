# -*- encoding: UTF-8 -*-
from api_modules.server.utils.config import ConfigUtils
from api_modules.server.utils import stock_utils
from api_modules.server.models import Transaction, Share, CalendarDate
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import pandas as pd


def init_dates():
    from api_modules.server.models import db_session
    date_path = ConfigUtils.get_stock('STOCKS_DATE')
    date_pd = pd.read_csv(date_path, encoding='utf-8')
    dates = list()
    for index, row in date_pd.iterrows():
        calendar_date = row['calendar_date']
        is_trading_day = int(row['is_trading_day'])
        tmp_cal = CalendarDate(calendar_date=calendar_date, is_trading_day=is_trading_day)
        dates.append(tmp_cal)
    # insert db
    db_session.add_all(dates)
    db_session.commit()

def init_shares():
    from api_modules.server.models import db_session
    industry_path = ConfigUtils.get_stock('STOCK_INDUSTRY')
    stock_path = ConfigUtils.get_stock('STOCK_NAME')
    industry_pd = pd.read_csv(industry_path, encoding='utf-8')
    stock_pd = pd.read_csv(stock_path, encoding='utf-8')
    share_pd = pd.merge(stock_pd, industry_pd, how='left', on=['code', 'code_name'])
    shares = list()
    # init shares
    for index, row in share_pd.iterrows():
        code = row['code']
        name = row['code_name']
        industry = None if pd.isna(row['industry']) else row['industry']
        industryClassification = None if pd.isna(row['industryClassification']) else row['industryClassification']
        tmp_share = Share(code=code, name=name, industry=industry, industryClassification=industryClassification)
        shares.append(tmp_share)
    # insert db
    db_session.add_all(shares)
    db_session.commit()


def init_transaction():
    from api_modules.server.models import db_session
    stock_path = ConfigUtils.get_stock('STOCK_NAME')
    stock_pd = pd.read_csv(stock_path, encoding='utf-8')
    # print(stock_pd.to_dict('index'))
    for index, elem in stock_pd.to_dict('index').items():
        code, name = elem['code'], elem['code_name']
        code_name = (code, name)
        stock_data = stock_utils.read_data(code_name)
        stock_data.fillna(0, inplace=True)
        tras = list()
        for idx, ele in stock_data.to_dict('index').items():
            tra = Transaction(code=code, name=name)
            tra.build_from_dict(ele)
            tra.set_type(1)
            tras.append(tra)
        db_session.add_all(tras)
        db_session.commit()

def syncup_transaction():
    from api_modules.server.models import db_session
    stock_path = ConfigUtils.get_stock('STOCK_NAME')
    stock_pd = pd.read_csv(stock_path, encoding='utf-8')
    # print(stock_pd.to_dict('index'))
    for index, elem in stock_pd.to_dict('index').items():
        code, name = elem['code'], elem['code_name']
        code_name = (code, name)
        stock_data = stock_utils.read_data(code_name)
        stock_data.fillna(0, inplace=True)
        tmp_stock = stock_data.tail(1)
        try:
            tras = list()
            for idx, ele in tmp_stock.to_dict('index').items():
                tra = Transaction(code=code, name=name)
                tra.build_from_dict(ele)
                tra.set_type(1)
                tras.append(tra)
            db_session.add_all(tras)
            db_session.commit()
        except IntegrityError as e:
            pass
        except InvalidRequestError as e:
            pass
    print("syncup transaction done.")

def init_funds():
    pass


if __name__ == '__main__':
    # init_shares()
    # init_dates()
    init_transaction()
    # syncup_transaction()