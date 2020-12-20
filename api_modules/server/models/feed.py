import logging
import datetime
import backtrader as bt

from typing import Iterator, List, Tuple
from sqlalchemy.engine import Engine, create_engine

log = logging.getLogger(__name__)


class DBDataFeed(bt.feed.DataBase):
    symbol: str
    historical_eod: Iterator
    engine: Engine = None

    params = (
        ("dataname", None),
        ("fromdate", datetime.date(2010, 1, 1)),
        ("todate", datetime.date(2050, 1, 1)),
        ("compression", 1),
        ("timeframe", bt.TimeFrame.Days),
        ("symbol", None),
    )

    def __init__(self, db_uri, *args, **kwargs):
        # db_uri sqlalchemy文档:
        #   https://docs.sqlalchemy.org/en/13/core/engines.html
        super(*args, **kwargs)
        self.db_uri = db_uri

        self.symbol = self.p.dataname

    def start(self):
        super().start()

        if not self.engine:
            log.info("initialize db connection: {}".format(self.db_uri))
            self.__class__.engine = create_engine(self.db_uri)

        # 从数据库load准备数据
        sql = """
            SELECT date
                , open
                , high
                , low
                , close
                , volume
            FROM transactions
            WHERE code = '{}'
                AND open > 0
                AND high > 0
                AND low > 0
                AND close > 0
                AND volume > 0
                AND date >= %s
                AND date <= %s
            """.format(self.symbol)
        rp = self.engine.execute(sql, (self.p.fromdate, self.p.todate))
        historical_eod = list(rp.fetchall())
        historical_eod.sort(key=lambda x: x.date)
        self.historical_eod = iter(historical_eod)

        log.info("load {} rows for {}".format(len(historical_eod), self.symbol))

    def stop(self):
        pass

    def _load(self):
        # 实现 datafeed 的iterator接口函数
        try:
            row = next(self.historical_eod)
        except StopIteration:
            return False

        self.lines.datetime[0] = bt.date2num(row.date)
        self.lines.open[0] = float(row.open)
        self.lines.high[0] = float(row.high)
        self.lines.low[0] = float(row.low)
        self.lines.close[0] = float(row.close)
        self.lines.volume[0] = float(row.volume)
        self.lines.openinterest[0] = 0

        return True