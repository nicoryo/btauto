import datetime
import schedule
import time
import adjustMysql
import create5minchart
import create1minchart
import getTicker

schedule.every().day.at("12:00").do(adjustMysql.main)

schedule.every(10).seconds.do(getTicker.main)
schedule.every(1).minutes.do(create1minchart.main)
schedule.every(5).minutes.do(create5minchart.main)

while True:
  schedule.run_pending()
  time.sleep(1)