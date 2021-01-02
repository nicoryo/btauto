# ビットフライヤー自動売買ツール

# システム構成
* getTicker.py(取引所からTicker情報を取得プログラム)
* create1minchart.py(1minローソク足作成プログラム)
* create5minchart.py(5minローソク足作成プログラム)
* tradeBitflyer.py(取引プログラム)

* mysql.py(MySQLでデータベース作成プログラム)
* adjustMysql.py(MySQLのデータ整理プログラム)
* lineNotift.py(注文をLine通知プログラム)

## MACD
MACD = 短期EMA - 長期EMA
## EMA
### 短期EMA
term=１２
### 長期EMA
term=26

## MACDシグナル
MACDのEMA
term=9

# 判定アルゴリズム
MACD vs MACDシグナル 
買いシグナル = ゴールデンクロス
売りシグナル = デッドクロス
