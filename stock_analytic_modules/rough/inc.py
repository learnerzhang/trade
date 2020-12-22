#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 12:58 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : inc.py
# @Software: PyCharm
import getopt
import sys
import datetime
import numpy as np
from tqdm import tqdm
import json
from common import stock_utils
from scipy import signal
import matplotlib.pyplot as plt
import collections
from common.config import ConfigUtils
from common.entity import Record
from common.mail_utils import send_hot_share_mail, send_month_share_mail
from common.sql_utils import get_mark_stocks, insert_records, get_records, get_period_records
from common.stock_utils import get_recently_trade_date
from stock_analytic_modules.rough.m_hunt import get_m_candidates
from stock_analytic_modules.utils.helper import moving_average, slope
import pandas as pd


def gen_records(day_ago=0):
	records = list()

	pd_names = pd.read_csv(ConfigUtils.get_stock("STOCK_NAME"))
	# 数据库获取沪、深、中小板
	zxb_stocks = [s.code for s in get_mark_stocks(mark='zxb')]
	hsb_stocks = [s.code for s in get_mark_stocks(mark='hsb')]
	ssb_stocks = [s.code for s in get_mark_stocks(mark='ssb')]
	candidate_stocks = zxb_stocks + hsb_stocks + ssb_stocks
	print("total stock size:", len(candidate_stocks))

	for index, row in tqdm(pd_names.iterrows()):
		code = row['code']
		name = row['code_name']
		if stock_utils.is_jiucaiban(code):
			continue
		if code[3:] not in candidate_stocks:
			continue

		code_name = (code, name)
		df = stock_utils.read_data(code_name)
		df = df.head(n=len(df) - day_ago)  # n天前 新高/低入口
		df.reset_index(drop=True, inplace=True)
		if len(df) < 60:
			continue

		for period in [500, 120, 60, 20, 10, 5]:
			df = df.tail(n=period)
			df.reset_index(drop=True, inplace=True)
			idxMax = df['close'].idxmax(axis=0)
			idxMin = df['close'].idxmin(axis=0)
			# print(idxMax, idxMin)
			dateMax = df.iloc[idxMax]['date']
			dateMin = df.iloc[idxMin]['date']
			date = df.iloc[-1]['date']
			volume = df.iloc[-1]['volume']
			record_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
			d_period_inc = (df.iloc[-1]['close'] - df.iloc[0]['close']) / df.iloc[0]['close']

			volume_avg = df['volume'].sum() / period
			amount_avg = df['amount'].sum() / period
			period_inc_avg = d_period_inc / period
			extraJson = {'volume_avg': volume_avg, 'amount_avg': amount_avg, 'inc_avg': period_inc_avg}

			flag, direction = False, None
			r = Record(name, code, record_date, df.iloc[-1]['close'], "d{}".format(period), volume, d_period_inc)
			r.set_extra(json.dumps(extraJson))
			if df.iloc[-1]['date'] == dateMax:
				flag, direction = True, 'up'
			if df.iloc[-1]['date'] == dateMin and 'ST' not in name:
				flag, direction = True, 'down'

			if flag:
				r.set_direction(direction)
				records.append(r)

		# 涨停分析
		close = df.iloc[-1]['close']
		chg = df.iloc[-1]['pctChg']
		volume = df.iloc[-1]['volume']
		volume_rate = (volume - df.iloc[-2]['volume']) / df.iloc[-2]['volume']
		if float(chg) >= 9:
			chgs = [c for c in df['pctChg']]  # 涨幅序列
			vols = [v / df.iloc[0]['volume'] for v in df['volume']]  # 量比序列
			extraJson = {'volume_rate': volume_rate, 'chgs': chgs, 'vols': vols}
			r = Record(name, code, record_date, close, "d1", volume, chg)
			r.set_direction(direction='limit')
			r.set_extra(json.dumps(extraJson))
			records.append(r)
	return records


def update_records():
	records = gen_records(day_ago=0)
	if records:
		status = insert_records(records)
		print("update status: {}".format(status))
		return ConfigUtils.OK
	return ConfigUtils.EMPTY


