import mysql.connector as mydb
import pybitflyer
from time import sleep
import setting
import buyTradeBitflyer
import sellTradeBitflyer
import lineNotify
from sshtunnel import SSHTunnelForwarder

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
RDShost = setting.RDShost
RDSpass = setting.RDSpass
RDSdb   = setting.RDSdb
RDSuser = setting.RDSuser

interval = 60
# coding:utf-8
# コネクションの作成
server = SSHTunnelForwarder(
    ('54.150.52.37', 22),
    ssh_host_key=None,
    ssh_username='ec2-user',
    ssh_password=None,
    ssh_pkey='./bitcoin_step_saver01.pem',
    remote_bind_address=(RDShost, 3306),
    local_bind_address=('127.0.0.1',10022)
)

server.start()
print("STEP1 server start")
conn = mydb.connect(
    host    ='127.0.0.1',
    port    =10022,
    user    =RDSuser,
    password=RDSpass,
    database=RDSdb,
    charset="utf8"
)
print('STEP2 get cursor')
# カーソルを取得する
cur = conn.cursor()

api = pybitflyer.API(
  API_KEY,
  API_SECRET  
  )

interval = 1

try:
  while True:
    cur.execute("SELECT MACD, MACDSignal FROM 5min_table ORDER BY id DESC LIMIT 2;")
    oneMinuteDataAll = cur.fetchall()
    conn.commit()

    MACD_n_minus1 = oneMinuteDataAll[1][-2]
    MACDSignal_n_minus1 = oneMinuteDataAll[1][-1]
    MACD_n = oneMinuteDataAll[0][-2]
    MACDSignal_n = oneMinuteDataAll[0][-1]

    if MACD_n_minus1 < MACDSignal_n_minus1:
    # かつ今回のデータがMACD>MACDSignal
      if MACD_n > MACDSignal_n:
        # buyTradeBitflyer.buyTrade()
        comment='Remote buy order test 5min'
        lineNotify.main(comment)
        sleep(60)

    elif MACD_n_minus1 > MACDSignal_n_minus1:
      if MACD_n < MACDSignal_n:
        # sellTradeBitflyer.sellTrade()
        comment='Remote sell order test 5min'
        lineNotify.main(comment)
        sleep(60)   
    else:
      sleep(interval)

except:
  comment='Algorithm Error have been ocurred!' 
  lineNotify.main(comment)