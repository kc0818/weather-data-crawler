#!/bin/bash
set -e

# venvが存在するか確認
if [ -d "./venv" ]; then
    echo "venv exsit"
else
    echo "make venv"
    python -m venv venv
fi

source "venv/bin/activate"
pip install -r requirements.txt
echo "venv activated"

# 入力を受け取る
read -p "対象の年を入力して下さい: " year
read -p "対象の月を入力して下さい: " month

# クローリング実行
python crawler.py --year="$year" --month="$month"
