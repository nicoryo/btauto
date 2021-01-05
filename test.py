import pybitflyer
import setting
import lineNotify
import decimal
import math
import adjustMysql
import datetime
import time
import mysql.connector as mydb
from datetime import datetime as dt

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
RDShost = setting.RDShost
RDSpass = setting.RDSpass
RDSdb   = setting.RDSdb
RDSuser = setting.RDSuser

# APIへアクセス
api = pybitflyer.API(
  API_KEY,
  API_SECRET  
  )

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

#  買い注文を出すコード
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
  buyPrice    = 2800000
  buySize     = 0.001
  # buyOrder(buyPrice, buySize) # buy order
  return {"buyPrice":buyPrice,"buySize":buySize}

# getexecutions = api.getexecutions(product_code="BTC_JPY")[0]
# try:
#   btdate = dt.strptime(getexecutions['exec_date'], '%Y-%m-%dT%H:%M:%S.%f')
# except:
#   btdate = dt.strptime(getexecutions['exec_date'], '%Y-%m-%dT%H:%M:%S')
# print(btdate.minute)
# print(datetime.datetime.now())
# print(datetime.datetime.now().minute)
# Amount = buyOrderAmount()
# buyOrder(Amount["buyPrice"], Amount["buySize"])
# api.cancelallchildorders(product_code="BTC_JPY")
# time.sleep(1)
# while True:
#   Amount
#   print("a")
#   if Amount["buySize"] < 0.002:
#     break
num = 0
while True:
  if num <100:
    print(num)
    if num > 10:
      print("step1")
      break
    num = num + 1
print("step2")
print(datetime.datetime.now().minute)
# print(api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'])
# time.sleep(5)
# print(api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'])


def job():
  return(datetime.datetime.now()) 

def main():
  return("main") 

if __name__ == "__main__":
    job()
