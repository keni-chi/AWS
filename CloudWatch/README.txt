-----------------
awslogs
-----------------
awslogsでログ収集し、テキストへ出力するメモである。

# 参考文献 https://dev.classmethod.jp/cloud/aws/show-cloudwatch-logs-with-awslogs-command/
pip install awslogs
awslogs get -w /aws/lambda/ite3naga1-CurrentEquipmentStateGet >> current_equipment_state_get_multi_resource.log
