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
    host='RDShost',
    port='3306',
    db='bitcoin01',
    # user='root',
    user='nicoryo',
    # password='',
    password='RDSpass',
    # database='bitflyer'
    charset="utf8"
)

# カーソルを取得する
cur = conn.cursor()

# テーブルを作成する
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS 1min_table(
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        price INT
        )
    """
)
conn.commit()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS 5min_table(
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        timestamp DATETIME,
        sig VARCHAR(25),
        open INT,
        close INT,
        max INT,
        min INT
        )
    """
)
conn.commit()

cur.close
conn.close