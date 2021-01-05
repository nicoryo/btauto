# import mysql.connector as mydb
import pybitflyer
from time import sleep
import setting
import lineNotify
import math
# from sshtunnel import SSHTunnelForwarder

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
RDShost = setting.RDShost
RDSpass = setting.RDSpass
RDSdb   = setting.RDSdb
RDSuser = setting.RDSuser

# coding:utf-8

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

# # コネクションの作成
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

# 売り注文を出すコード
def sellOrder(sellPrice=[], sellSize=[]):
  return api.sendchildorder(
    product_code="BTC_JPY",
    child_order_type="LIMIT",
    side="SELL",
    price=sellPrice,
    size=sellSize,
    minute_to_expire=10000,
    time_in_force="GTC"
  )

# 売り注文の値段と量を調整するコード
def sellOrderAmount():
  getbalance = api.getbalance(product_code="BTC_JPY")
  getboard    = api.board(product_code="BTC_JPY")
  # jpyAmount = getbalance[0]['amount']
  btcAmount = getbalance[1]['amount']
  sellPrice = getboard["mid_price"]+1000
  # sellPrice   = 3300000
  sellSize =  (math.floor(btcAmount *(1-0.0015)* 100000000)) / 100000000
  sellOrder(sellPrice, sellSize) # sell order
  return {"sellPrice":sellPrice,"sellSize":sellSize}

# 売り注文から約定まで
def sellTrade():
  try:
    if not api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "ACTIVE":
      Amount = sellOrderAmount()
      sellOrder(Amount["sellPrice"],Amount["sellSize"])
      print('売り注文:', Amount["sellPrice"],'/', Amount["sellSize"] )
      comment='売り注文:', Amount["sellPrice"],'/', Amount["sellSize"] 
      lineNotify.main(comment)
      sleep(shortsleep)

      while not api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "COMPLETED":
        # bitflyer側の反映が遅れている可能性あり！
        while api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "ACTIVE":
 
          api.cancelallchildorders(product_code="BTC_JPY")
          sleep(1)
          Amount = sellOrderAmount()
          sellOrder(Amount["sellPrice"],Amount["sellSize"])

          comment='売り注文訂正:', Amount["sellPrice"],'/',Amount["sellSize"] 
          lineNotify.main(comment)
          sleep(shortsleep)

        if api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "REJECTED":
          comment='注文失敗！注文やめまーす！どんまい'
          lineNotify.main(comment)
          sleep(shortsleep)
          break

      if api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "CANCELED":
          getexecutions = api.getexecutions(product_code="BTC_JPY")[1]
          comment='売り注文約定?:', getexecutions['price'],'/', getexecutions['size']
          lineNotify.main(comment)
          sleep(shortsleep)
          

      # 約定通知
      getexecutions = api.getexecutions(product_code="BTC_JPY")[0]
      comment='売り注文約定:', getexecutions['price'],'/', getexecutions['size']
      lineNotify.main(comment)
      sleep(interval)
  except:
    comment='Please check sell trade system'
    lineNotify.main(comment)

if __name__ == "__main__":
    sellTrade()

