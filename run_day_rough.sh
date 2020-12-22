#!/usr/local/share/zsh
source ~/.bash_profile

conda activate env

# email 1
# load stocks
python -m data_modules.baostock_reptile -m all

# 趋势入库
python -m stock_analytic_modules.rough.run_rough -m persist

# 发邮件
python -m stock_analytic_modules.rough.run_rough -m report

# email 2
# 月线
python -m data_modules.baostock_reptile -m period

# 月线级别选股
python -m stock_analytic_modules.rough.inc -m month

