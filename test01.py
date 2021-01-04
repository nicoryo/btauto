import mysql.connector as mydb
import setting
from sshtunnel import SSHTunnelForwarder

API_KEY = setting.API_KEY
API_SECRET = setting.API_SECRET
RDShost = setting.RDShost
RDSpass = setting.RDSpass
RDSdb   = setting.RDSdb
RDSuser = setting.RDSuser

server = SSHTunnelForwarder(
    ('54.150.52.37', 22),
    ssh_host_key=None,
    ssh_username='ec2-user',
    ssh_password=None,
    ssh_pkey='./bitcoin_step_saver01.pem',
    remote_bind_address=(RDShost, 3306),
    local_bind_address=('127.0.0.1',10022)
)
print("server start")
server.start()
conn = mydb.connect(
    host    ='127.0.0.1',
    port    =10022,
    user    =RDSuser,
    password=RDSpass,
    database=RDSdb,
    charset="utf8"
)
# conn = mydb.connect(
#     host='127.0.0.1',
#     port=10022,
#     user='dbに繋ぐユーザ名',
#     db='db名',
#     passwd='dbのパスワード',
#     charset='utf8mb4'
# )
c = conn.cursor()
# テストで実行するSQL文
c.execute("SELECT BUYSig, SELLSig, close FROM 5min_table ORDER BY id DESC LIMIT 1;")
for row in c.fetchall():
    print(row)
conn.close()

server.stop()
