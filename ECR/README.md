# ECR

## 概要
覚書である。順次記載予定。


### 詳細

================
CLI
https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/installing.html
================
pip install awscli --upgrade --user
aws --version
pip install awscli --upgrade --user

================
Credential設定
https://dev.classmethod.jp/cloud/aws-cli-credential-config/
================
aws configure

=====================================================================================
ECR
https://qiita.com/3utama/items/b19e2239edb6996a735f
=====================================================================================

aws ecr get-login --no-include-email --region ap-northeast-1

docker login -u AWS -p {xxxxx} https://{account_id}.dkr.ecr.ap-northeast-1.amazonaws.com

ここでビルドする（dockerメモを参照）
docker tag aws_account_id.dkr.ecr.us-east-1.amazonaws.com/amazon-ecs-sample:latest {account_id}.dkr.ecr.ap-northeast-1.amazonaws.com/practice02ecr:latest

docker push {account_id}.dkr.ecr.ap-northeast-1.amazonaws.com/practice02ecr:latest
