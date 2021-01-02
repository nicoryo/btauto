import mysql.connector as mydb
import os
import setting

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

# cur.execute(
#   """
#     DROP TABLE 1min_table;
#   """
# )
# conn.commit()
# cur.execute(
#   """
#     DROP TABLE 5min_table;
#   """
# )
# conn.commit()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS 1min_table(
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        BUYSig BOOLEAN,
        SELLSig BOOLEAN,
        open INT,
        close INT,
        max INT,
        min INT,
        shortEma INT,
        longEma INT,
        MACD INT,
        MACDSignal INT
        )
    """
)
conn.commit()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS 5min_table(
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        BUYSig BOOLEAN,
        SELLSig BOOLEAN,
        open INT,
        close INT,
        max INT,
        min INT,
        shortEma INT,
        longEma INT,
        MACD INT,
        MACDSignal INT
        )
    """
)
conn.commit()



cur.execute(
  """
    ALTER TABLE 1min_table MODIFY BUYSig boolean;
  """
)
conn.commit()
cur.execute(
  """
    ALTER TABLE 1min_table MODIFY SELLSig boolean;
  """
)
conn.commit()

cur.execute(
  """
    ALTER TABLE 5min_table MODIFY BUYSig boolean;
  """
)
conn.commit()
cur.execute(
  """
    ALTER TABLE 5min_table MODIFY SELLSig boolean;
  """
)
conn.commit()


# 初期データを埋め込む
add_bttable =("INSERT INTO 1min_table "
            "(timestamp, BUYSig, SELLSig, open, close, max, min, shortEma, longEma, MACD, MACDSignal)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )
btdata = (
  "2021-01-01T12:46:17.123",
  False,
  False,
  "3020561.0",
  "3020561.0",
  "3020561.0",
  "3020561.0",
  "3020561.0",
  "3020561.0",
  "3020561.0", 
  "3020561.0"
)
cur.execute(add_bttable, btdata)
conn.commit()




add_bttable =("INSERT INTO 5min_table "
            "(timestamp, BUYSig, SELLSig, open, close, max, min, shortEma, longEma, MACD, MACDSignal)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            )

# SQL文の実行
cur.execute(add_bttable, btdata)
conn.commit()

cur.close
conn.close