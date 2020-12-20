#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 12:56 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : helper.py.py
# @Software: PyCharm
import numpy as np


def moving_average(ts, win):
	return np.convolve(ts, np.ones(win) / win, 'valid')


def rmse(y, y_hat):
	"""
	返回预测序列相对于真值序列的标准差。
	Args:
		y:
		y_hat:
	Returns:
	"""
	return np.sqrt(np.mean(np.square(y - y_hat)))


def slope(df, err):
	"""返回直线斜率。如果拟合误差大于err，则抛出异常
	"""
	# 对ts进行归一化，以便斜率可以在不同的时间序列之间进行比较
	assert df[0] != 0

	df = df / df[0]
	x = np.arange(len(df))
	z = np.polyfit(x, df, deg=1)
	p = np.poly1d(z)

	df_hat = np.array([p(xi) for xi in x])
	error = rmse(df, df_hat) / np.sqrt(np.mean(np.square(df)))
	if error >= err:
		raise ValueError("can not fit into line")
	return z[0]
