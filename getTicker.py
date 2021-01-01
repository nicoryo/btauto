import pybitflyer
import mysql.connector as mydb
from datetime import datetime as dt
from time import sleep
import os
from dotenv import load_dotenv

# APIへアクセス
api = pybitflyer.API(
  
  )
# 取得するデータを選択する
option = ['timestamp','ltp']

# best_ask：最高買価格
# best_bid：最低売価格
# best_ask_size：最高買価格数
# best_bid_size：最低売価格数
# ltp：最終取引価格
# total_ask_depth：買注文総数
# total_bid_depth：売注文総数
# volume_by_product: 価格ごとの出来高


# 取得間隔(秒)
interval = 10

load_dotenv('.env') 

RDShost = os.environ.get("RDShost")
RDSpass = os.environ.get("RDSpass")
# coding:utf-8
# コネクションの作成
conn = mydb.connect(
    # host='localhost',
    host=RDShost,
    port='3306',
    db='bitcoin01',
    # user='root',
    user='nicoryo',
    # password='',
    password=RDSpass,
    # database='bitflyer'
    charset="utf8"
)
# カーソルを取得する
cur = conn.cursor()

print('準備完了')

while True:
  # 取得
  ticker = api.ticker(product_code="BTC_JPY")

  # 保存用にコンマ区切りにする
  line = ','.join([str(ticker[op]) for op in option])
  print(line)

  # レコード追加のSQL文
  add_bttable =("INSERT INTO 1min_table "
                "(timestamp, price) "
                "VALUES (%s, %s)"
                )

  try:
    btdate = dt.strptime(ticker['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
  except:
    btdate = dt.strptime(ticker['timestamp'], '%Y-%m-%dT%H:%M:%S')
 
  # パラメータの設定
  btdata =  (
      btdate,
      ticker['ltp']
    )

  # SQL文の実行
  cur.execute(add_bttable, btdata)
  conn.commit()

  # 指定した秒数だけストップ
  sleep(interval)
