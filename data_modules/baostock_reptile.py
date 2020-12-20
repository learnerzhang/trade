# -*- encoding: UTF-8 -*-
import getopt
import sys

import baostock as bs
import pandas as pd
import logging
import os
from multiprocessing import Pool
from common import stock_utils
from common.config import ConfigUtils

logging.basicConfig(format='%(asctime)s %(message)s', filename='sequoia.log')
logging.getLogger().setLevel(logging.INFO)

"""
    同步stock数据
"""


def hs300_stocks():
	# 登陆系统
	lg = bs.login()
	# 显示登陆返回信息
	print('login respond error_code:' + lg.error_code)
	print('login respond  error_msg:' + lg.error_msg)

	# 获取证券基本资料
	rs = bs.query_hs300_stocks()
	print('query_hs300 error_code:' + rs.error_code)
	print('query_hs300  error_msg:' + rs.error_msg)

	# 打印结果集
	hs300_stocks = []
	while (rs.error_code == '0') & rs.next():
		# 获取一条记录，将记录合并在一起
		hs300_stocks.append(rs.get_row_data())
	result = pd.DataFrame(hs300_stocks, columns=rs.fields)
	# 结果集输出到csv文件
	# result.to_csv("D:/hs300_stocks.csv", encoding="gbk", index=False)
	result.to_csv(ConfigUtils.get_stock("HS_300_STOCK_NAME"), index=False)
	print(result.tail())
	print("init all hs300 stock names")


def get_all_stock_names():
	# 登陆系统 ####
	lg = bs.login()
	# 显示登陆返回信息
	print('login respond error_code:' + lg.error_code + ', error_msg:' + lg.error_msg)
	dt = stock_utils.get_recently_trade_date()
	dt = '2020-08-03'
	k_rs = bs.query_all_stock(day=dt)
	print(k_rs)
	data_list = []
	while (k_rs.error_code == '0') & k_rs.next():
		# 获取一条记录，将记录合并在一起
		data_list.append(k_rs.get_row_data())
	result = pd.DataFrame(data_list, columns=k_rs.fields)
	print(result.tail())
	result.to_csv(ConfigUtils.get_stock("STOCK_NAME"), index=False)
	print("init all stock names")
	bs.logout()


def get_all_stock_industries():
	lg = bs.login()
	print('login respond error_code:' + lg.error_code)
	print('login respond  error_msg:' + lg.error_msg)

	# 获取行业分类数据
	rs = bs.query_stock_industry(date='2020-08-01')
	# rs = bs.query_stock_basic(code_name="浦发银行")
	print('query_stock_industry error_code:' + rs.error_code)
	print('query_stock_industry respond  error_msg:' + rs.error_msg)

	# 打印结果集
	industry_list = []
	while (rs.error_code == '0') & rs.next():
		# 获取一条记录，将记录合并在一起
		industry_list.append(rs.get_row_data())
	result = pd.DataFrame(industry_list, columns=rs.fields)
	# 结果集输出到csv文件
	result.to_csv(ConfigUtils.get_stock("STOCK_INDUSTRY"), index=False)
	print(result)
	# 登出系统
	bs.logout()


def update_trades(select=False):
	try:
		et = stock_utils.get_recently_trade_date()
		st = ConfigUtils.get_stock("START_DATE")
		print(st, et)
		# 登陆系统 ####
		lg = bs.login()
		# 显示登陆返回信息
		print('login respond error_code:' + lg.error_code + ', error_msg:' + lg.error_msg)

		if not select:
			print("stock—name path:", ConfigUtils.get_stock("STOCK_NAME"))
			pd_names = pd.read_csv(ConfigUtils.get_stock("STOCK_NAME"))
		else:
			pd_names = pd.read_csv(ConfigUtils.get_stock("HS_300_STOCK_NAME"))

		for index, row in pd_names.iterrows():
			code = row['code']
			name = row['code_name']
			k_rs = bs.query_history_k_data_plus(code, ConfigUtils.get_stock("STOCK_FIELDS"), start_date=st, end_date=et)
			data_list = []
			while (k_rs.error_code == '0') & k_rs.next():
				# 获取一条记录，将记录合并在一起
				data_list.append(k_rs.get_row_data())
			result = pd.DataFrame(data_list, columns=k_rs.fields)
			print(result.tail())
			if not os.path.exists(ConfigUtils.get_stock("DATA_DIR")):
				os.makedirs(ConfigUtils.get_stock("DATA_DIR"))
			result.to_csv(os.path.join(ConfigUtils.get_stock("DATA_DIR"), code + "_" + name + ".csv"), index=False)
			print("Downloading :" + code + " , name :" + name)
		bs.logout()
	except IOError as e:
		print("Update Data Error ", e)


def main(argv):
	mode = None
	try:
		opts, args = getopt.getopt(argv, "hm:", ["mode"])
	except getopt.GetoptError:
		print('baostock_reptile.py -m <mode:hs300:all>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('baostock_reptile.py -m <mode>')
			sys.exit()
		elif opt in ("-m", "--model"):
			mode = arg

	if mode == 'hs300':
		hs300_stocks()

	if mode == 'all':
		update_trades(select=False)


if __name__ == '__main__':
	main(sys.argv[1:])
