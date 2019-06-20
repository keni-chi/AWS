# IoTcore

## 概要
覚書である。IoTcoreについて記載する。

## 手動設定
1. IAMロールを作成しておく。  
IAMロール内容の例
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

4. ロールエイリアスを作成する。  
 - 名前をつける。URLの一部となる。  
 - 紐づけるIAMロールを設定する。  

5. ポリシーを作成し、証明書にアタッチする。  
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

## JITR
[AWS IoT 証明書のJust In Time登録](https://qiita.com/TakashiKOYANAGAWA/items/b3b679e2a7d56f144a8e)   

### registration codeを取得  
- ここで取得する registration codeをCAのCN(Common Name)で利用。  
  - aws iot get-registration-code  

### 認証局
- 秘密鍵(CAroot.key)  
openssl genrsa -out CAroot.key 2048  
- 証明書(CAroot.pem)  
openssl req -x509 -new -nodes -key CAroot.key -sha256 -days 365 -out CAroot.pem  
- 参考  
  - 秘密鍵の確認  
    - openssl rsa -in CAroot.key -text  

### 中間証明書(プライベートキー検証証明書)
- 秘密鍵(Verify.key)  
openssl genrsa -out Verify.key 2048  
- 証明書署名要求(Verify.csr)  
openssl req -new -key Verify.key -out Verify.csr  
- 証明書(署名の実行)(Verify.crt)(CAroot.srl)  
openssl x509 -req -in Verify.csr -CA CAroot.pem -CAkey CAroot.key -CAcreateserial -out Verify.crt -days 365 -sha256  
証明書=署名付き公開鍵。公開鍵が誰の公開鍵であるかを証明している。  
CAroot.srlは、CA（認証局）が使用するシリアルナンバーのファイル。  
- 参考  
  - 証明書の内容をテキストで表示する  
    - openssl x509 -noout -text -in Verify.crt  

### 作成したルート証明書、中間証明書をAWS IoTへ登録
- 証明書をAWS IoTへ登録  
aws iot register-ca-certificate --ca-certificate file://CAroot.pem --verification-certificate file://Verify.crt  
- statusとautoRegistrationStatusが有効化されていないので、これらを以下のコマンド有効にする。  
aws iot update-ca-certificate --certificate-id $YOUR_CA_CERT_ID --new-status ACTIVE  
aws iot update-ca-certificate --certificate-id $YOUR_CA_CERT_ID --new-auto-registration-status ENABLE  

### Device用証明書
- 秘密鍵(deviceCert.key)  
openssl genrsa -out deviceCert.key 2048  
- 証明書署名要求(deviceCert.csr)  
openssl req -new -key deviceCert.key -out deviceCert.csr  
- 証明書(署名の実行)(deviceCert.crt)  
openssl x509 -req -in deviceCert.csr -CA ../CA/CAroot.pem -CAkey ../CA/CAroot.key -CAcreateserial -out deviceCert.crt -days 365 -sha256   
- Just in Timeで利用する証明書を作成  
cat deviceCert.crt ../CA/CAroot.pem > deviceCertAndCA.crt  


## JITP
[自前の証明書を使用する](https://docs.aws.amazon.com/ja_jp/iot/latest/developerguide/device-certs-your-own.html)  
[Setting Up Just-in-Time Provisioning with AWS IoT Core](https://aws.amazon.com/jp/blogs/iot/setting-up-just-in-time-provisioning-with-aws-iot-core/)    
[ジャストインタイムのプロビジョニング](https://docs.aws.amazon.com/ja_jp/iot/latest/developerguide/jit-provisioning.html)    

＜凡例＞

>はファイルシュル直の例を示す。  

>>はコンソール出力の例を示す。

### クラウド構築
ロールを作成  
IoTポリシーを作成  
ロールエイリアスを作成  
マネージメントコンソールで初期認証APIのAPIGatewayへ移動し、IAM認証を有効化。デプロイする。  

### CA 証明書を作成
openssl genrsa -out rootCA.key 2048
>rootCA.key

openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem
>rootCA.pem

### CA 証明書の登録
aws iot get-registration-code
>> "registrationCode": "xxxxxxxx"

openssl genrsa -out verificationCert.key 2048
>verificationCert.key

openssl req -new -key verificationCert.key -out verificationCert.csr  
Common Name (eg, your name or your server's hostname) []:xxxxxxxx
>verificationCert.csr

openssl x509 -req -in verificationCert.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out verificationCert.pem -days 500 -sha256
>>Signature ok  
>>subject=/C=XX/L=Default City/O=Default Company Ltd/CN=xxxxxxxx  
>>Getting CA Private Key  
>rootCA.srl  
>verificationCert.pem  

provisioning-template.jsonを準備  

aws iot register-ca-certificate --ca-certificate file://rootCA.pem --verification-cert file://verificationCert.pem --set-as-active --allow-auto-registration --registration-config file://jitp-template.json  
注意: CA証明書は10個まで登録可能  
>>"certificateArn": "arn:aws:iot:ap-northeast-1:yyyyy",  
>>"certificateId": "zzzzzzz"


### CA 証明書を使用してデバイス証明書を作成する
openssl genrsa -out deviceCert.key 2048
>deviceCert.key

openssl req -new -key deviceCert.key -out deviceCert.csr
Common Name (eg, your name or your server's hostname) []:testThingxxxx
>deviceCert.csr

openssl x509 -req -in deviceCert.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out deviceCert.crt -days 500 -sha256
>>Signature ok
>>subject=/C=XX/L=Default City/O=Default Company Ltd/CN=testThingxxxx
>>Getting CA Private Key
>deviceCert.crt

cat deviceCert.crt rootCA.pem > deviceCertAndCACert.crt
>deviceCertAndCACert.crt


### ロール取得
aws iot describe-endpoint --endpoint-type iot:CredentialProvider  
>> "endpointAddress": "aaaaaaaaaaaaa.credentials.iot.ap-northeast-1.amazonaws.com"

ローカルPCへ証明書をダウンロード(deviceCert.key, deviceCertAndCACert.crtが必要。)  

curl -v --cert deviceCertAndCACert.crt --key deviceCert.key -H "x-amzn-iot-thingname: testThinga01" https://aaaaaaaaaaaaa.credentials.iot.ap-northeast-1.amazonaws.com/role-aliases/bbbbbbbbb/credentials  

>>正常  
>>{"credentials":{"accessKeyId":"ccccccccccccc","secretAccessKey":"dddddddddd","sessionToken":"eeeeeeeeee","expiration":"fffffff"}}


## APIアクセス
Postmanを起動し、以下の通り設定。  

  ・TYPEで「AWS Signature」を選択。  
  ・URL  
  https://ggggggg  
  POST  
  ・ヘッダの設定  
  Content-Type   application/json  
  Bodyの設定
  ```
  {
    "hhhh": "iiiii"
  }
  ```
  ・認証情報の設定  
  AccessKey　レスポンス値を入力。  
  SecretKey　レスポンス値を入力。  
  AWS Region　ap-northeast-1  
  (Service Name　execute-api)  
  Session Token　レスポンス値を入力。



## 参考
[RSA鍵、証明書のファイルフォーマットについて](https://qiita.com/kunichiko/items/12cbccaadcbf41c72735)  S
[AWS サービスの直接呼び出しの承認](https://docs.aws.amazon.com/ja_jp/iot/latest/developerguide/authorizing-direct-aws.html)  
[AWS GreengrassでLチカ：クラウドとエッジについて考える(1)](https://qiita.com/nobu_e753/items/4c0b0643f6d225daa067)
