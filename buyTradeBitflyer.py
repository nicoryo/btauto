import mysql.connector as mydb
import pybitflyer
from time import sleep
import setting
import lineNotify
import math

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
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
        while api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "ACTIVE":
          # お財布状況（リファクタリング候補）
          api.cancelallchildorders(product_code="BTC_JPY")
          sleep(1)
          Amount = buyOrderAmount()
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

      # 約定通知
      getexecutions = api.getexecutions(product_code="BTC_JPY")[0]
      comment='買い注文約定:', getexecutions['price'],'/', getexecutions['size']
      lineNotify.main(comment)
      sleep(interval)
  except:
    comment='Please check buy trade system'
    lineNotify.main(comment)

if __name__ == "__main__":
    buyTrade()

