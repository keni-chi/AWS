import boto3
from datetime import datetime

SQS_NAME = 'nagatest'

def lambda_handler(event, context):
    sqs_sends()


def sqs_sends():
    print('Input--------------------start')
    now = datetime.utcnow()
    now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.%fZ')
    print('Input-start:  ' + now_str)

    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=SQS_NAME)
    data = '{\"k\": \"v\"}'
    msg_list = [{'Id': '1', 'MessageBody': data}]
    response = queue.send_messages(Entries=msg_list)

    now = datetime.utcnow()
    now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.%fZ')
    print('Input-end:    ' + now_str)
    print('Input--------------------end')
