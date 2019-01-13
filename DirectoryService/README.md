# DirectoryService

## 概要

- SimpleAd, Microsoft ADなどを実際に構築などしてみた。

- AD応用調査

	- 要件
	RedmineやGitLabとID,Passwordを共通にし、AWS ActiveDirectoryで一元管理したい。

	- 疑問
	具体的な「Cognito User PoolのSAML Provider」を使った認証認可システムの実現方法についての疑問。(※特に＜詳細＞の１～３について)

		- 概要
		AWSDirectoryServiceを使うことが前提の場合、Cognitoを使ったとしてもIdPとなるサーバ用のEC2を立てる必要があり、
		完全にサーバレスな認証認可アーキテクチャは実現できないのではないか。
		一方で、AWS DirectoryServiceには「Amazon Cloud Directory、Amazon Cognito Your User Pools、
		Microsoft AD、Simple AD、AD Connector」と５種類あり、どれかを使ってしっかり設定すればサーバレスで実現できそう？

		- 詳細（実現できないかもしれないと思った理由）
		１．IAMのプロバイダの作成が必要であり、その時、メタデータドキュメントのファイル選択をする必要があると認識。
		２．そのファイルを用意するには、ADFSからSAML用Metadata(ADFSサーバーのフェデレーションメタデータ)をダウンロードする必要がある。
		３．SAML用Metadataを用意するためには、EC2上にIdPとなるサーバが必要ではないか。（IdPとなるサーバをAWS DirectoryServiceで代用できるか？）

