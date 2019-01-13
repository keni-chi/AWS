# APIGateway

## 概要
Lambdaでvalidateを実装しなくてもAPIGatewayでモデルを作成すれば実装不要なことを調査した。
Swaggerを用いたデータのexport/importなども試した。

- 検証の設定方法
API Swagger 定義をインポートして基本的なリクエストの検証を設定する
API Gateway REST API を使用してリクエストの検証を設定する
API Gateway コンソールを使用して基本的なリクエストの検証を設定する

- API Gateway でモデルを作成する
API Gateway コンソールを使用してモデルを作成する

- モデル作成例
{
  "title": "controllersIdModel",
  "type": "object",
  "properties": {
    "Status": { "type": "string", "enum": ["dog", "cat"] }
  }
}