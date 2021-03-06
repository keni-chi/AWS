# Cloudformation

## 概要
以下などを行った。

- cloudformerでテンプレートリバース。

- DynamoDBのテンプレートを作成。デプロイおよびアンデプロイ用のMakefileを作成。

- troposphereを使ってテンプレート生成。


### 組み込み関数

#### Fn::GetAtt
テンプレートのリソースから属性の値を返します。
```
SourceSecurityGroupName: !GetAtt myELB.SourceSecurityGroup.GroupName
```

#### Fn::ImportValue
別のスタックによってエクスポートされた出力の値を返します。この関数は通常、クロススタック参照を作成するために使用されます。次のサンプルテンプレートスニペットでは、スタック A は VPC セキュリティグループ値をエクスポートし、スタック B はそれをインポートします。
```
Fn::ImportValue:
  !Sub "${NetworkStackName}-SecurityGroupID"
```

#### Fn::Sub
特定した値の入力文字列にある変数の代わりになります。テンプレートで、スタックを作成または更新するまで使用できない値を含むコマンドまたは出力を作成するために、この関数を使用できます。
```
Name: !Sub
  - www.${Domain}
  - { Domain: !Ref RootDomainName }
```

#### Ref
指定したパラメータまたはリソースの値を返します。
パラメーターの論理名を指定すると、それはパラメーターの値を返します。
リソースの論理名を指定すると、それはそのリソースを参照するために通常使用できる値を返します (物理 ID)。
テンプレートでリソースを宣言するときに別のテンプレートリソースを名前で指定する必要がある場合は、Ref を使用して別のリソースを参照できます。一般的に、Ref はリソースの名前を返します。たとえば、AWS::AutoScaling::AutoScalingGroup の参照は、Auto Scaling グループリソースの名前を返します。
```
MyEIP:
  Type: "AWS::EC2::EIP"
  Properties:
    InstanceId: !Ref MyEC2Instance
```


## 参考
[組み込み関数リファレンス](https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference.html)
