#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/28 9:41 上午
# @Author  : zhangzhen12
# @Site    : 
# @File    : foreign_capital.py
# @Software: PyCharm
from datetime import timedelta, datetime, date
import pandas as pd
import pprint
import csv
import codecs
import time
import requests
import json
import os
from common.stock_utils import get_trade_dates
from common.config import ConfigUtils

wzcg_url = 'http://www.waizichigu.com/Handler/Handler2.ashx?code=&updatetime={}&page={}&rows={}'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'


def post_wzcg(date, url=wzcg_url, page=1, rows=20):
	request = requests.session()
	headers = {
		'User-Agent': user_agent,
		'Content-Type': 'application/json',
		'Host': 'www.waizichigu.com',
		'Origin': 'http://www.waizichigu.com',
		'Referer': 'http://www.waizichigu.com/RankingPage',
		'Cookie': 'UM_distinctid=1740af6145bc99-030ada2304d509-31677305-1fa400-1740af6145c33b; CNZZDATA1279058265=378897155-1597907945-%7C1606526468'
	}
	url = url.format(str(date), page, rows)
	req = request.post(url, headers=headers)
	print("req params:", url)

	if req.status_code == 200:
		return json.loads(req.text)
	else:
		return None


def get_foreign_num(date=date.today() + timedelta(-1)):
	rs = post_wzcg(date)
	if rs and 'total' in rs:
		return rs['total']
	else:
		return -1


def reptile_dynamic_wz():
	wz_path = os.path.join(ConfigUtils.get_stock("DATA"), "wz_top_20.csv")
	url = 'http://www.waizichigu.com/Handler/Handler6.ashx'
	rs = post_wzcg(None, url=url)
	if rs:
		pprint.pprint(rs)
		df = pd.DataFrame(rs)
		df.to_csv(wz_path, index=None, mode='w+')


def reptile_by_date(trade_date=date.today() + timedelta(-1), size=50, ):
	if not os.path.exists(ConfigUtils.get_stock("WZ_DIR")):
		os.mkdir(ConfigUtils.get_stock("WZ_DIR"))

	wz_path = os.path.join(ConfigUtils.get_stock("WZ_DIR"), "wz_{}.csv".format(str(trade_date)))
	total = get_foreign_num(trade_date)
	print("total:", total)
	if total > 0:
		df = pd.DataFrame()
		for i in range(0, int((total + size - 1) / size)):
			outJson = post_wzcg(trade_date, page=(i + 1), rows=size)
			print(outJson)
			if outJson and "rows" in outJson:
				row = pd.DataFrame(outJson['rows'])
				df = df.append(row, ignore_index=True)
				time.sleep(1)
		df.to_csv(wz_path, index=None, mode='w+')


def reptile_wz():
	end = date.today() + timedelta(-1)
	tdates = get_trade_dates(start='2019-03-20', end=str(end))
	for d in tdates:
		reptile_by_date(trade_date=d)


if __name__ == '__main__':
	today = date.today()
	print(today)
	# get_foreign_num()
	# reptile_by_date()
	# reptile_dynamic_wz()
	reptile_wz()
