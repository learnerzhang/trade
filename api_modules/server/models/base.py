from flask import current_app
from sqlalchemy import exc, Column, Integer, FLOAT, String, DateTime, create_engine, distinct, and_, PrimaryKeyConstraint
import datetime
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api_modules.server.utils.config import ConfigUtils
app = current_app

# 连接数据库
engine = create_engine(ConfigUtils.get_mysql('engine'), echo=False, pool_size=100, pool_recycle=3600)
# 基本类
Base = declarative_base()

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(session_factory)


class Fund(Base):
    __tablename__ = 'funds'
    __table_args__ = {"mysql_charset" : "utf8"}

    id = Column(Integer, primary_key=True)
    code = Column(String(40), unique=True)
    name = Column(String(40), unique=True)
    type = Column(String(20), default=None)
    scale = Column(FLOAT, default=None)
    positions = Column(String(20000), default=None)
    update_date = Column(DateTime, default=datetime.datetime.now)
    create_date = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, name=None, code=None, type=None, scale=None, positions=None):
        self.name = name
        self.code = code
        self.type = type
        self.scale = scale
        self.positions = positions
        self.update_date = datetime.date.today()
        self.create_date = datetime.date.today()

    def set_create_date(self, date):
        self.create_date = date

    def set_update_date(self, date):
        self.update_date = date

    def __repr__(self):
        return '<User %r %r %r %r %r>' % (self.code, self.name, self.type, self.positions, self.update_date)



class Share(Base):
    __tablename__ = 'shares'
    __table_args__ = {"mysql_charset" : "utf8"}
    
    id = Column(Integer, primary_key=True)
    code = Column(String(40), unique=True)
    name = Column(String(40), unique=False)
    industry = Column(String(40), unique=False, default=None)
    industryClassification = Column(String(40), unique=False, default=None)
    update_date = Column(DateTime, default=datetime.datetime.now)
    create_date = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, code=None, name=None, industry=None, industryClassification=None):
        self.name = name
        self.code = code
        self.industry = industry
        self.industryClassification = industryClassification
        self.update_date = datetime.date.today()
        self.create_date = datetime.date.today()
        
    def set_industry(self, industry):
        self.industry = industry

    def set_industryClassification(self, industryClassification):
        self.industryClassification = industryClassification

    def set_create_date(self, date):
        self.create_date = date

    def set_update_date(self, date):
        self.update_date = date

    def __repr__(self):
        return '<User %r %r %r %r %r>' % (self.code, self.name, self.industry, self.industryClassification, self.update_date)

    def serialize(self):
        return {"id": self.id, "code": self.code, "name": self.name, "industry": self.industry, "industryClassification": self.industryClassification, "update_date": str(self.update_date), "create_date": str(self.create_date), }


class Transaction(Base):
    __tablename__ = 'transactions'
    __table_args__ = (PrimaryKeyConstraint('date', 'code'),)

    code = Column(String(40), primary_key=False)
    date = Column(DateTime, default=datetime.datetime.now, primary_key=False)
    name = Column(String(40), unique=False)
    open = Column(FLOAT, default=None)
    high = Column(FLOAT, default=None)
    low = Column(FLOAT, default=None)
    close = Column(FLOAT, default=None)
    preclose = Column(FLOAT, default=None)
    volume = Column(FLOAT, default=None)
    amount = Column(FLOAT, default=None)
    adjustflag = Column(Integer, default=None)
    turn = Column(FLOAT, default=None)
    tradestatus = Column(FLOAT, default=None)
    change = Column(FLOAT, default=None)
    pctChg = Column(FLOAT, default=None)
    pbMRQ = Column(FLOAT, default=None)
    peTTM = Column(FLOAT, default=None)
    psTTM = Column(FLOAT, default=None)
    pcfNcfTTM = Column(FLOAT, default=None)
    isST = Column(Integer, default=None)
    type = Column(Integer, default=None)
    
    
    update_date = Column(DateTime, default=datetime.datetime.now)
    create_date = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.update_date = datetime.date.today()
        self.create_date = datetime.date.today()

    def build_from_dict(self, v):
        if not isinstance(v, dict):
            return
        self.code = v['code']
        self.open = v['open']
        self.high = v['high']
        self.low = v['low']
        self.close = v['close']
        self.preclose = v['preclose']
        self.volume = v['volume']
        self.amount = v['amount']
        self.adjustflag = v['adjustflag']
        self.turn = v['turn']
        self.tradestatus = v['tradestatus']
        self.change = self.high -self.low
        self.pctChg = v['pctChg']
        self.pbMRQ = v['pbMRQ']
        self.peTTM = v['peTTM']
        self.psTTM = v['psTTM']
        self.pcfNcfTTM = v['pcfNcfTTM']
        self.isST = v['isST']
        self.date = v['date']

    def set_type(self, type):
        self.type = type

    def set_adjustflag(self, adjustflag):
        self.adjustflag = adjustflag

    def set_turn(self, turn):
        self.turn = turn

    def set_tradestatus(self, tradestatus):
        self.tradestatus = tradestatus

    def set_pctChg(self, pctChg):
        self.pctChg = pctChg

    def set_pbMRQ(self, pbMRQ):
        self.pbMRQ = pbMRQ

    def set_peTTM(self, peTTM):
        self.peTTM = peTTM

    def set_psTTM(self, psTTM):
        self.psTTM = psTTM

    def set_pcfNcfTTM(self, pcfNcfTTM):
        self.pcfNcfTTM = pcfNcfTTM

    def set_create_date(self, date):
        self.create_date = date

    def set_update_date(self, date):
        self.update_date = date

    def serialize(self):
        return {
            "code": self.code,
            "name": self.name,
            "open": self.open,
            "close": self.close,
            "date": str(self.date),
            "high": self.high,
            "low": self.low,
            "preclose": self.preclose,
            "volume": self.volume*1.0/10000,
            "amount": self.amount*1.0/10000,
            "pctChg": self.pctChg,
            "change": self.change,
        }

    def __repr__(self):
        return '<User %r %r %r %r %r %r>' % (self.code, self.name, self.type, self.open, self.close, self.date)


