# 参考: https://dev.classmethod.jp/cloud/aws/boto3_sqs_lambda_schedule_trial/
import boto3
import json
import gzip

SQS_TESTTEST = 'testtest'



def sqs_sends():
    sqs = boto3.resource('sqs')
    try:
        # キューの名前を指定してインスタンスを取得
        queue = sqs.get_queue_by_name(QueueName=SQS_TESTTEST)
    except:
        # 指定したキューがない場合はexceptionが返るので、キューを作成
        queue = sqs.create_queue(QueueName=SQS_TESTTEST)
     
    # メッセージ×3をキューに送信
    msg_num = 3
    # msg_list = [{'Id' : '{}'.format(i+1), 'MessageBody' : 'msg_{}'.format(i+1)} for i in range(msg_num)]
    msg_list = [{'Id': '11', 'MessageBody': '12'}, {'Id': '21', 'MessageBody': '22'}]
    response = queue.send_messages(Entries=msg_list)
    print(response)


def sqs_recieve():
    """sqs_recieve.

    以下は実行例。
    sqs_recieve--------------------start
    sqs_recieve------
    12
    sqs_recieve------
    22
    sqs_recieve--------------------end

    """
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=SQS_TESTTEST)
    while True:
        # メッセージを取得
        msg_list = queue.receive_messages(MaxNumberOfMessages=10)
        if msg_list:
            for message in msg_list:
                print('sqs_recieve------')
                print(message.body)
                message.delete()
        else:
            # メッセージがなくなったらbreak
            break


def main():
    """main."""
    
    # sqs_sends
    print('sqs_sends--------------------start')
    sqs_sends()
    print('sqs_sends--------------------end')

    # sqs_recieve
    print('sqs_recieve--------------------start')
    sqs_recieve()
    print('sqs_recieve--------------------end')



if __name__ == '__main__':
    main()


