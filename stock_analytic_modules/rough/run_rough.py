#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 3:58 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : run_rough.py
# @Software: PyCharm
import getopt
import sys

from stock_analytic_modules.rough.inc import update_records, period_records


def main(argv):
	mode = None
	try:
		opts, args = getopt.getopt(argv, "hm:", ["mode"])
	except getopt.GetoptError:
		print('run_rough.py -m <mode:report/persist>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('run_rough.py -m <mode>')
			sys.exit()
		elif opt in ("-m", "--model"):
			mode = arg

	# 定时持久化
	if mode == 'persist':
		update_records()

	# 定时发送邮箱
	if mode == 'report':
		period_records()


if __name__ == '__main__':
	main(sys.argv[1:])
