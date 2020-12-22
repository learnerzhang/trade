#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/12/11 4:24 下午
# @Author  : zhangzhen12
# @Site    : 
# @File    : entity.py
# @Software: PyCharm
from flask_sqlalchemy import Model
from sqlalchemy import Column, Integer, FLOAT, String, Table, ForeignKey, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc, Column, Integer, FLOAT, String, DateTime, create_engine, distinct, and_, \
	PrimaryKeyConstraint
import datetime

from sqlalchemy.orm import relationship, backref

Base = declarative_base()


# 定义映射类User，其继承上一步创建的Base
class Block(Base):
	__tablename__ = 'block'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(128), unique=True)
	code = Column(String(20), unique=True)
	url = Column(String(128), unique=True)
	# many to many block <-> stock
	date = Column(Date)
	update_date = Column(DateTime, default=datetime.datetime.now)
	create_date = Column(DateTime, default=datetime.datetime.now)

	def __init__(self, name, code, date, url):
		self.url = url
		self.date = date
		self.code = code
		self.name = name

	def set_name(self, name):
		self.name = name

	def __hash__(self):
		return hash(self.code + self.name)

	def __repr__(self):
		return "<Block(id='%s',name='%s', code='%s', date='%s', url='%s')>" % (self.id,
																			   self.name, self.code,
																			   self.date, self.url,)


class Stock(Base):
	__tablename__ = 'stock'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(128))
	code = Column(String(20), unique=True)
	mark = Column(String(20))
	update_date = Column(DateTime, default=datetime.datetime.now)
	create_date = Column(DateTime, default=datetime.datetime.now)

	def __init__(self, name, code, mark):
		self.name = name
		self.code = code
		self.mark = mark

	def set_name(self, name):
		self.name = name

	def __hash__(self):
		return hash(self.code + self.name)

	def __repr__(self):
		return "<Block(id='%s', name='%s', code='%s')>" % (self.id, self.name, self.code)


class BlockStock(Base):
	__tablename__ = 'block_stock'
	id = Column(Integer, primary_key=True, autoincrement=True)
	block_id = Column(Integer, ForeignKey('block.id'))
	stock_id = Column(Integer, ForeignKey('stock.id'))
	UniqueConstraint(block_id, stock_id)

	def __init__(self, b_id, s_id):
		self.stock_id = s_id
		self.block_id = b_id

	def __repr__(self):
		return "<BlockStock(id='%s', block_id='%s', stock_id='%s', flag='%s'>" % (
			self.id, self.block_id, self.stock_id, self.flag)


class Record(Base):
	__tablename__ = 'record'
	id = Column(Integer, primary_key=True, autoincrement=True)
	name = Column(String(128))
	code = Column(String(20))
	date = Column(Date)
	period = Column(String(5))  # 5d, 10d, 20d, 30d, 60d, 100d, 200d, 500d
	direction = Column(String(5))  # up, down
	price = Column(FLOAT)  # 价
	volume = Column(FLOAT)  # 量
	change = Column(FLOAT)  # 增幅
	extra = Column(String(256))
	update_date = Column(DateTime, default=datetime.datetime.now)
	create_date = Column(DateTime, default=datetime.datetime.now)
	UniqueConstraint(code, date, period)

	def __init__(self, name, code, date, price, period, volume, change):
		self.name = name
		self.code = code
		self.date = date
		self.price = price
		self.period = period
		self.volume = volume
		self.change = change

	def set_direction(self, direction):
		self.direction = direction

	def set_extra(self, extra):
		self.extra = extra

	def __hash__(self):
		return hash(self.code + self.name + str(self.date))

	def __repr__(self):
		return "<Record(id='%s', date='%s', name='%s', code='%s', " \
			   "price='%s', period='%s', direction='%s', change='%s', " \
			   "volume='%s', extra='%s')>" % (
			   self.id, self.date, self.name, self.code, self.price, self.period, self.direction, self.change,
			   self.volume, self.extra)
