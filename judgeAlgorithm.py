import mysql.connector as mydb
import pybitflyer
from time import sleep
import pandas as pd
import setting
import buyTradeBitflyer
import sellTradeBitflyer
import lineNotify

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
RDShost = setting.RDShost
RDSpass = setting.RDSpass
RDSdb   = setting.RDSdb
RDSuser = setting.RDSuser

interval = 60
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

api = pybitflyer.API(
  API_KEY,
  API_SECRET  
  )

def shortEma(oneMinuteDataPriceR=[], term = 12):
  s = pd.Series(oneMinuteDataPriceR)
  sma = s.rolling(term).mean()[:term]
  return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())

def longEma(oneMinuteDataPriceR=[], term = 26):
  s = pd.Series(oneMinuteDataPriceR)
  sma = s.rolling(term).mean()[:term]
  return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())

def MACDSignal(oneMinuteDataMACDR=[], term = 9):
  s = pd.Series(oneMinuteDataMACDR)
  sma = s.rolling(term).mean()[:term]
  return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())

interval = 1
intervaltime = 60*5

try:
  while True:
    ticker = api.ticker(product_code="BTC_JPY")

    cur.execute("SELECT * FROM 5min_table ORDER BY id DESC LIMIT 25;")
    # cur.execute("SELECT * FROM 1min_table ORDER BY id DESC LIMIT 25;")
    oneMinuteDataAll = cur.fetchall()
    oneMinuteDataPrice = [ticker['ltp']]
    conn.commit()

    for i in oneMinuteDataAll:
      oneMinuteDataPrice.append(i[5])

    oneMinuteDataPriceR = list(reversed(oneMinuteDataPrice))

    ShortEma  = shortEma(oneMinuteDataPriceR)[-1]
    LongEma   = longEma(oneMinuteDataPriceR)[-1]

    MACD = ShortEma - LongEma

    # MACDSignal
    oneMinuteDataMACD = [MACD]
    for i in oneMinuteDataAll:
      oneMinuteDataMACD.append(i[-2])

    oneMinuteDataMACDR = list(reversed(oneMinuteDataMACD))

    MacdSignal = MACDSignal(oneMinuteDataMACDR)[-1]

    MACDNMinus1 = oneMinuteDataAll[0][-2]
    MACDSignalNMinus1 = oneMinuteDataAll[0][-1]

    sleep(2)

    if MACDNMinus1 < MACDSignalNMinus1:
    # かつ今回のデータがMACD>MACDSignal
      if MACD > MacdSignal:
        buyTradeBitflyer.buyTrade(intervaltime)
        # comment='Remote buy order test 5min'
        # lineNotify.main(comment)

    elif MACDNMinus1 > MACDSignalNMinus1:
      if MACD < MacdSignal:
        sellTradeBitflyer.sellTrade(intervaltime)
        # comment='Remote sell order test 5min'
        # lineNotify.main(comment)   
    else:
      sleep(interval)

except:
  comment='Algorithm Error have been ocurred!' 
  lineNotify.main(comment)