def period_records():
	outResult = collections.defaultdict(dict)
	extraResult = collections.defaultdict(list)

	hsb = 1696
	ssb = 484
	zxb = 961

	HSB_NUM = 10
	SSB_NUM = 5
	ZXB_NUM = 5

	# 数据库获取沪、深、中小板
	zxb_stocks = [s.code for s in get_mark_stocks(mark='zxb')]
	hsb_stocks = [s.code for s in get_mark_stocks(mark='hsb')]
	ssb_stocks = [s.code for s in get_mark_stocks(mark='ssb')]
	candidate_stocks = zxb_stocks + hsb_stocks + ssb_stocks

	pool = {}
	bestStocks = []

	dt = get_recently_trade_date()

	new_highs = [r for r in get_records(dt=dt, direction='up', period='d500') if r.code[3:] in candidate_stocks]
	new_lows = [r for r in get_records(dt=dt, direction='down', period='d500') if r.code[3:] in candidate_stocks]

	pool['d60'] = get_records(dt=dt, direction='up', period='d60')
	pool['d20'] = get_records(dt=dt, direction='up', period='d20')
	pool['d10'] = get_records(dt=dt, direction='up', period='d10')
	pool['d5'] = get_records(dt=dt, direction='up', period='d5')

	for k, records in pool.items():
		hsb = [r for r in records if r.code[3:] in hsb_stocks][:HSB_NUM]
		ssb = [r for r in records if r.code[3:] in ssb_stocks][:SSB_NUM]
		zxb = [r for r in records if r.code[3:] in zxb_stocks][:ZXB_NUM]

		for r in hsb + ssb + zxb:
			bestStocks.append((r.code, r.name))

		outResult[k]['hsb'] = hsb
		outResult[k]['ssb'] = ssb
		outResult[k]['zxb'] = zxb

	#  近一周的新高股票
	day_week_ago = datetime.datetime.now() + datetime.timedelta(days=-7)
	target_date = day_week_ago.strftime('%Y-%m-%d')
	records = get_period_records(start_date=target_date)
	week_bests = []
	for r in records:
		if r.code[3:] not in candidate_stocks:
			continue
		week_bests.append((r.code, r.name))

	# print(collections.Counter(bestStocks))
	# best = sorted(collections.Counter(bestStocks).items(), key=lambda x: x[1], reverse=True)
	# print(best)  # [(('sh.600121', '郑州煤电'), 4), (('sh.601015', '陕西黑猫'), 4), (('sh.600418', '江淮汽车'), 4),...
	extraResult['best'] = sorted(collections.Counter(bestStocks).items(), key=lambda x: x[1], reverse=True)
	extraResult['week_best'] = sorted(collections.Counter(week_bests).items(), key=lambda x: x[1], reverse=True)
	extraResult['high'] = new_highs
	extraResult['low'] = new_lows

	# # 月线趋势选股
	# # 结构 [(('sh.600196', '复星医药'), 44517688035.19, 2269476415.0), (('sh.600887', '伊利股份'), 29118278005.35, 1554822026.0), ..]
	# breakstocks, highstocks = get_m_candidates()
	# extraResult['m_break'] = breakstocks
	# extraResult['m_high'] = highstocks

	send_hot_share_mail(outResult, extraResult)


def month_records():
	extraResult = collections.defaultdict(list)

	breakstocks, highstocks = get_m_candidates()
	extraResult['m_break'] = breakstocks
	extraResult['m_high'] = highstocks
	send_month_share_mail(extraResult)


def main(argv):
	mode = None
	try:
		opts, args = getopt.getopt(argv, "hm:", ["mode"])
	except getopt.GetoptError:
		print('inc.py -m <mode>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('inc.py -m <mode>')
			sys.exit()
		elif opt in ("-m", "--model"):
			mode = arg

	if mode == 'persist':
		print(update_records())

	if mode == 'record':
		period_records()

	if mode == 'month':
		month_records()


if __name__ == '__main__':
	main(sys.argv[1:])
