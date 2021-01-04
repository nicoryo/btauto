import mysql.connector as mydb
import pybitflyer
from time import sleep
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

interval = 1

try:
  while True:
    cur.execute("SELECT MACD, MACDSignal FROM 1min_table ORDER BY id DESC LIMIT 2;")
    oneMinuteDataAll = cur.fetchall()
    conn.commit()

    MACD_n_minus1 = oneMinuteDataAll[1][-2]
    MACDSignal_n_minus1 = oneMinuteDataAll[1][-1]
    MACD_n = oneMinuteDataAll[0][-2]
    MACDSignal_n = oneMinuteDataAll[0][-1]

    # print(Amount["buyPrice"])
    # cur.close()
    # conn.close()

    if MACD_n_minus1 < MACDSignal_n_minus1:
    # かつ今回のデータがMACD>MACDSignal
      if MACD_n > MACDSignal_n:
        buyTradeBitflyer.buyTrade()
        sleep(interval)

    elif MACD_n_minus1 > MACD_n_minus1:
      if MACD_n < MACDSignal_n:
        sellTradeBitflyer.sellTrade()
        sleep(interval)   
    else:
      sleep(interval)

except:
  comment='Algorithm Error have been ocurred!' 
  lineNotify.main(comment)