class CalendarDate(Base):
    __tablename__ = 'calendar_dates'
    __table_args__ = {"mysql_charset" : "utf8"}

    id = Column(Integer, primary_key=True)
    is_trading_day = Column(Integer, unique=False)
    calendar_date = Column(DateTime, default=datetime.datetime.now, unique=True)
    update_flag = Column(Integer, default=0)
    update_date = Column(DateTime, default=datetime.datetime.now)
    create_date = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, calendar_date=None, is_trading_day=None):
        self.calendar_date = calendar_date
        self.is_trading_day = is_trading_day
        self.update_flag = 0
        self.update_date = datetime.date.today()
        self.create_date = datetime.date.today()

    def set_update_flag(self, update_flag):
        self.update_flag = update_flag

    def __repr__(self):
        return '<CalendarDate %r %r>' % (self.calendar_date, self.is_trading_day)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"mysql_charset" : "utf8"}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    cash = Column(FLOAT, default=None)
    password = Column(String(50), unique=False)
    email = Column(String(120), unique=True)
    update_date = Column(DateTime, default=datetime.datetime.now)
    create_date = Column(DateTime, default=datetime.datetime.now)
    

    def __init__(self, name=None, email=None, cash=500000):
        self.name = name
        self.email = email
        self.cash = cash
        self.update_date = datetime.date.today()
        self.create_date = datetime.date.today()

    def set_cash(self, cash):
        self.cash = cash

    def set_name(self, name):
        self.name = name

    def serialize(self,):
        return {
            'id': self.id,
            'name': self.name,
            'cash': self.cash
        }

    def __repr__(self):
        return '<User %r %r %r>' % (self.name, self.email, self.cash)

class Account(Base):
    __tablename__ = 'accounts'
    __table_args__ = {"mysql_charset" : "utf8"}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, default=None)
    code = Column(String(50), unique=False)
    code_name = Column(String(50), unique=False)
    price = Column(FLOAT, default=None)
    num = Column(Integer, default=None)
    date = Column(DateTime, default=datetime.datetime.now)
    flag = Column(Integer, default=0) # 1 买入, 2 卖出, 0 表示完成
    amount = Column(FLOAT, default=None)
    update_date = Column(DateTime, default=datetime.datetime.now)
    create_date = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, user_id=None, code=None,  code_name=None, price=None, num=None, amount=None, flag=0, date=None):
        self.user_id = user_id
        self.code = code
        self.code_name = code_name
        self.price = price
        self.num = num
        self.amount = amount
        self.flag = flag
        self.date = date
        self.update_date = datetime.date.today()
        self.create_date = datetime.date.today()
    
    def sell(self):
        self.flag = 0

    def __repr__(self):
        return '<User %r %r %r %r %r %r >' % (self.code, self.code_name, self.price, self.num, self.amount, self.flag)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'code': self.code,
            'code_name': self.code_name,
            'price': self.price,
            'num': self.num,
            'amount': self.amount,
            'flag': self.flag,
            'date': str(self.date),
        }


def init_db():
    """
    need create databases manual, init table schema auto by `flask init-db`
    :return:
    """
    Base.metadata.create_all(bind=engine)


def save_entity(entity):
    db_session.add(entity)
    try:
        db_session.commit()
        return True
    except exc.SQLAlchemyError:
        return False

def save_entities(entities):
    db_session.add_all(entities)
    try:
        db_session.commit()
        return True
    except exc.SQLAlchemyError:
        return False

def get_entity(cls, filters):
    return db_session.query(cls).filter(*filters).limit(1).all()

def update_entity():
    try:
        db_session.flush()
        return True
    except exc.SQLAlchemyError:
        return False

def get_entities(cls, filters, order):
    return db_session.query(cls).filter(*filters).order_by(order).all()

def get_dist_columns(cls, column):
    return db_session.query(distinct(column)).all()

def get_nums_by_filter(cls, filters):
    return db_session.query(cls).filter(*filters).count()

def get_entity_by_filter(cls, filters):
    return db_session.query(cls).filter(*filters).limit(1).all()

def get_entities_by_filter(cls, filters, offset, limit, order):
    return db_session.query(cls).filter(*filters).order_by(order).limit(limit).offset(offset).all()

def get_tbs_nums_by_filter(cls, join_cls, c1, c2, filters):
    return db_session.query(cls).join(join_cls, c1==c2).filter(*filters).count()

def get_tbs_entities_by_filter(cls, join_cls, c1, c2, filters, offset, limit, order):
    return db_session.query(cls).join(join_cls, c1==c2).filter(*filters).order_by(order).limit(limit).offset(offset).all()

def get_recently_trade_date(cur_date = datetime.date.today(), update_flag=1):
    return db_session.query(CalendarDate).filter(and_(CalendarDate.is_trading_day==1, CalendarDate.update_flag==update_flag, CalendarDate.calendar_date <= cur_date)).order_by(CalendarDate.calendar_date.desc()).limit(1).all()


if __name__ == "__main__":
    # init_db()
    r = get_recently_trade_date()
    print(r)