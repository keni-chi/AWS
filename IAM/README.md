# IAM

## 概要
覚書である。順次記載予定。

### 設定

- credentials

[{任意１}]
aws_access_key_id = xxxxxxxx
aws_secret_access_key = xxxxxxxx

[{任意A}]
source_profile = {任意１}
role_arn = arn:aws:iam::{アカウントID}:role/{ロール名}

- config

[{任意A}]
region = ap-northeast-1
output = json

[default]
region = ap-northeast-1
output = json



## 参考
[サービス間の認証を API Gateway + IAM で行う](https://qiita.com/paper2/items/cea6021512132f070403)  
[完全なバージョン 4 署名プロセスの例 (Python)](https://docs.aws.amazon.com/ja_jp/general/latest/gr/sigv4-signed-request-examples.html)  
[API Gatewayでリソースポリシーを使ったアクセス制御をやってみたい](https://qiita.com/Hikosaburou/items/9cc2d65166bd7e3044b8)
