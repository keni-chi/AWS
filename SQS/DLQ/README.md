# DLQ検証

## 概要
DLQを用いたリトライ機能の仕様を明らかにすることを目的とする。

### 検証1
DLQを設定して動作確認をした。

- SQSの設定  
キューの属性：  標準キュー  
デフォルトの可視性タイムアウト：		10秒  
メッセージ保持期間：		3分  
配信遅延：		5秒  
メッセージ受信待機時間：		3秒  
最大受信数：		5

- 結果  
out.log の通り。  

### 検証2
DLQを設定せずに動作確認を行う。  

- 結果  
「メッセージ保持期間」の間リトライをし続けた。


### 検証3
- 前提
複数メッセージをSQSに積む。  

- 結果1
SQSトリガーのバッチサイズの設定を1にすると、lambdaが同時起動して並列で各メッセージを処理。

- 結果2
SQSトリガーのバッチサイズの設定を1より大きくすると、lambdaが複数メッセージを取得する場合がある。

```
{
  "Records": [
    {
      "messageId": "xxxxx",
      "receiptHandle": "xxxxx",
      "body": "msg_3",
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "xxxxx",
        "SenderId": "YYYYY",
        "ApproximateFirstReceiveTimestamp": "YYYYY"
      },
      "messageAttributes": {},
      "md5OfBody": "xxxxx",
      "eventSource": "aws:sqs",
      "eventSourceARN": "xxxxx",
      "awsRegion": "ap-northeast-1"
    },
    {
      "messageId": "xxxxx",
      "receiptHandle": "xxxxx",
      "body": "msg_1",
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "xxxxx",
        "SenderId": "YYYYY",
        "ApproximateFirstReceiveTimestamp": "YYYYY"
      },
      "messageAttributes": {},
      "md5OfBody": "xxxxx",
      "eventSource": "aws:sqs",
      "eventSourceARN": "xxxxx",
      "awsRegion": "ap-northeast-1"
    }
  ]
}
```
