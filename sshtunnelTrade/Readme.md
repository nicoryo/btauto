# installation

## pip install 
* pip install mysql-connector-python
* pip snstall mysqlclient
* pip install pybitflyer
* pip install python-dotenv
* pip install schedule
* pip install sshtunnel
* pip install requests
* pip install matplotlib

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


## bitflyer API
下記記事を参考にして、API KeyとAPI Secretを入手する
参考記事
https://cryptolinc.com/faq_cases/bitflyer_api_setting

## Line notify
[https://notify-bot.line.me/ja/](https://notify-bot.line.me/ja/)
アカウント作成後、マイページ > トークンを発行する > トークン名、トークルームを設定 > 発行する
発行されたトークンをコピーしておく。
一度切りしか表示されないので、必ずコピーして置くこと。
消しちゃった場合は再発行する。