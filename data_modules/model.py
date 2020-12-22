#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 7:24 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : model.py
# @Software: PyCharm


class RealTrade(object):

	def __init__(self, tradelists):
		self.name = tradelists[0]
		self.open = tradelists[1]
		self.preclose = tradelists[2]
		self.price = tradelists[3]
		self.high = tradelists[4]
		self.low = tradelists[5]
		self.jbuy = tradelists[6]
		self.jsell = tradelists[7]
		self.volume = tradelists[8]  # 股, 100股为手
		self.amount = tradelists[9]
		self.buy_volume1 = tradelists[10]  # 股, 100股为手
		self.buy_price1 = tradelists[11]
		self.buy_volume2 = tradelists[12]
		self.buy_price2 = tradelists[13]
		self.buy_volume3 = tradelists[14]
		self.buy_price3 = tradelists[15]
		self.buy_volume4 = tradelists[16]
		self.buy_price4 = tradelists[17]
		self.buy_volume5 = tradelists[18]
		self.buy_price5 = tradelists[19]

		self.sell_volume1 = tradelists[20]
		self.sell_price1 = tradelists[21]
		self.sell_volume2 = tradelists[22]
		self.sell_price2 = tradelists[23]
		self.sell_volume3 = tradelists[24]
		self.sell_price3 = tradelists[25]
		self.sell_volume4 = tradelists[26]
		self.sell_price4 = tradelists[27]
		self.sell_volume5 = tradelists[28]
		self.sell_price5 = tradelists[29]

		self.date = tradelists[30]
		self.time = tradelists[31]
		self.extra = tradelists[32:]

		self.pctChg = round((float(self.price) - float(self.preclose)) / float(self.preclose), 3)

	def __repr__(self):
		bsInfo = "[S({}-{}), ({}-{}), ({}-{}), ({}-{}), ({}-{}); B({}-{}), ({}-{}), ({}-{}), ({}-{}), ({}-{})]"\
			.format(self.sell_price5, self.sell_volume5,
					self.sell_price4, self.sell_volume4,
					self.sell_price3, self.sell_volume3,
					self.sell_price2, self.sell_volume2,
					self.sell_price1, self.sell_volume1,
					self.buy_price1, self.buy_volume1,
					self.buy_price2, self.buy_volume2,
					self.buy_price3, self.buy_volume3,
					self.buy_price4, self.buy_volume4,
					self.buy_price5, self.buy_volume5)
		return "<RealTrade(name='%s', date='%s', time='%s', price='%s', pctChg='%s', volume=%s, amount=%s, bsInfo='%s'>" % (
			self.name, self.date, self.time, self.price, self.pctChg, self.volume, self.amount, bsInfo)
