#!/bin/bash

func() {
    echo "func:"
    echo "run.sh [-d] [-r] [-n] [-s] [-g] [-t] [-p]"
    echo "Description:"
    echo "[-d], load stock info from baostock."
    echo "[-r], generate index stg"
    echo "[-g], generate dataset"
    echo "[-x], syncup dataset"
    echo "[-a], run trade"
    echo "[-n], npm ui"
    echo "[-t], train model"
    echo "[-p], predict model"
    echo "[-s], run app"
    exit
}


while getopts ":ahdrnsgtpx" arg #选项后面的冒号表示该选项需要参数
do
      case $arg in
            a) flask trade-run;;
            r) flask run-stg;;
            d) flask init-stock;;
            x) flask syncup-stock;;
            g) flask run-gen-ds;;
            t) flask train;;
            p) flask predict;;
            n) npm run dev;;
            s) python -m app;;
            h) func;;
            ?) func;;
      esac
done


if [ ! -n "$1" ]; then
      func
      exit
fi
