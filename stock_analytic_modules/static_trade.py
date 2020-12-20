# -*- encoding: UTF-8 -*-
import logging
import collections
import pandas as pd
from api_modules.server.utils.config import ConfigUtils
from common import stock_utils
from stock_analytic_modules.layout import parking_apron, keep_increasing, breakthrough_platform, \
    backtrace_ma250, turtle_trade, low_atr
from stock_analytic_modules.layout import enter


def run_pipline_stg(filter_kc=True):
    logging.info("************************ process start ***************************************")
    pd_names = pd.read_csv(ConfigUtils.get_stock("STOCK_NAME"))
    strategies = {
        '海龟交易法则': turtle_trade.check_enter,
        '潜伏慢阳3d': turtle_trade.continue_increase3,
        '潜伏慢阳5d': turtle_trade.continue_increase5,
        '潜伏慢阳7d': turtle_trade.continue_increase7,
        'BigInc': turtle_trade.big_inc,
        'BreakInc': turtle_trade.break_inc,
        'BackInc': turtle_trade.feedback_inc,
        'Demon': turtle_trade.demon_inc,
        '连续含1y': turtle_trade.inc_cyin1,
        '连续含2y': turtle_trade.inc_cyin2,
        '放量上涨_1.5': enter.check_volume,
        '大涨': enter.check_continuous_inc,
        'ATR': enter.check_breakthrough,
        '突破平台': breakthrough_platform.check,
        '均线多头': keep_increasing.check,
        '停机坪': parking_apron.check,
        '回踩年线': backtrace_ma250.check,
        '低ATR成长策略': low_atr.check_low_increase,
        # 'pe': pe.check,
    }

    stg_result_dict = collections.defaultdict(list)
    for index, row in pd_names.iterrows():
        code = row['code']
        name = row['code_name']
        
        if filter_kc and stock_utils.is_jiucaiban(code):
            continue
        if "ST" in name:
            continue
        code_name = (code, name)
        print(code_name)
        data = stock_utils.read_data(code_name)
        if data is None:
            continue

        for strategy, strategy_func in strategies.items():
            r = strategy_func(code_name, data)
            if r and r > 0.0:
                stg_result_dict[strategy].append((code, name, r))

    for strategy, results in stg_result_dict.items():
        outs = sorted(results, key=lambda e: e[2], reverse=True)
        stock_utils.persist(strategy, outs)
    logging.info("************************ process   end ***************************************")


if __name__ == '__main__':
    run_pipline_stg()