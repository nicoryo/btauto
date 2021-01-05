# import mysql.connector as mydb
import pybitflyer
from time import sleep
import setting
import lineNotify
import math
# from sshtunnel import SSHTunnelForwarder
import datetime
from datetime import datetime as dt

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
RDShost = setting.RDShost
RDSpass = setting.RDSpass
RDSdb   = setting.RDSdb
RDSuser = setting.RDSuser

# coding:utf-8
# コネクションの作成
# server = SSHTunnelForwarder(
#     ('54.150.52.37', 22),
#     ssh_host_key=None,
#     ssh_username='ec2-user',
#     ssh_password=None,
#     ssh_pkey='./bitcoin_step_saver01.pem',
#     remote_bind_address=(RDShost, 3306),
#     local_bind_address=('127.0.0.1',10022)
# )
# print("STEP1 server start")
# # server.start()
# conn = mydb.connect(
#     host    ='127.0.0.1',
#     port    =10022,
#     user    =RDSuser,
#     password=RDSpass,
#     database=RDSdb,
#     charset="utf8"
# )

# # カーソルを取得する
# cur = conn.cursor()

# APIへアクセス
api = pybitflyer.API(
  API_KEY,
  API_SECRET  
  )

interval = 60
shortsleep = 5

# 買い注文を出すコード
def buyOrder(buyPrice=[], buySize=[]):
  return api.sendchildorder(
    product_code="BTC_JPY",
    child_order_type="LIMIT",
    side="BUY",
    price=buyPrice,
    size=buySize,
    minute_to_expire=10000,
    time_in_force="GTC"
  )

# 買い注文の値段と量を調整するコード
def buyOrderAmount():
  getbalance  = api.getbalance(product_code="BTC_JPY")
  getboard    = api.board(product_code="BTC_JPY")
  jpyAmount   = getbalance[0]['amount']
  if jpyAmount > 50000:
    jpyAmount = 50000
  # btcAmount   = getbalance[1]['amount']
  # btcAmount   = getbalance[1]['amount']
  buyPrice    = getboard["mid_price"]-1000
  buySize     = (math.floor((jpyAmount / buyPrice) * 100000000))/100000000
  # buyOrder(buyPrice, buySize) # buy order
  return {"buyPrice":buyPrice,"buySize":buySize}

# 買い注文から約定まで
def buyTrade():
  try:
    if not api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "ACTIVE":
      # お財布状況（リファクタリング候補）
      Amount = buyOrderAmount()
      buyOrder(Amount["buyPrice"],Amount["buySize"])
      # print('買い注文:', buyOrderResult["buyPrice"],'/', buyOrderResult["buySize"] )
      comment='買い注文:', Amount["buyPrice"],'/', Amount["buySize"] 
      lineNotify.main(comment)
      sleep(shortsleep)

      while not api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "COMPLETED":
        if api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "ACTIVE":
          # お財布状況（リファクタリング候補）
          api.cancelallchildorders(product_code="BTC_JPY")
          sleep(1)
          Amount = buyOrderAmount()

          if Amount["buySize"] < 0.0001:
            break
          buyOrder(Amount["buyPrice"],Amount["buySize"])

          comment='買い注文訂正:', Amount["buyPrice"],'/',Amount["buySize"] 
          lineNotify.main(comment)
          sleep(shortsleep)

        sleep(shortsleep)
        if api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "REJECTED":
          comment='注文失敗！注文やめまーす！どんまい'
          lineNotify.main(comment)
          sleep(shortsleep)
          break

        if api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "CANCELED":
          sleep(shortsleep)
          break
            
      # 約定通知
      getexecutions = api.getexecutions(product_code="BTC_JPY")[0]
      try:
        exectime = dt.strptime(getexecutions['exec_date'], '%Y-%m-%dT%H:%M:%S.%f')
      except:
        exectime = dt.strptime(getexecutions['exec_date'], '%Y-%m-%dT%H:%M:%S')
      if exectime.minute == datetime.datetime.now().minute:
        comment='買い注文約定:', getexecutions['price'],'/', getexecutions['size']
        lineNotify.main(comment)
        sleep(interval)
      else:
        getexecutions = api.getexecutions(product_code="BTC_JPY")[1]
        comment='買い注文約定?:', getexecutions['price'],'/', getexecutions['size']
        lineNotify.main(comment)
        sleep(interval)

  except:
    comment='Please check buy trade system'
    lineNotify.main(comment)

if __name__ == "__main__":
    buyTrade()

