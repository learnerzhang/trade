#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/11 4:10 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : sql_utils.py
# @Software: PyCharm
from operator import and_

import sqlalchemy
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
import sys, getopt
import pprint
from common.entity import Base, Stock, Block, BlockStock, Record
from data_modules.ths_reptile import init_q_stocks, reptile_blocks, reptile_block_stocks
from common.config import ConfigUtils

engine = create_engine('sqlite:////Users/zhangzhen12/data/share.db?check_same_thread=False', echo=True)


def init_db():  # 初始化表
	# drop_db()
	Base.metadata.create_all(engine)


def drop_db():  # 删除表
	Base.metadata.drop_all(engine)


def init_blocks():
	blocks = reptile_blocks()
	Session = sessionmaker(engine)
	db_session = Session()
	for block in blocks:
		try:
			tmp_block = db_session.query(Block).filter(Block.name == block.name, Block.code == block.code).first()
			if tmp_block:
				tmp_block.set_name(block.name)
			else:
				db_session.add(block)
			db_session.commit()
		except IOError:
			db_session.rollback()
			print("Error Constraint.", block)
	print("init block success.")


def init_stocks():
	stocks = init_q_stocks()
	Session = sessionmaker(engine)
	db_session = Session()
	for stock in stocks:
		try:
			tmp_block = db_session.query(Stock).filter(Stock.code == stock.code).first()
			if tmp_block:
				tmp_block.set_name(stock.name)
			else:
				db_session.add(stock)
			db_session.commit()
		except IOError:
			db_session.rollback()
			print("Error Constraint.", stock)
	print("init stock success.")


def init_block_stocks():
	Session = sessionmaker(engine)
	db_session = Session()

	block2stocks = reptile_block_stocks()
	for block_code, stocks in block2stocks.items():
		tmp_block = db_session.query(Block).filter(Block.code == block_code).first()
		# 版块不存在
		if tmp_block is None:
			continue

		for stock in stocks:
			try:
				tmp_stock = db_session.query(Stock).filter(Stock.code == stock.code).first()
				if tmp_stock is None:
					continue
				bs = BlockStock(b_id=tmp_block.id, s_id=tmp_stock.id)

				tmp_bs = db_session.query(BlockStock)\
					.filter(BlockStock.block_id == bs.block_id, BlockStock.stock_id == bs.stock_id)\
					.first()
				# b-s 映射
				if tmp_bs:
					continue
				db_session.add(bs)
				db_session.commit()
			except IOError:
				db_session.rollback()
				print("Error Constraint.")


def query_stocks():
	Session = sessionmaker(engine)
	db_session = Session()

	blocks = db_session.query(Block).all()
	print(len(blocks))
	for block in blocks:
		print(block)

	blocks = db_session.query(Block).filter(Block.name == '拼多多概念').all()
	print(len(blocks))
	for block in blocks:
		# print(block)
		pass

	stocks = db_session.query(Stock).all()
	print(len(stocks))
	for stock in stocks:
		# print(stock)
		pass

	block_stocks = db_session.query(BlockStock).all()
	print(len(block_stocks))
	for b_s in block_stocks:
		print(b_s)
		pass


def get_stocks():
	Session = sessionmaker(engine)
	db_session = Session()

	try:
		stocks = db_session.query(Stock).all()
		return stocks
	except IOError:
		return []
	finally:
		db_session.close()


def get_mark_stocks(mark='zxb'):
	Session = sessionmaker(engine)
	db_session = Session()

	try:
		stocks = db_session.query(Stock).filter(Stock.mark == mark).all()
		return stocks
	except IOError:
		return []
	finally:
		db_session.close()


def get_records(dt='2020-12-11', direction='up', period='d20', **kwargs):
	Session = sessionmaker(engine)
	db_session = Session()
	records = db_session.query(Record).filter(Record.date == dt, Record.direction == direction, Record.period == period) \
		.order_by(Record.change.desc()).all()
	# print(records)
	# pprint.pprint(records)
	return records


def get_period_records(start_date, end_date='2022-12-11', direction='up', period='d500'):
	Session = sessionmaker(engine)
	db_session = Session()
	records = db_session \
		.query(Record) \
		.filter(and_(Record.date < end_date, Record.date >= start_date), Record.direction == direction,
				Record.period == period) \
		.order_by(Record.change.desc()) \
		.all()
	# pprint.pprint(records)
	return records


def insert_records(records):
	if records:
		Session = sessionmaker(engine)
		db_session = Session()
		for r in records:
			try:
				tmp_record = db_session.query(Record) \
					.filter(Record.date == r.date, Record.period == r.period, Record.code == r.code).first()
				if tmp_record:
					tmp_record.set_extra(r.extra)
				else:
					db_session.add(r)
				db_session.commit()
			except IOError:
				db_session.rollback()
				print("Error Constraint.", r)
	return ConfigUtils.OK


def main(argv):
	mode = None
	try:
		opts, args = getopt.getopt(argv, "hm:", ["mode"])
	except getopt.GetoptError:
		print('sql_utils.py -m <mode>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('sql_utils.py -m <mode>')
			sys.exit()
		elif opt in ("-m", "--model"):
			mode = arg

	if mode == 'drop':
		drop_db()
	if mode == 'db':
		init_db()
	if mode == 'init-blocks':
		init_blocks()
	if mode == 'init-stocks':
		init_stocks()
	if mode == 'init-bs':
		init_block_stocks()
	if mode == 'demo':
		query_stocks()
	if mode == 'record':
		# records = get_records(period='d500')
		# pprint.pprint(records)
		# records = get_period_records(start_date='2020-12-07')
		# pprint.pprint(records)
		records = get_records(dt='2020-11-18', direction='limit', period='d1')
		pprint.pprint(records)
		print(len(records))


if __name__ == '__main__':
	main(sys.argv[1:])
