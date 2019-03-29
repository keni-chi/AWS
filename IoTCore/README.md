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

## 方法１
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

### 作成したルート証明書、中間証明書をAWS IoTへ登録(JITR)
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


## 方法２
[自前の証明書を使用する](https://docs.aws.amazon.com/ja_jp/iot/latest/developerguide/device-certs-your-own.html)  
[Setting Up Just-in-Time Provisioning with AWS IoT Core](https://aws.amazon.com/jp/blogs/iot/setting-up-just-in-time-provisioning-with-aws-iot-core/)    
[ジャストインタイムのプロビジョニング](https://docs.aws.amazon.com/ja_jp/iot/latest/developerguide/jit-provisioning.html)    

### CA 証明書を作成
openssl genrsa -out rootCA.key 2048  
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem

### CA 証明書の登録
aws iot get-registration-code
openssl genrsa -out verificationCert.key 2048
openssl req -new -key verificationCert.key -out verificationCert.csr  (Common Nameに「registration-code」を入力)
openssl x509 -req -in verificationCert.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out verificationCert.pem -days 500 -sha256

aws iot register-ca-certificate --ca-certificate file://rootCA.pem --verification-cert file://verificationCert.pem --set-as-active --allow-auto-registration --registration-config file://jitp-template.json

### CA 証明書を使用してデバイス証明書を作成する
openssl genrsa -out deviceCert.key 2048
openssl req -new -key deviceCert.key -out deviceCert.csr  (Common Nameに「thingName」を入力)
openssl x509 -req -in deviceCert.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out deviceCert.crt -days 500 -sha256
cat deviceCert.crt rootCA.pem > deviceCertAndCACert.crt

### 動作確認
- endPointを調べる
  aws iot describe-endpoint
<!-- - amazon linuxにmosquiito_clientを入れるには、以下のコマンドを実行
  sudo curl http://download.opensuse.org/repositories/home:/oojah:/mqtt/CentOS_CentOS-6/home:oojah:mqtt.repo -o /etc/yum.repos.d/mqtt.repo
  sudo yum install -y mosquitto-clients mosquitto
- publishする
  mosquitto_pub --cafile root.cert --cert deviceCertAndCACert.crt --key deviceCert.key -h <prefix>.iot.us-east-1.amazonaws.com -p 8883 -q 1 -t foo/bar -I anyclientID --tls-version tlsv1.2 -m "Hello" -d
  以下にpublishされる
    $aws/events/certificates/registered/caCertificateID
      {
        "certificateId": "certificateID",
        "caCertificateId": "caCertificateId",
        "timestamp": timestamp,
        "certificateStatus": "PENDING_ACTIVATION",
        "awsAccountId": "awsAccountId",
        "certificateRegistrationTimestamp": "certificateRegistrationTimestamp"
      } -->


## 参考
[RSA鍵、証明書のファイルフォーマットについて](https://qiita.com/kunichiko/items/12cbccaadcbf41c72735)
[AWS サービスの直接呼び出しの承認](https://docs.aws.amazon.com/ja_jp/iot/latest/developerguide/authorizing-direct-aws.html)  
