#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 4:27 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : m_hunt.py
# @Software: PyCharm
import pandas as pd
from tqdm import tqdm
import datetime
from common import stock_utils
from common.config import ConfigUtils
from common.entity import Record
from common.sql_utils import get_mark_stocks


def get_m_candidates():
	pd_names = pd.read_csv(ConfigUtils.get_stock("STOCK_NAME"))
	# 数据库获取沪、深、中小板
	zxb_stocks = [s.code for s in get_mark_stocks(mark='zxb')]
	hsb_stocks = [s.code for s in get_mark_stocks(mark='hsb')]
	ssb_stocks = [s.code for s in get_mark_stocks(mark='ssb')]
	candidate_stocks = zxb_stocks + hsb_stocks + ssb_stocks
	print("total stock size:", len(candidate_stocks))

	t_date = datetime.date.today().strftime('%Y-%m')
	break_stocks = list()
	high_stocks = list()
	for index, row in tqdm(pd_names.iterrows()):
		code = row['code']
		name = row['code_name']
		if stock_utils.is_jiucaiban(code):
			continue
		if code[3:] not in candidate_stocks:
			continue

		code_name = (code, name)
		df = stock_utils.read_data(code_name, root=ConfigUtils.get_stock("DATA_M_DIR"))
		if df is None or len(df) < 2:
			continue
		df = df.tail(n=12)  # n天前 新高/低入口
		df.reset_index(drop=True, inplace=True)
		close_df = df.sort_values(by='close', ascending=False)
		volume_df = df.sort_values(by='volume', ascending=False)
		amount_df = df.sort_values(by='amount', ascending=False)
		pctChg_df = df.sort_values(by='pctChg', ascending=False)

		idxCloseMax0, idxCloseMax1 = close_df.index[0], close_df.index[1]
		idxVolMax0, idxVolMax1 = volume_df.index[0], volume_df.index[1]
		idxAmountMax0, idxAmountMax1 = amount_df.index[0], amount_df.index[1]
		idxChgMax0, idxChgMax1 = pctChg_df.index[0], pctChg_df.index[1]

		volMax0, volMax1 = df.iloc[idxVolMax0]['volume'], df.iloc[idxVolMax1]['volume']
		pctMax0, pctMax1 = df.iloc[idxChgMax0]['pctChg'], df.iloc[idxChgMax1]['pctChg']

		closeMax0, closeMax1 = df.iloc[idxCloseMax0]['close'], df.iloc[idxCloseMax1]['close']
		date0, date1 = df.iloc[idxCloseMax0]['date'], df.iloc[idxCloseMax1]['date']
		pch0, pch1 = df.iloc[idxCloseMax0]['pctChg'], df.iloc[idxCloseMax1]['pctChg']
		amount0, amount1 = df.iloc[idxCloseMax0]['amount'], df.iloc[idxCloseMax1]['amount']
		# 经过3个月洗盘, 最近股价将赶超新高
		if t_date == date1 and (idxCloseMax1 - idxCloseMax0) > 2:
			# print(code_name, volMax1, date0, date1, idxVolMax0, idxChgMax0, idxCloseMax0, closeMax0)
			r = Record(name, code, t_date, closeMax1, 'm', amount1, pch1)
			break_stocks.append(r)
		# 持续新高
		if t_date == date0:
			# print(code_name, dateMax0, dateMax1, idxVolMax0, idxChgMax0, idxCloseMax0, closeMax0)
			r = Record(name, code, t_date, closeMax0, 'm', amount0, pch0)
			high_stocks.append(r)

	break_stocks = sorted(break_stocks, key=lambda x: x.volume, reverse=True)
	high_stocks = sorted(high_stocks, key=lambda x: x.volume, reverse=True)

	# print(break_stocks[:30])
	# print(high_stocks[:30])

	break_stocks = [r for r in break_stocks if r.volume < 5e11]
	high_stocks = [r for r in high_stocks if r.volume < 90081936793]

	return break_stocks, high_stocks


if __name__ == '__main__':
	bs, hs = get_m_candidates()
	print(bs)
	print(hs)
