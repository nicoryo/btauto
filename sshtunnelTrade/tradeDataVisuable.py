import mysql.connector as mydb
import setting
from sshtunnel import SSHTunnelForwarder
import matplotlib.pyplot as plt
import datetime

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
RDShost = setting.RDShost
RDSpass = setting.RDSpass
RDSdb   = setting.RDSdb
RDSuser = setting.RDSuser

interval = 60
# coding:utf-8
# コネクションの作成
server = SSHTunnelForwarder(
    ('54.150.52.37', 22),
    ssh_host_key=None,
    ssh_username='ec2-user',
    ssh_password=None,
    ssh_pkey='bitcoino1pem.pem',
    remote_bind_address=(RDShost, 3306),
    local_bind_address=('127.0.0.1',10022)
)

server.start()
print("STEP1 server start")
conn = mydb.connect(
    host    ='127.0.0.1',
    port    =10022,
    user    =RDSuser,
    password=RDSpass,
    database=RDSdb,
    charset="utf8"
)
print('STEP2 get cursor')
# カーソルを取得する
cur = conn.cursor()

cur.execute("SELECT timestamp, close, MACD, MACDSignal FROM 5min_table ORDER BY id DESC LIMIT 144 ;")
# cur.execute("SELECT timestamp, close, MACD, MACDSignal FROM 1min_table ORDER BY id DESC LIMIT 180 ;")
row = cur.fetchall()

# print(row[1][1])
x_date = []
y_MACD = []
y2_MACD_signal = []
y3_close_price = []

conn.commit()
cur.close()
conn.close()
server.stop()
for i in reversed(range(144)):
    x_date.append(row[i][0])
    y_MACD.append(row[i][-2])
    y2_MACD_signal.append(row[i][-1])
    y3_close_price.append(row[i][1])

# print(y_MACD)
data1 = x_date,y_MACD
data2 = x_date, y2_MACD_signal
data3 = x_date,y3_close_price

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # 2つのプロットを関連付ける
ax1.plot(x_date,y_MACD,linewidth=2, color="red",label='MACD')
ax1.plot(x_date,y2_MACD_signal, linewidth=2, color="orange", label='MACD_signal')
ax2.plot(x_date,y3_close_price, linewidth=2, color="green", label='close_price')

# 凡例
ax1.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0.5, fontsize=10)
ax2.legend(bbox_to_anchor=(0, 0.85), loc='upper left', borderaxespad=0.5, fontsize=10)

#軸ラベルを表示
plt.xlabel('date')
ax1.set_ylabel('MACD')
ax2.set_ylabel('close price')
# plt.plot(x_date,y_MACD)
# plt.plot(x_date,y2_MACD_signal)
# plt.plot(x_date,y3_close_price)
plt.show()



