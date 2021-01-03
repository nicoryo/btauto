import pybitflyer
import setting
import lineNotify
import decimal
import math
import adjustMysql

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

def buyOrderAmount():
  getbalance  = api.getbalance(product_code="BTC_JPY")
  getboard    = api.board(product_code="BTC_JPY")
  jpyAmount   = getbalance[0]['amount']
  # btcAmount   = getbalance[1]['amount']
  # buyPrice    = getboard["mid_price"]-1000
  buyPrice    = 2800000
  # buySize     = (math.floor((jpyAmount / buyPrice) * 100000000))/100000000
  buySize     = 0.001
  buyOrder(buyPrice, buySize) # buy order
  return {"buyPrice":buyPrice, "buySize":buySize}

# buy = buyOrderAmount()
# print(buy["buyPrice"])

adjustMysql.main()

# getboard = api.board(product_code="BTC_JPY")
# getchildorders = api.getchildorders(product_code="BTC_JPY")[0]
# getbalance = api.getbalance(product_code="BTC_JPY")
# # jpyAmount = getbalance[0]['amount']
# # btcAmount = getbalance[1]['amount']
# # print(getbalance)
# print(getboard["mid_price"])
# print(getboard["mid_price"]-1000)
# print(getchildorders)
# # if getchildorders['child_order_state'] == "ACTIVE":
# if api.getchildorders(product_code="BTC_JPY")[0]['child_order_state'] == "ACTIVE":
#   if getchildorders['side'] == 'SELL':
#     print("OK")
#   elif getchildorders['side'] == []:
#     print("CA")
#   else:
#     print("NG")
