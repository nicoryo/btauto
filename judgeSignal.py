import mysql.connector as mydb
from datetime import datetime as dt
from time import sleep
import pandas as pd

# Mysqlへのコネクションの作成
conn = mydb.connect(
    host='localhost',
    port='3306',
    user='root',
    password='',
    database='bitflyer'
)
# カーソルを取得する
cur = conn.cursor()

# # 手数料
# 0.01% ~ 0.15%

# # Buy
# ALL_buy_BTC = buy_BTC - buy_BTC * 0.0015
# buy_BTC = JPYpBTC * buy_BTC_mount
# buy_BTC_mount = input("発注数を入力")

# shortEMA = df['Close'].ewm(span=5).mean()
# longEMA = df['Close'].ewm(span=20).mean()

# MACD = shortEMA - longEMA

# MACDEMA = 
# signalMACD = MACDEMA



# # Sell
# ALL_sell_BTC = ALL_buy_BTC

# def signal
#   # cur.execute("SELECT * FROM 1min_table;")
# # rows = cur.fetchall()
# # 出力
# # for i in rows:
# #     print(i)

# def max

# def min


# 取得間隔(秒)
interval = 60*5

while True:

  cur.execute("SELECT * FROM 1min_table ORDER BY id DESC LIMIT 6;")
  rows = cur.fetchall()
  data = []
  for i in rows:
    data.append(i[-1])

  datar = list(reversed(data))
  # 短期EMA
  def shortEma(datar=[], term = 12):
    s = pd.Series(datar)
    sma = s.rolling(term).mean()[:term]
    return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())
  shortEma=shortEma(datar)
  print(shortEma[-1])

  # 長期EMA
  def longEma(datar=[], term = 26):
    s = pd.Series(datar)
    sma = s.rolling(term).mean()[:term]
    return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())
  longEma = longEma(datar)
  print(longEma[-1])

  # MACD
  MACD = [x - y for (x, y) in zip(shortEma, longEma)]
  def MACDSignal(MACD=[], term = 9):
    s = pd.Series(MACD)
    sma = s.rolling(term).mean()[:term]
    return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())

  print(MACD)
  MACDSignal = MACDSignal(MACD)
  print(MACDSignal)


  # def ema1(data=[], term=5):
  #   '''指数平滑移動平均の計算(修正版)'''
  #   s = pd.Series(data)
  #   sma = s.rolling(term).mean()[:term]
  #   return list(pd.concat([sma, s[term:]]).ewm(span=term, adjust=False).mean())
  # shortEMA = data.ewm(span=5).mean()
  # print(shortEMA)

  # 最大値
  maxinum = max(data)

  # 最小値
  minimam = min(data)

  # 始値
  open = rows[-1][-1]
  # print(start)

  # 終値
  close = rows[0][-1]
  # print(end)

  # データ作成時間(1minデータの最新時間とする)
  timestamp = rows[0][1]

  # シグナルを判別する
  if open < close:
    sig = True
  else:
    sig = False

  # BuySignal
  MACD > MACDSignal

  # SellSignal
  MACDSignal > MACD


  add_bttable =("INSERT INTO 5min_table "
              "(timestamp, sig, open, close, max, min) "
              "VALUES (%s, %s, %s, %s, %s, %s)"
              )
  btdata = (
    timestamp,
    sig,
    open,
    close,
    maxinum,
    minimam
  )

  # SQL文の実行
  # cur.execute(add_bttable, btdata)
  # conn.commit()

  print(btdata)

  sleep(interval)