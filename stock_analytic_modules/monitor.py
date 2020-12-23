#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 2:18 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : monitor.py
# @Software: PyCharm
from data_modules.sina_reptile import get_real_price
from stock_analytic_modules.utils.helper import get_before_day
from common.sql_utils import get_records, get_mark_stocks
from common.stock_utils import get_recently_trade_date
import datetime
import threading
from time import ctime, sleep

dt = get_before_day(ago=1)
# print(dt)
# 数据库获取沪、深、中小板
zxb_stocks = [s.code for s in get_mark_stocks(mark='zxb')]
hsb_stocks = [s.code for s in get_mark_stocks(mark='hsb')]
ssb_stocks = [s.code for s in get_mark_stocks(mark='ssb')]
candidate_stocks = zxb_stocks + hsb_stocks + ssb_stocks


def monitor_low():
	new_lows = [r for r in get_records(dt=dt, direction='down', period='d500') if r.code[3:] in candidate_stocks]
	print("low:", len(new_lows))
	while True:
		sleep(10)
		for r in new_lows:
			code = str(r.code).replace('.', '')
			rt = get_real_price(code)
			if float(rt.pctChg) > 0.05:
				print("[LOW]", rt)
		print("[LOW] loop done.")


def monitor_high():
	new_highs = [r for r in get_records(dt=dt, direction='up', period='d500') if r.code[3:] in candidate_stocks]
	print("high:", len(new_highs))

	while True:
		for r in new_highs:
			code = str(r.code).replace('.', '')
			rt = get_real_price(code)
			if float(rt.pctChg) > 0.06:
				print("[HIGH]", rt)
		print("[HIGH] loop done.")
		sleep(10)


def monitor_change():
	d60 = get_records(dt=dt, direction='up', period='d60')
	d20 = get_records(dt=dt, direction='up', period='d20')
	d10 = get_records(dt=dt, direction='up', period='d10')
	d5 = get_records(dt=dt, direction='up', period='d5')
	codes = set([r.code for r in d60 + d20 + d10 + d5])

	while True:
		for code in codes:
			code = str(code).replace('.', '')
			rt = get_real_price(code)
			if float(rt.pctChg) < -0.06:
				print("[Change]", rt)
		print("[Change] loop done.")
		sleep(10)


if __name__ == '__main__':
	t1 = threading.Thread(target=monitor_low, args=())
	t2 = threading.Thread(target=monitor_high, args=())
	t3 = threading.Thread(target=monitor_change, args=())
	t1.start()
	t2.start()
	t3.start()
	t1.join()
	t2.join()
	t3.join()
	print("all over %s" % ctime())

