#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/11/29 11:13 上午
# @Author  : zhangzhen12
# @Site    : 
# @File    : position_reptile.py
# @Software: PyCharm
from datetime import timedelta, datetime, date
import pandas as pd
import pprint
import csv
import codecs
import time
import requests
from bs4 import BeautifulSoup
import json
import sys
import os
from common.stock_utils import get_trade_dates
from common.config import ConfigUtils

# 个股持仓变动
stock_detail_url = "http://cwzx.shdjt.com/gpdmgd.asp?gpdm={}"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'


def reptile_position(code='600600'):
	url = stock_detail_url.format(code)
	request = requests.session()
	headers = {
		'User-Agent': user_agent,
		'Content-Type': 'application/json',
		'Cookie': '__gads=ID=f765be925ab2e761-22bd873789c400ba:T=1604461526:RT=1604461526:S=ALNI_MaZ36qmxjUzfmO-uB_UuVoveArNYA; Hm_lvt_8d618eb1a2f508d97c6366877d94a494=1604461526,1606616899; Hm_lvt_21824589dcdcfa175a9ffe2cdd908b30=1604461526,1606616899; ASPSESSIONIDQAQBBASD=GEHLECHBOPKAPGABMOENFDEC; Hm_lvt_c63de846e8823f696db1d63ebb9065f3=1606616982; Hm_lpvt_c63de846e8823f696db1d63ebb9065f3=1606619374; Hm_lpvt_21824589dcdcfa175a9ffe2cdd908b30=1606619701; Hm_lpvt_8d618eb1a2f508d97c6366877d94a494=1606619701'
	}
	req = request.post(url, headers=headers)
	print("req url:", url)

	if req.status_code == 200:
		return req.text
	else:
		return None


def parse_position_change(code='600600'):
	if not os.path.exists(ConfigUtils.get_stock("POS_DIR")):
		os.mkdir(ConfigUtils.get_stock("POS_DIR"))

	pos_path = os.path.join(ConfigUtils.get_stock("POS_DIR"), "position_{}.csv".format(code))

	html = reptile_position(code=code)
	html = (html.replace('<br>', '')).replace('<br/>', '')

	soup = BeautifulSoup(html, 'lxml')  # html.parser是解析器，也可是lxml
	# print(soup.prettify())
	inner = soup.select('table[class="tb0td1"]')
	if len(inner) > 0:
		tr_rows = inner[0].select('tr[height]')

		tb_head = tr_rows[0].select('td')
		heads = [ct.text for ct in tb_head]
		# print(heads)

		content = []
		for row in tr_rows[1:]:
			cols = row.select('td')
			tmp_rows = []
			for ct in cols:
				[s.extract() for s in ct(['a', 'br'])]
				tmp_rows.append(ct.text.replace('\n', '').replace('\r', ''))
			# print(tmp_rows)
			content.append(tmp_rows)

		with open(pos_path, mode="ab+") as csvfile:
			csvfile.write(codecs.BOM_UTF8)

		with open(pos_path, 'a+', newline='', encoding='utf-8') as csvfile:
			writer = csv.writer(csvfile)
			# 先写入columns_name
			writer.writerow(heads)
			# 写入多行用writerows
			writer.writerows(content)


def reptile_dc():
	pd_names = pd.read_csv(ConfigUtils.get_stock("STOCK_NAME"))
	codes = set([row['code'][3:] for index, row in pd_names.iterrows()])
	for code in codes:
		parse_position_change(code)


if __name__ == '__main__':
	reptile_dc()
