#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 7:08 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : sina_reptile.py
# @Software: PyCharm
import requests
import json

from data_modules.model import RealTrade

STOCK_REAL_URL = 'http://hq.sinajs.cn/list={}'
STOCK_PERIOD_URL = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={}&scale={}&ma=no&datalen=1023'


def get_real_price(code):
	url = STOCK_REAL_URL.format(code)
	# print("real url:", url)
	resp = requests.get(url)
	if resp.status_code == 200:
		real_str = resp.text
		parts = real_str.strip().split('=')
		if len(parts) < 2:
			return
		hq_str = parts[0]
		list_str = parts[1][1:-2]
		tokes = list_str.split(',')
		return RealTrade(tokes)


def get_mark_data(code, scale):
	"""
	:param code: [市场][股票代码]
	:param scale: 5、10、30、60分钟
	:return: day日期、open开盘价、high最高价、low最低价、close收盘价、volume成交量
	"""
	url = STOCK_PERIOD_URL.format(code, scale)
	print("mark url:", url)
	resp = requests.get(url)
	if resp.status_code == 200:
		json_str = resp.text
		return json.loads(json_str)
	else:
		return None


if __name__ == '__main__':
	rt = get_real_price('sh600006')
	print(rt)
	#
	# rt = get_mark_data('sh600006', scale='5')
	# print(rt)
