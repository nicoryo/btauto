import mysql.connector as mydb
import setting

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
RDShost = setting.RDShost
RDSpass = setting.RDSpass
RDSdb   = setting.RDSdb
RDSuser = setting.RDSuser
# coding:utf-8
def main():
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

  cur.execute(
    """
      DELETE FROM 
        1min_table 
      WHERE 
        timestamp < DATE_SUB( CURDATE(),INTERVAL 5 DAY );
    """
  )
  conn.commit()

  cur.execute(
    """
      DELETE FROM 
        5min_table 
      WHERE 
        timestamp < DATE_SUB( CURDATE(),INTERVAL 5 DAY );
    """
  )
  conn.commit()

  cur.execute(
    """
      DELETE FROM 
        got_data
      WHERE 
        timestamp < DATE_SUB( CURDATE(),INTERVAL 5 DAY );
    """
  )
  conn.commit()

if __name__ == "__main__":
    main()
