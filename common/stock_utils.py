# -*- coding: UTF-8 -*-
from pandas.tseries.offsets import *
import baostock as bs
import pandas as pd

import datetime
import xlrd
import os

from common.config import ConfigUtils

market_map = {'主板': 0, '中小板': 1}
exchange_map = {'SZSE': 0, 'SSE': 1}
is_hs_map = {'S': 0, 'N': 1, 'H': 2}
area_map = {'深圳': 0, '北京': 1, '吉林': 2, '江苏': 3, '辽宁': 4, '广东': 5, '安徽': 6, '四川': 7, '浙江': 8, '湖南': 9, '河北': 10,
			'新疆': 11, '山东': 12, '河南': 13, '山西': 14, '江西': 15, '青海': 16, '湖北': 17, '内蒙': 18, '海南': 19, '重庆': 20,
			'陕西': 21, '福建': 22, '广西': 23, '天津': 24, '云南': 25, '贵州': 26, '甘肃': 27, '宁夏': 28, '黑龙江': 29, '上海': 30,
			'西藏': 31}
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
	total_num = int(money / (100 * price))
	buy_num = 0
	if total_num > 6:
		buy_num = int(total_num / 3)
	elif total_num > 4:
		buy_num = int(total_num / 2)
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


def is_jiucaiban(code):
	if code:
		return code.startswith('sz.300') or code.startswith('sh.688')
	return False


def is_index(code, name):
	if code:
		return code.startswith("sz.399") or ("指数" in name) or ("小盘" in name) or ("等权" in name) \
			   or ("国企" in name) or ("龙头" in name) or ("民企" in name) or ("综指" in name) \
			   or ("上证" in name)
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


def get_recently_trade_date(dt=datetime.date.today()):
	date_path = ConfigUtils.get_stock("STOCKS_DATE")
	print(date_path)
	if date_path and os.path.exists(date_path):
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


def get_trade_dates(start='2010-01-01', end='2020-12-30'):
	date_path = ConfigUtils.get_stock("STOCKS_DATE")
	print(date_path)
	trade_dates = pd.read_csv(ConfigUtils.get_stock("STOCKS_DATE"), header=0)
	trade_dates = trade_dates[(trade_dates['calendar_date'] >= start) &
							  (trade_dates['calendar_date'] <= end) &
							  (trade_dates['is_trading_day'] == 1)]
	# print(trade_dates['calendar_date'].values)
	return trade_dates['calendar_date'].values


if __name__ == '__main__':
	# init_trade_date()
	get_trade_dates()
	dt = get_recently_trade_date()
	print(dt)
	# gen_dataset()
	# print(get_price('sz.300111', '向日葵', '2020-08-20'))
