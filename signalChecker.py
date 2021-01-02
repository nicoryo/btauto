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

interval = 35

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

while True:
  try:
    # アクティブな注文の有無を確認
    ticker = api.ticker(product_code="BTC_JPY")
    getchildorders = api.getchildorders(product_code="BTC_JPY", child_order_state="ACTIVE")
    getbalance = api.getbalance(product_code="BTC_JPY")
    jpyAmount = getbalance[0]['amount']
    btcAmount = getbalance[1]['amount']
    cur.execute("SELECT BUYSig, SELLSig, close FROM 5min_table ORDER BY id DESC LIMIT 1;")
    # print(cur.fetchall())
    oneMinuteDataAll = cur.fetchall()
    conn.commit()

    if getchildorders == []: #active order is nothing
      # print(oneMinuteDataAll[0][0],oneMinuteDataAll[0][1],oneMinuteDataAll[0][2])
      if oneMinuteDataAll[0][0] == 1:

        buyPrice = oneMinuteDataAll[0][-1]
        # buySize = (math.floor((jpyAmount / buyPrice) * 100000000))/100000000
        # buyOrder(buyPrice, buySize) # buy order

        # print('買い注文:', buyPrice,'/', buySize )

        comment='5min足で買いシグナル:', buyPrice, 
        lineNotify.main(comment)

        sleep(interval)
      elif oneMinuteDataAll[0][1] == 1:
        
        sellPrice = oneMinuteDataAll[0][-1]
        # sellSize =  (math.floor(btcAmount *(1-0.0015)* 100000000)) / 100000000
        # sellOrder(sellPrice, sellSize) # sell order

        # print('売り注文:', sellPrice, '/', sellSize )

        comment='5min足で売りシグナル:', sellPrice 
        lineNotify.main(comment)

        sleep(interval)
      
      else:
        sleep(2)

    elif getchildorders[0]['side'] == 'BUY':
      if oneMinuteDataAll[0][0] == 1: # buy signal is true
        if getchildorders[0]['price'] > oneMinuteDataAll[0][-1]:
          cancelallchildorders = api.cancelallchildorders(
            product_code="BTC_JPY"
          )

          buyPrice = oneMinuteDataAll[0][-1]
          # buySize = (math.floor((jpyAmount / buyPrice) * 100000000))/100000000
          # buyOrder(buyPrice, buySize) # buy order

          # print('買い注文更新:', buyPrice, '/',  buySize )

          # comment='買い注文更新:', buyPrice, '/',  buySize 
          # lineNotify.main(comment)
          sleep(interval)
        else:
          sleep(2)
      else:
        sleep(2)
    else:
      if oneMinuteDataAll[0][1] == 1: # sell signal is true
        if getchildorders[0]['price'] < oneMinuteDataAll[0][-1]:
          # 注文をキャンセルコード
          cancelallchildorders = api.cancelallchildorders(
            product_code="BTC_JPY"
          )

          sellPrice = oneMinuteDataAll[0][-1]
          # # sellSize =  (math.floor(btcAmount * 100000000) ) / 100000000
          # # sellOrder(sellPrice, sellSize) # sell order
          # # print('売り注文更新:', sellPrice,'/', sellSize )

          # # comment='売り注文更新:', sellPrice,'/', sellSize 
          # lineNotify.main(comment)

          sleep(interval) 
        else:
          sleep(2)
      else:
        sleep(2)
  except:
    comment="5分足シグナルチェッカーシステムにエラーが発生したよ！2分待機！"
    lineNotify.main(comment)
    sleeep(120)
    

# 買い注文を出すコード
# sendchildorder = api.sendchildorder(
#   product_code="BTC_JPY",
#   child_order_type="LIMIT",
#   side="BUY",
#   price=BUY_price,
#   size=BUY_size,
#   minute_to_expire=10000,
#   time_in_force="GTC"
# )
# getchildorders = api.getchildorders(product_code="BTC_JPY", child_order_state="ACTIVE")
# print(getchildorders)
# product_code: 必須。注文するプロダクト。BTC_JPY
# child_order_type: 必須。指値注文の場合は "LIMIT", 成行注文の場合は "MARKET" を指定。
# side: 必須。買い注文の場合は "BUY", 売り注文の場合は "SELL" を指定。
# price: 価格を指定。child_order_type に "LIMIT" を指定した場合は必須。
# size: 必須。注文数量を指定。
# minute_to_expire: 期限切れまでの時間を分で指定。省略した場合の値は 43200 (30 日間) 。
# time_in_force: 執行数量条件 を "GTC", "IOC", "FOK" のいずれかで指定。省略した場合の値は "GTC"


