# installation
## pip install 
* pip install mysql-connector-python
* pip snstall mysqlclient
* pip install pybitflyer
* pip install python-dotenv
* pip install schedule
* pip install sshtunnel
* pip install requests

## .env
api_key="自分のBitflyer API KEY"
api_secret_key="自分のBitflyer API SECRET KEY"
line_key = "自身のライン Notifyキー"

下記は、製作者の私に要問い合わせ
RDS
RDShost     =
RDSpass     =
RDSdb       =
RDSuser     =

## RDSへのアクセス方法
* EC2の踏み台サーバのキーを製作者にもらう
* .pemファイルをsshtunnelTradeディレクトリへ格納する

## 自動売買ツールを起動する
$ python judgeAlgorithm.py