# localstack

## 概要
覚書である。順次記載予定。

### 構築手順  
- インストール  
```  
git clone https://github.com/atlassian/localstack.git  
cd localstack  
```  
- "docker-compose up"ではエラーになるので以下のコマンドを打つ  
```  
TMPDIR=/private$TMPDIR docker-compose up  
```  
- "http://localhost:8080" にアクセスして確認。  

### Lambda作成
- .pyを作成  
- .zipに圧縮  
- 以下のコマンドを打つ  
```  
aws --endpoint-url=http://localhost:4574 --region ap-northeast-1 --profile localstack lambda create-function --function-name=f1 --runtime=python3.7 --role=r1 --handler=lambda.lambda_handler --zip-file fileb://lambda.zip
```  

### 実行
```  
aws lambda --endpoint-url=http://localhost:4574 invoke --function-name f1 --payload '{"key1":"value1", "key2":"value2", "key3":"value3"}' result.log
```  

## 参考
[環境構築](https://dev.classmethod.jp/cloud/aws/localstack-lambda/)
