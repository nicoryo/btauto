import mysql.connector as mydb

# コネクションの作成
conn = mydb.connect(
    # host='localhost',
    port='3306',
    db='db-bitcoin01',
    # user='root',
    user='nicoryo',
    # password='',
    password='Kaitou1412',
    # database='bitflyer'
    charset=”utf8"
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
        start INT,
        end INT,
        max INT,
        min INT
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