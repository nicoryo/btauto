import pybitflyer
import os
from dotenv import load_dotenv

load_dotenv('.env') 

API_KEY = os.environ.get("api_key")
API_SECRET = os.environ.get("api_secret_key")

# APIへアクセス
api = pybitflyer.API(
  API_KEY,
  API_SECRET  
  )

# ticker = api.ticker(product_code="BTC_JPY")
# print(ticker)

getbalance = api.getbalance(product_code="BTC_JPY")
print(getbalance[0])


# 買い注文を出すコード
sendchildorder = api.sendchildorder(
  product_code="BTC_JPY",
  child_order_type="LIMIT",
  side="BUY",
  price="2800000",
  size=0.001,
  minute_to_expire=10000,
  time_in_force="GTC"
)
# product_code: 必須。注文するプロダクト。BTC_JPY
# child_order_type: 必須。指値注文の場合は "LIMIT", 成行注文の場合は "MARKET" を指定。
# side: 必須。買い注文の場合は "BUY", 売り注文の場合は "SELL" を指定。
# price: 価格を指定。child_order_type に "LIMIT" を指定した場合は必須。
# size: 必須。注文数量を指定。
# minute_to_expire: 期限切れまでの時間を分で指定。省略した場合の値は 43200 (30 日間) 。
# time_in_force: 執行数量条件 を "GTC", "IOC", "FOK" のいずれかで指定。省略した場合の値は "GTC"

# 注文をキャンセルコード
cancelallchildorders = api.cancelallchildorders(
  product_code="BTC_JPY"
)
