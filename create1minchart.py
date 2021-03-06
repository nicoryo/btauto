import mysql.connector as mydb
from datetime import datetime as dt
from time import sleep
import pandas as pd
import setting
import math
import lineNotify

def main():
  # 取得間隔(秒)
  # interval = 60

  # API_KEY = setting.API_KEY
  # API_SECRET = setting.API_SECRET
  RDShost = setting.RDShost
  RDSpass = setting.RDSpass
  RDSdb   = setting.RDSdb
  RDSuser = setting.RDSuser

  # coding:utf-8
  # コネクションの作成
  conn = mydb.connect(
      host    =RDShost,
      port    ='3306',
      user    =RDSuser,
      password=RDSpass,
      database=RDSdb,
      charset="utf8"
  )
  # カーソルを取得する
  cur = conn.cursor()

  try:

    cur.execute("SELECT * FROM got_data ORDER BY id DESC LIMIT 6;")
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

    ## MACDを作成
    # 手前に新しいデータの順でSQLから取得
    cur.execute("SELECT * FROM 1min_table ORDER BY id DESC LIMIT 26;")
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
    if math.isnan(shortEma):
      shortEma = "0"

    # 一番後ろのデータが最新のEMAになる

    # 長期EMA
    def longEma(oneMinuteDataPriceR=[], term = 26):
      s = pd.Series(oneMinuteDataPriceR)
      sma = s.rolling(term).mean()[:term]
      return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())
    longEma = longEma(oneMinuteDataPriceR)[-1]
    if math.isnan(longEma):
      longEma = "0"

    # MACD
    # MACD = [x - y for (x, y) in zip(shortEma, longEma)]
    try: 
      MACD = shortEma - longEma
    except:
      MACD = "0"

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
    if math.isnan(MACDSignal):
      MACDSignal = "0"

    # BUYSig = False
    # SELLSig = False
    # BuySignal
    # 前回のデータがMACD<MACDSignal
    try:
      if oneMinuteDataAll[0][-2] < oneMinuteDataAll[0][-1]:
      # かつ今回のデータがMACD>MACDSignal
        if MACD > MACDSignal:
          BUYSig = True
        else: 
          BUYSig = False
      else:
        BUYSig = False
    except:
      BUYSig = False
      print("buySigError")



    # SellSignal
    # 前回のデータがMACD>MACDSignal
    try:
      if oneMinuteDataAll[0][-2] > oneMinuteDataAll[0][-1]:
      # かつ今回のデータがMACD<MACDSignal
        if MACD < MACDSignal:
          SELLSig = True
        else: 
          SELLSig = False
      else:
        SELLSig = False
    except:
      SELLSig = False
      print("sellSigError")

    add_bttable =("INSERT INTO 1min_table "
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

    # print(btdata)
  except:
    comment="データ取得システムにエラーが発生したよ！"
    lineNotify.main(comment)

if __name__ == "__main__":
    main()
