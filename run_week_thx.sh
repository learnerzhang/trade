#!/bin/bash
python -m common.sql_utils -m init-blocks

python -m common.sql_utils -m init-stocks

python -m common.sql_utils -m init-bs
