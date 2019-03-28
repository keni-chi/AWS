# IoTcore

## 概要
覚書である。IoTcoreについて記載する。

### アクセス手順
1. IAMポリシーを作成しておく。  
IAMポリシー内容の例
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "execute-api:Invoke",
            "Resource": "arn:aws:execute-api:ap-northeast-1:*:*/*/POST/{URI}"
        }
    ]
}
```

2. モノを作成する。任意の名称をつける。

3. 証明書を作成して以下を保存する。(モノを作成する続き)
 - certificate.pem.crt  
 - private.pem.key  
 
5. ロールエイリアスを作成する。  
 - 名前をつける。URLの一部となる。  
 - 紐づけるIAMロールを設定する。  

4. ポリシーを作成し、証明書にアタッチする。  
ポリシー内容の例
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:AssumeRoleWithCertificate",
      "Resource": "arn:aws:iot:ap-northeast-1:{account-id}:rolealias/{ロールエイリアス}",
      "Condition": {
        内容
      }
    }
  ]
}
```
