#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/11 6:08 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : ths_reptile.py
# @Software: PyCharm
from datetime import timedelta, datetime, date
import pandas as pd
import pprint
import csv
import codecs
import collections
import time
import re
import requests
import datetime
from bs4 import BeautifulSoup
import json
import sys
import os

from common.entity import Block, Stock
from common.stock_utils import get_trade_dates
from common.config import ConfigUtils

block_url = "http://q.10jqka.com.cn/gn/index/field/addtime/order/desc/page/{}/ajax/1/"
stock_url = "http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{}/ajax/1/code"

zxb_url = "http://q.10jqka.com.cn/index/index/board/zxb/field/zdf/order/desc/page/{}/ajax/1/"
hsb_url = "http://q.10jqka.com.cn/index/index/board/hs/field/zdf/order/desc/page/{}/ajax/1/"
ssb_url = "http://q.10jqka.com.cn/index/index/board/ss/field/zdf/order/desc/page/{}/ajax/1/"

block_stocks_url = "http://q.10jqka.com.cn/gn/detail/field/264648/order/desc/page/{}/ajax/1/code/"

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
cookie = 'searchGuide=sg; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1607586976; spversion=20130314; user=MDq358fh1Ma1rVlQbTo6Tm9uZTo1MDA6NDQ2NzA4NzM0OjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI1Ojo6NDM2NzA4NzM0OjE2MDc2NzA1Nzk6OjoxNTE4MTUxMTQwOjYwNDgwMDowOjFiYjlmY2QxZDNmNTBjMTVjMzRhOWVjMDgzZWEwZWI0YzpkZWZhdWx0XzQ6MQ%3D%3D; userid=436708734; u_name=%B7%E7%C7%E1%D4%C6%B5%ADYPm; escapename=%25u98ce%25u8f7b%25u4e91%25u6de1YPm; ticket=9b0bcbe740bc3ca34e130ef8320e03b6; user_status=0; __utma=156575163.2035611393.1607676715.1607676715.1607676715.1; __utmc=156575163; __utmz=156575163.1607676715.1.1.utmcsr=10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1607676824; historystock=002571%7C*%7C002594; v=AjGDlx6QyhP4emYH0sCPzb7mRrbIHqWWT5JJnhNGLfgXOl9gW261YN_iWgWg'


def reptile_req(url):
	request = requests.session()
	headers = {
		'User-Agent': user_agent,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Cookie': cookie,
		'Connection': 'keep-alive',
		'DNT': '1',
		'Cache-Control': 'max-age=60',
		'Host': 'q.10jqka.com.cn'
	}
	req = request.get(url, headers=headers)
	print("req url:", url)

	if req.status_code == 200:
		return req.text
	else:
		return None


def reptile_blocks():
	rs_blocks = []

	page = 1
	total_page = page
	while page <= total_page:
		time.sleep(5)
		url = block_url.format(page)
		outHtml = reptile_req(url)
		if outHtml is None:
			time.sleep(5)
			continue
		# print(outHtml)
		html = (outHtml.replace('<br>', '')).replace('<br/>', '')
		soup = BeautifulSoup(html, 'lxml')  # html.parser是解析器，也可是lxml
		inner = soup.select('tr')
		page_info = soup.select('span[class="page_info"]')

		if page_info:
			p_info = page_info[0].text
			total_page = int(p_info.split('/')[1])
		print("page {}/{}".format(page, total_page))

		for row in inner[1:]:
			cols = row.select('td')
			if len(cols) < 4:
				continue
			block_date = cols[0].text
			block_date = datetime.datetime.strptime(block_date, '%Y-%m-%d').date()

			block_name = cols[1].text

			block_stock_url = None
			block_code = None
			a_elems = cols[1].select('a')
			if a_elems:
				block_stock_url = a_elems[0].get('href')
				pattern = re.compile(r'http://q.10jqka.com.cn/gn/detail/code/(\d+)/')
				results = pattern.findall(block_stock_url)
				if results:
					block_code = results[0]
			print(block_date, block_name, block_code, block_stock_url)

			rs_blocks.append(Block(block_name, block_code, block_date, block_stock_url))
		page += 1
		# break
	return rs_blocks


def reptile_stock(ori_url, mark=None,):
	rs_stocks = []
	page = 1
	total_page = page
	while page <= total_page:
		time.sleep(3)
		url = ori_url.format(page)
		outHtml = reptile_req(url)
		if outHtml is None:
			time.sleep(5)
			continue
		# print(outHtml)
		html = (outHtml.replace('<br>', '')).replace('<br/>', '')
		soup = BeautifulSoup(html, 'lxml')  # html.parser是解析器，也可是lxml
		inner = soup.select('tr')
		page_info = soup.select('span[class="page_info"]')

		if page_info:
			p_info = page_info[0].text
			total_page = int(p_info.split('/')[1])
		print("page {}/{} {}/{}".format(page, total_page, mark, url))

		for row in inner[1:]:
			cols = row.select('td')
			if len(cols) < 14:
				continue
			s_code = cols[1].text
			s_name = cols[2].text
			s_price = cols[3].text
			s_change_per = cols[4].text
			s_change_size = cols[5].text
			s_turn = cols[7].text
			s_volume_rate = cols[8].text
			s_amp = cols[9].text
			s_amount = cols[10].text
			s_flow = cols[11].text
			s_flow_value = cols[12].text
			s_pe = cols[13].text
			# print(s_code, s_name, s_price, s_change_per, s_change_size, s_turn, s_volume_rate, s_amp, s_amount, s_flow, s_flow_value, s_pe)
			stock = Stock(s_name, s_code, mark=mark)
			# print(mark, page, stock)
			rs_stocks.append(stock)
		page += 1
	# break
	return rs_stocks


def init_q_stocks():
	zx_stocks = reptile_stock(ori_url=zxb_url, mark='zxb')
	hs_stocks = reptile_stock(ori_url=hsb_url, mark='hsb')
	ss_stocks = reptile_stock(ori_url=ssb_url, mark='ssb')
	return zx_stocks + hs_stocks + ss_stocks


def reptile_block_stocks():
	block2stocks = collections.defaultdict(list)
	blocks = reptile_blocks()
	for block in blocks:
		url = block_stocks_url + block.code
		stocks = reptile_stock(ori_url=url)
		block2stocks[block.code] = stocks
	return block2stocks


if __name__ == '__main__':
	# reptile_blocks()
	reptile_block_stocks()
	pass
