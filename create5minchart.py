import mysql.connector as mydb
from datetime import datetime as dt
from time import sleep
import pandas as pd
import os
from dotenv import load_dotenv

# 取得間隔(秒)
interval = 60*5

load_dotenv('.env') 

RDShost = os.environ.get("RDShost")
RDSpass = os.environ.get("RDSpass")
# coding:utf-8
# コネクションの作成
conn = mydb.connect(
    # host='localhost',
    host='RDShost',
    port='3306',
    db='bitcoin01',
    # user='root',
    user='nicoryo',
    # password='',
    password='RDSpass',
    # database='bitflyer'
    charset="utf8"
)
# カーソルを取得する
cur = conn.cursor()

while True:

  cur.execute("SELECT * FROM 1min_table ORDER BY id DESC LIMIT 5;")
  rows = cur.fetchall()
  data = []
  for i in rows:
    data.append(i[-1])

  # 最大値
  maxinum = max(data)

  # 最小値
  minimam = min(data)

  # 始値
  open = rows[-1][-1]
  # print(start)

  # 終値
  close = rows[0][-1]
  # print(end)

  # データ作成時間(1minデータの最新時間とする)
  timestamp = rows[0][1]

  # 手前に新しいデータの順でSQLから取得
  cur.execute("SELECT * FROM 5mins_table ORDER BY id DESC LIMIT 26;")
  oneMinuteDataAll = cur.fetchall()
  oneMinuteDataPrice = []
  for i in oneMinuteDataAll:
    oneMinuteDataPrice.append(i[5])

  # 手前が古い順に並び直す
  oneMinuteDataPriceR = list(reversed(oneMinuteDataPrice))
  # 短期EMA
  def shortEma(oneMinuteDataPriceR=[], term = 12):
    s = pd.Series(oneMinuteDataPriceR)
    sma = s.rolling(term).mean()[:term]
    return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())
  shortEma=shortEma(oneMinuteDataPriceR)[-1]
  # 一番後ろのデータが最新のEMAになる

  # 長期EMA
  def longEma(oneMinuteDataPriceR=[], term = 26):
    s = pd.Series(oneMinuteDataPriceR)
    sma = s.rolling(term).mean()[:term]
    return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())
  longEma = longEma(oneMinuteDataPriceR)[-1]

  # MACD
  MACD = [x - y for (x, y) in zip(shortEma, longEma)]

  # MACDSignal
  oneMinuteDataMACD = []
  for i in oneMinuteDataAll:
    oneMinuteDataMACD.append(i[-2])
  oneMinuteDataMACDR = list(reversed(oneMinuteDataMACD))
  def MACDSignal(oneMinuteDataMACDR=[], term = 9):
    s = pd.Series(oneMinuteDataMACDR)
    sma = s.rolling(term).mean()[:term]
    return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())

  MACDSignal = MACDSignal(oneMinuteDataMACDR)[-1]

  # BuySignal
  # 前回のデータがMACD<MACDSignal
  if oneMinuteDataAll[0][-2] < oneMinuteDataAll[0][-1]:
  # かつ今回のデータがMACD>MACDSignal
    if MACD > MACDSignal:
      BUYSig = True
    else: 
      BUYSig = False
  else:
    BUYSig = False



  # SellSignal
  # 前回のデータがMACD>MACDSignal
  if oneMinuteDataAll[0][-2] > oneMinuteDataAll[0][-1]:
  # かつ今回のデータがMACD<MACDSignal
    if MACD < MACDSignal:
      SELLSig = True
    else: 
      SELLSig = False
  else:
    SELLSig = False


  add_bttable =("INSERT INTO 5min_table "
              "(timestamp, BUYSig, SELLSig, open, close, max, min, shortEma, longEma, MACD, MACDSignal)"
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
              )
  btdata = (
    timestamp,
    BUYSig,
    SELLSig,
    open,
    close,
    maxinum,
    minimam,
    shortEma,
    longEma,
    MACD,
    MACDSignal
  )

  # SQL文の実行
  cur.execute(add_bttable, btdata)
  conn.commit()

  print(btdata)

  sleep(interval)