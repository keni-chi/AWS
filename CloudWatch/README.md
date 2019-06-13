# CloudWatch

## awslogs
awslogsでログ収集し、テキストへ出力するメモである。

- コマンド  
pip install awslogs  
awslogs get -w {ロググループ名} >> output.log

- フィルター、時間範囲指定 2018/10/3 10:40 ～ 2018/10/3 10:45 の間で、“Duration” を含むログを抽出する。  
awslogs get -f “Duration” -G -S --start='Oct 03, 2018 10:40' --end='Oct 03, 2018 10:45' --timestamp {ロググループ名}


## 参考
[ターミナルから直感的にCloudWatch Logsを検索できるawslogsコマンドの紹介](https://dev.classmethod.jp/cloud/aws/show-cloudwatch-logs-with-awslogs-command/)
