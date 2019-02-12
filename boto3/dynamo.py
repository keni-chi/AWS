# coding: utf-8
import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr

TABLE_TESTTEST = 'testtest'


def dynamo_insert(file_path, file_name, table_name):
    """dynamo_insert."""
    client = boto3.resource('dynamodb')
    table = client.Table(table_name)

    file = file_path + '/' + file_name
    f = open(file)
    json_data = json.load(f)
    f.close()

    response = table.put_item(Item=json_data)

    response = {
        'pk': json_data['pk'],
        'at1': json_data['at1']
    }
    return response


def dynamo_insert_sample():
    """dynamo_insert_sample."""
    path_data = os.getcwd() + '/file/'
    res = dynamo_insert(path_data, 'testtest.json', TABLE_TESTTEST)
    print(res)


def dynamo_query(partition_key,sort_key):
    resource = boto3.resource('dynamodb')
    table = resource.Table(TABLE_TESTTEST)

    queryData = table.query(
        KeyConditionExpression = Key('pk').eq(partition_key)& Key('sk').eq(sort_key)
    )
    item = queryData['Items']
    return item


def dynamo_query_sample():
    """dynamo_query_sample."""
    res = dynamo_query('pk_v', 'sk_v')
    print(res)


def dynamo_scan():
    """dynamo_scan."""
    from boto3.session import Session
    session = Session()
    dynamodb = session.resource('dynamodb')

    dynamodb_table = dynamodb.Table(TABLE_TESTTEST)
    res = dynamodb_table.scan()
    print(res)


def dynamo_update():
    resource = boto3.resource('dynamodb')
    table = resource.Table(TABLE_TESTTEST)    
    
    # ネストされているdictのvalueを書き換える更新
    res = table.update_item(
        Key={
            'pk': 'pk_v',
            'sk': 'sk_v'
        },
        UpdateExpression="set at3.rating = :r, at3.plot=:p, at3.actors=:a",
        ExpressionAttributeValues={
            ':r': 10,
            ':p': "p value test",
            ':a': ["a", "b", "c"]
        },
        ReturnValues="UPDATED_NEW"
    )
    print(res)

    # 属性を追加する更新
    res = table.update_item(
        Key={
            'pk': 'pk_v',
            'sk': 'sk_v'
        },
        UpdateExpression='ADD attribute_new :at_new_k',
        ExpressionAttributeValues={':at_new_k': {"at_new_v"}}
    )
    print(res)

    # 更新付き更新(ratingのvalueが0より大きければ、ratingをdictごと削除)
    res = table.update_item(
        Key={
            'pk': 'pk_v',
            'sk': 'sk_v'
        },
        UpdateExpression="remove at3.rating",
        ConditionExpression="at3.rating > :num",
        ExpressionAttributeValues={
            ':num': 0
        },
        ReturnValues="UPDATED_NEW"
    )
    print(res)


def dynamo_delete():
    resource = boto3.resource('dynamodb')
    table = resource.Table(TABLE_TESTTEST)    

    # 更新付き削除(at2がat2_vであれば、itemを削除)
    res = table.delete_item(
        Key={
            'pk': 'pk_v',
            'sk': 'sk_v'
        },
        ConditionExpression="at2 = :val",
        ExpressionAttributeValues= {
            ":val": "at2_v"
        }
    )
    print(res)


def dynamo_batch_write():
    try:
        resource = boto3.resource('dynamodb')
        table = resource.Table(TABLE_TESTTEST)
        with table.batch_writer() as batch:
            for i in range(10):
                batch.put_item(
                    Item={
                        'pk': 'pk' + str(i),
                        'sk': 'sk' + str(i),
                        'LSI1': 1000000 + i,
                        'LSI2': 2000000 + i,
                        'LSI3': 3000000 + i,
                        'GSI1': 4000000 + i,
                        'GSI2': 5000000 + i,
                        'GSI3': 6000000 + i,
                        'GSI4': 7000000 + i,
                        'GSI5': 8000000 + i
                    }
                )
    except Exception as error:
        raise error


def dynamo_batch_get():
    # from time import sleep
    # sleep(1)
    dynamodb = boto3.resource('dynamodb', "ap-northeast-1")
    res = dynamodb.batch_get_item(
        RequestItems={
            TABLE_TESTTEST: {
                'Keys': [
                        {'pk':'pk0', 'sk':"sk0"},
                        {'pk':'pk1', 'sk':"sk1"}
                    ]
                }
        })
    print(res['Responses'])


def dynamo_delete_all():
    table = boto3.resource('dynamodb').Table(TABLE_TESTTEST)
    datas = dynamo_scan_all()
    for data in datas:
        table.delete_item(Key={'pk': data['pk'], 'sk': data['sk']})


def dynamo_scan_all():
    table = boto3.resource('dynamodb').Table(TABLE_TESTTEST)
    result = table.scan()
    return result['Items']


def main():
    """main."""

    # dynamo_insert_sample
    print('dynamo_insert_sample--------------------start')
    dynamo_insert_sample()
    print('dynamo_insert_sample--------------------end')

    # dynamo_query_sample
    print('dynamo_query_sample--------------------start')
    dynamo_query_sample()
    print('dynamo_query_sample--------------------end')

    # dynamo_scan
    print('dynamo_scan--------------------start')
    dynamo_scan()
    print('dynamo_scan--------------------end')

    # dynamo_update
    print('dynamo_update--------------------start')
    dynamo_update()
    print('dynamo_update--------------------end')

    # dynamo_delete
    print('dynamo_delete--------------------start')
    dynamo_delete()
    print('dynamo_delete--------------------end')

    # dynamo_batch_write
    print('dynamo_batch_write--------------------start')
    dynamo_batch_write()
    print('dynamo_batch_write--------------------end')

    # dynamo_batch_get
    print('dynamo_batch_get--------------------start')
    dynamo_batch_get()
    print('dynamo_batch_get--------------------end')

    # dynamo_delete_all
    print('dynamo_delete_all--------------------start')
    dynamo_delete_all()
    print('dynamo_delete_all--------------------end')



if __name__ == '__main__':
    main()
