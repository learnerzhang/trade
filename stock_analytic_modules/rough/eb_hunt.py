#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/16 5:13 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : eb_hunt.py
# @Software: PyCharm
from sklearn.cluster import KMeans
import numpy as np
import json
import pandas as pd
from tqdm import tqdm

from common import stock_utils
from common.config import ConfigUtils
from common.sql_utils import get_records, get_mark_stocks


def normalization(data):
	_range = np.max(data) - np.min(data)
	return (data - np.min(data)) / _range


def standardization(data):
	mu = np.mean(data, axis=0)
	sigma = np.std(data, axis=0)
	return (data - mu) / sigma


def euclidean_dist(v1, v2):
	return np.sqrt(np.square(v1 - v2).sum())


def cosine_dist(v1, v2):
	return float(np.dot(v1, v2)) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def cluster():
	records = get_records(dt='2020-12-15', direction='limit', period='d1')
	print("zhangting num:", len(records))
	chgs = [json.loads(record.extra)['chgs'][:-1] for record in records]
	vols = [json.loads(record.extra)['vols'][:-1] for record in records]
	chgs = [standardization(c) for c in chgs]
	vols = [standardization(v) for v in vols]
	feats = [standardization(c) + standardization(v) for c, v in zip(chgs, vols)]
	kmeans = KMeans(n_clusters=5, random_state=0).fit(feats)

	print(kmeans.labels_)
	for label, record in sorted(zip(kmeans.labels_, records), key=lambda x: x[0]):
		print(label, record.name, record.code, json.loads(record.extra)['chgs'], json.loads(record.extra)['vols'])


def scan_stocks():
	pd_names = pd.read_csv(ConfigUtils.get_stock("STOCK_NAME"))
	# 数据库获取沪、深、中小板
	zxb_stocks = [s.code for s in get_mark_stocks(mark='zxb')]
	hsb_stocks = [s.code for s in get_mark_stocks(mark='hsb')]
	ssb_stocks = [s.code for s in get_mark_stocks(mark='ssb')]
	candidate_stocks = zxb_stocks + hsb_stocks + ssb_stocks
	print("total stock size:", len(candidate_stocks))

	records = get_records(dt='2020-12-15', direction='limit', period='d1')
	print("涨停数量:", len(records))
	for index, row in tqdm(pd_names.iterrows()):
		code = row['code']
		name = row['code_name']
		if stock_utils.is_jiucaiban(code):
			continue
		if code[3:] not in candidate_stocks:
			# print(name, code)
			continue

		code_name = (code, name)
		df = stock_utils.read_data(code_name)
		df.reset_index(drop=True, inplace=True)
		if len(df) < 60:
			continue

		df = df.tail(n=5)
		df.reset_index(drop=True, inplace=True)
		# 涨停分析
		close = df.iloc[-1]['close']
		chg = df.iloc[-1]['pctChg']
		volume = df.iloc[-1]['volume']
		volume_rate = (volume - df.iloc[-2]['volume']) / df.iloc[-2]['volume']
		chgs = [c for c in df['pctChg']]  # 涨幅序列
		vols = [v / df.iloc[0]['volume'] for v in df['volume']]  # 量比序列

		feat = standardization(chgs[:-1]) + standardization(vols[:-1])
		feat = standardization(chgs[:-1])
		# print(feat)
		tmp_count = 0
		for record in records:
			tmp_chg = json.loads(record.extra)['chgs'][:-1]
			tmp_vol = json.loads(record.extra)['vols'][:-1]
			tmp_feat = standardization(tmp_chg) + standardization(tmp_vol)
			tmp_feat = standardization(tmp_chg)
			dist = cosine_dist(feat, tmp_feat)
			if dist > 0.9:
				# print(name, record.name, chg, "sim:", dist)
				tmp_count += 1
		if tmp_count > 5:
			print(code, name, chg)


if __name__ == '__main__':
	# cluster()
	scan_stocks()
