# Cognito

## 概要
覚書である。順次記載予定。

### 詳細

プール ID
ap-northeast-1_{xxxxxxx}
プール
ARN arn:aws:cognito-idp:ap-northeast-1:{accountId}:userpool/ap-northeast-1_{xxxxxxx}
アプリクライアント ID
{xxxxxxxxxxxxxxxxxxxx}

■CLI
aws cognito-idp sign-up --client-id ＜作成したClientId＞ --username user01 --password 00000000 --user-attributes Name=email,Value=＜任意のEmailアドレス＞
aws cognito-idp admin-confirm-sign-up --user-pool-id ＜作成したPoolId＞ --username user01

aws cognito-idp sign-up --client-id {xxxxxxxxxxxxxxxxxxxx} --username user01 --password {yyyyyyy} --user-attributes Name=email,Value={mailAddr}
aws cognito-idp admin-confirm-sign-up --user-pool-id ap-northeast-1_{xxxxxxx} --username user01

==================================

■画面で作成
user012
{password}

■APIGateway
名称
Practice01dcogAuthlizer
Authorization

■APIのエンドポイント
https://{xxxxx}.execute-api.ap-northeast-1.amazonaws.com/prod

■aclをcliで設定
aws s3api put-bucket-acl --acl private --bucket {aaaa}
aws s3api put-bucket-acl --acl public-read --bucket {aaaa}
