# coding:utf-8

import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):

    response = sns.publish(
        TopicArn='arn:aws:sns:ap-northeast-1:{AcountId}:{Name}',
        Message=u'Publishできました',
        Subject=u'LambdaからのPublish'
    )

    return 'return Hello from Lambda'
