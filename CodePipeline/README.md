## CodeBuild, CodePipeLine

## 概要
覚書である。

### 詳細

1. CodeBuild用のロールを作成しておく

1. CodeCommitのリポジトリ直下にbuildspec.ymlをpushしておく。
```
version: 0.1 
phases: 
  install: 
    commands: 
      - pip install chalice 
      - pip install boto3 
      - chalice deploy 
```

3. CodeBuildにて以下の通り設定。  
Project configuration  
  Project name  
Source   
  Source provider: AWS CodeCommit  
  Repository: 任意のリポジトリ  
Environment  
  用意したロール(codebuild.amazonaws.com)  
Buildspec  
  Use a buildspec file  
  buildspec.yml  
Artifacts  
  S3  
  Bucket name  
  Name- オプショナル  
  Namespace type - オプショナル  
    Build ID  
  Artifacts packaging  
    なし  
Logs  
  デフォルト  

4. CodePipeLineにて以下の通り設定。  
パイプライン名  
  ソースステージを追加する  
    アクション名  
    ソースプロバイダー  AWS CodeCommit  
    リポジトリ名  任意  
    ブランチ名  master  
    検出オプションを変更する  Amazon CloudWatch Events（推奨）  
    出力アーティファクト  MyApp  
  ビルドステージを追加する  
    プロバイダーを構築する  AWS CodeCommit  
    リージョン  
    プロジェクト名  
  デプロイステージを追加する  
    デプロイ ステージをスキップする  
