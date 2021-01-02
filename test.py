import pybitflyer
import setting
import lineNotify
import decimal
import math

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

getchildorders = api.getchildorders(product_code="BTC_JPY", child_order_state="active")
getbalance = api.getbalance(product_code="BTC_JPY")
# jpyAmount = getbalance[0]['amount']
# btcAmount = getbalance[1]['amount']
print(getbalance)
# print(jpyAmount)
# print(type(jpyAmount))
# a = 0
# if a == 0:
#   buyPrice = 2800000
#   # decimal.getcontext().prec = 6
#   # buySize = decimal.Decimal(jpyAmount / buyPrice).quantize(Decimal('.00000001'), rounding=ROUND_DOWN)
#   # buySize = decimal.Decimal(jpyAmount / buyPrice)
#   # buySize = round(jpyAmount / buyPrice, 8)
#   buySize = (math.floor((jpyAmount / buyPrice) * 100000000))/100000000
#   print(buySize)
#   print(type(buySize))
#   buyOrder(buyPrice, buySize)
  # comment='買い注文 :', buyPrice, '/', buySize
# lineNotify.main(comment)


# print('買い注文 :', buyPrice, '/', buySize )