import mysql.connector as mydb
import os
from dotenv import load_dotenv

load_dotenv('.env') 

RDShost = os.environ.get("RDShost")
RDSpass = os.environ.get("RDSpass")
# coding:utf-8
# コネクションの作成
conn = mydb.connect(
    # host='localhost',
    host=RDShost,
    port='3306',
    db='bitcoin01',
    # user='root',
    user='nicoryo',
    # password='',
    password=RDSpass,
    # database='bitflyer'
    charset="utf8"
)
# conn = mydb.connect(
#     host='localhost',
#     port='3306',
#     user='root',
#     password='',
#     database='bitflyer',
#     charset="utf8"
# )

# カーソルを取得する
cur = conn.cursor()

# テーブルを作成する
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS got_data(
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        price int
        )
    """
)
conn.commit()



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

# 書き込みテスト
# cur.execute("INSERT INTO 1min_table (timestamp, price) VALUES (20201226, 10200)")
# conn.commit()

# MySQL出力テスト
# cur.execute("SELECT * FROM 1min_table;")
# rows = cur.fetchall()
# 出力
# for i in rows:
#     print(i)

cur.close
conn.close