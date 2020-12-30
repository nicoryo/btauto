import mysql.connector as mydb
from datetime import datetime as dt
from time import sleep

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

  cur.execute("SELECT * FROM 1min_table ORDER BY id DESC LIMIT 5;")
  rows = cur.fetchall()

  # 最大値
  maxinum = []
  for i in rows:
    # print(i)
    maxinum.append(i[-1])
  # print(maxinum)
  maxinum = max(maxinum)
  # print(maxinum)

  # 最小値
  minimam = []
  for i in rows:
    minimam.append(i[-1])

  minimam = min(minimam)
  # print(minimam)

  # 始値
  start = rows[-1][-1]
  # print(start)

  # 終値
  end = rows[0][-1]
  # print(end)

  # データ作成時間(1minデータの最新時間とする)
  timestamp = rows[0][1]

  # シグナルを判別する
  if start < end:
    sig = True
  else:
    sig = False

  add_bttable =("INSERT INTO 5min_table "
              "(timestamp, sig, start, end, max, min) "
              "VALUES (%s, %s, %s, %s, %s, %s)"
              )
  btdata = (
    timestamp,
    sig,
    start,
    end,
    maxinum,
    minimam
  )

  # SQL文の実行
  cur.execute(add_bttable, btdata)
  conn.commit()

  print(btdata)

  sleep(interval)