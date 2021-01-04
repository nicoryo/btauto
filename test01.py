import pybitflyer
import setting
import lineNotify
# import decimal
import math
# import adjustMysql
import datetime
import time
# import test
import buyTradeBitflyer
import sellTradeBitflyer

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

# print(test.job())

# print(test.main())
# TEST = api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "COMPLETED"
# TEST = api.getchildorders(product_code="BTC_JPY")[0]['child_order_state']
# print(TEST)

sellTradeBitflyer.sellTrade()