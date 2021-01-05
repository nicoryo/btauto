import pybitflyer
import setting
import lineNotify
import decimal
import math
import adjustMysql
import datetime
import time
import mysql.connector as mydb

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

interval = 1
get = api.getchildorders(product_code="BTC_JPY")
getexecutions = api.getexecutions(product_code="BTC_JPY")
for i in range(10):
  print(getexecutions[i]['side'], getexecutions[i]['price'], getexecutions[i]['size'], getexecutions[i]['exec_date'])
# print(get[0]['child_order_state'])
# print(getexecutions)
# for i in range(50):
#   print(get[i]['child_order_state'])

# cur.execute("SELECT MACD, MACDSignal FROM 1min_table ORDER BY id DESC LIMIT 2;")
# oneMinuteDataAll = cur.fetchall()
# conn.commit()
# print(oneMinuteDataAll)
def job():
  return(datetime.datetime.now()) 

def main():
  return("main") 

if __name__ == "__main__":
    job()
