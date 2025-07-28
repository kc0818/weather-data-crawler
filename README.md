# weather-data-crawler

## 概要
気象庁の過去の気象データ検索（日ごと）からデータをクローリングし、csvファイルとして成果物を出力する。

## 対象ページの例
https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=44&block_no=47662&year=2025&month=7&day=&view=

## 実行コマンド
### シェルスクリプトで実行
```
sh crawling.sh
```

### 手動実行
```
python crawler.py --year=2025 --month=7
```
