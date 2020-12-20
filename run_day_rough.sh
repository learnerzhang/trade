#!/usr/local/share/zsh
source ~/.bash_profile

conda activate env

python -m data_modules.baostock_reptile -m all

python -m stock_analytic_modules.rough.run_rough -m persist

python -m stock_analytic_modules.rough.run_rough -m report

