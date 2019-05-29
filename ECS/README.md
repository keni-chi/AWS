
## 概要
性能にかかわる設定メモを以下に示す。

■ECS			
	タスク定義		
		タスクメモリ：　デフォルト	
		タスクCPU：　デフォルト	
		コンテナ	
			メモリ制限(MB)：ハード制限512
	クラスタ		
		インスタンスタイプ：　m4.large	
		インスタンス数：　1	
	サービス		
		タスク数：１	
		サ－ビスタイプ：　DAEMON	
	スケジュール		
		```15分毎  cron(0/15 * * * ? *)
		```

## 参考
[ECS運用のノウハウ](https://qiita.com/naomichi-y/items/d933867127f27524686a)  
[AWSECSを利用し、コンテナのログをCloudWatch Logsへ出力する](https://dev.classmethod.jp/cloud/aws/ecs-cloudwatch-logs/)
