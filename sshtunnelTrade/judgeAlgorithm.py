import mysql.connector as mydb
import pybitflyer
from time import sleep
import pandas as pd
import setting
import buyTradeBitflyer
import sellTradeBitflyer
import lineNotify
from sshtunnel import SSHTunnelForwarder

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET

RDShost     = setting.RDShost
RDSpass     = setting.RDSpass
RDSport     = setting.RDSport

Host        = setting.Host
Port        = setting.Port
Db          = setting.Db
User        = setting.User

SSHadress   = setting.SSHadress
SSHusername = setting.SSHusername
SSHpkey     = setting.SSHpkey

ENV         = setting.ENV

if ENV == 'local':
  # coding:utf-8
  # コネクションの作成
  server = SSHTunnelForwarder(
      ('54.150.52.37', 22),
      ssh_host_key        = None,
      ssh_username        = SSHusername,
      ssh_password        = None,
      ssh_pkey            = SSHpkey,
      remote_bind_address = (RDShost, 3306),
      local_bind_address  = ('127.0.0.1',10022)
  )
  server.start()
  print("STEP1 server start")

conn = mydb.connect(
    host    =Host,
    port    =Port,
    user    =User,
    password=RDSpass,
    database=Db,
    charset="utf8"
)

print('STEP2 get cursor')
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