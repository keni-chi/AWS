# Lambda
  
## 概要  
覚書である。順次記載予定。  

### イベント    

| AWSサービス                             | ポーリング | 非同期 | 同期 |
|:----------------------------------------|:-----------|:-------|:-----|
| S3                                      |            | ○      |      |
| DynamoDB                                | ○          |        |      |
| Kinesis Data Streams                    | ○          |        |      |
| SNS                                     |            | ○      |      |
| SES                                     |            | ○      |      |
| SQS                                     | ○          |        |      |
| Cognito                                 |            |        | ○    |
| CloudFormation                          |            |        | ○    |
| CloudWatch Logs                         |            |        | ○    |
| CloudWatch イベント                     |            | ○      |      |
| CodeCommit                              |            | ○      |      |
| スケジュール (CloudWatch Events を使用) |            | ○      |      |
| Config                                  |            | ○      |      |
| Alexa                                   |            |        | ○    |
| Lex                                     |            |        | ○    |
| API Gateway                             |            |        | ○    |
| IoT ボタン                              |            | ○      |      |
| CloudFront                              |            |        | ○    |
| Kinesis Data Firehose                   |            |        | ○    |
  
## 参考   
https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/invoking-lambda-function.html