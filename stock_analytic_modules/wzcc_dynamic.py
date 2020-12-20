#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/29 5:09 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : wzcc_dynamic.py
# @Software: PyCharm
import codecs
import csv
import os
import pandas as pd
import tqdm
from common.config import ConfigUtils

wz_path = ConfigUtils.get_stock("WZ_DIR")

names = list(os.listdir(wz_path))
dates = sorted([name[3:-4] for name in names])
dates = dates[-100:]

stock_percent_dict = {}
stock_amount_dict = {}
stocks = set()

for name in tqdm.tqdm(names):
	date = name[3:-4]
	df = pd.read_csv(os.path.join(wz_path, name))

	# print(list(df.iterrows())[0])
	for index, row in df.iterrows():
		stock_name = row['name']
		percentage = row['percentage']
		amount = row['amount']
		stocks.add(stock_name)
		# print(row['code'], row['name'], row['amount'], row['percentage'])
		if stock_name not in stock_percent_dict:
			stock_percent_dict[stock_name] = {}

		if stock_name not in stock_amount_dict:
			stock_amount_dict[stock_name] = {}
		stock_percent_dict[stock_name][date] = percentage
		stock_amount_dict[stock_name][date] = amount
	# break

print(len(stocks), stocks)
# print(stock_amount_dict)
# print(stock_percent_dict)

with open("test.csv", 'w+', newline='', encoding='utf-8-sig') as csvfile:
	writer = csv.writer(csvfile)
	# 先写入columns_name
	writer.writerow(['名称'] + dates)
	for name in tqdm.tqdm(stocks):
		tmp_row = [name]
		for d in dates:
			per = stock_percent_dict[name][d] if d in stock_percent_dict[name] else 0
			tmp_row.append(per)
		# print(tmp_row)
		writer.writerow(tmp_row)
