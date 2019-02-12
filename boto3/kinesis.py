import boto3
import json
import gzip

STREAM_TESTTEST = 'testtest'


def kinesis_put_record():

    try:
        data ={"k": "v"}
        data_str = json.dumps(data)
        data_str_b = data_str.encode('utf-8')
        # data_zip = gzip.compress(data_str_b)

        res = boto3.client('kinesis').put_record(
            StreamName = STREAM_TESTTEST,
            Data = data_str_b,
            # Data = data_zip,
            PartitionKey = "pk001",
        )
        print(res)
        return res
    except Exception as e:
        raise e


def kinesis_put_records():

    try:
        data_list = [{"k1": "v1"}, {"k2": "v2"}]
        records = [
            {
                'Data': json.dumps(d) if type(d) in [list, dict] else d,
                'PartitionKey': "pk001"
            } for d in data_list
        ]

        res = boto3.client('kinesis').put_records(
            StreamName=STREAM_TESTTEST,
            Records=records
        )
        print(res)
        return res
    except Exception as e:
        raise e


def kinesis_get_records(timestamp):
    import time

    client_kinesis = boto3.client('kinesis')

    data_list = []

    stream = client_kinesis.describe_stream(StreamName=STREAM_TESTTEST)
    shards = stream['StreamDescription']['Shards'][0]['ShardId']

    kinesis_iterator = client_kinesis.get_shard_iterator(
        StreamName=STREAM_TESTTEST,
        ShardIteratorType="AT_TIMESTAMP",
        Timestamp=timestamp,
        ShardId=shards
    )

    next_iterator = None
    response = None
    while True:
        if next_iterator is None:
            next_iterator = kinesis_iterator['ShardIterator']
        else:
            next_iterator = response['NextShardIterator']

        response = None
        response = client_kinesis.get_records(ShardIterator=next_iterator, Limit=123)
        if len(response['Records']) == 0:
            break
        for record in response['Records']:
            data_list.append(record['Data'])
        time.sleep(1)

    return data_list


def kinesis_get_records_sample():
    import datetime
    tz = datetime.timezone.utc
    now = datetime.datetime.now(tz)
    res_record = kinesis_get_records(now)
    print(res_record)


def main():
    """main."""
    
    # kinesis_put_record
    print('kinesis_put_record--------------------start')
    kinesis_put_record()
    print('kinesis_put_record--------------------end')

    # kinesis_get_records_sample
    print('kinesis_get_records_sample--------------------start')
    kinesis_get_records_sample()
    print('kinesis_get_records_sample--------------------end')

    # kinesis_put_records
    print('kinesis_put_records--------------------start')
    kinesis_put_records()
    print('kinesis_put_records--------------------end')

    # kinesis_get_records_sample
    print('kinesis_get_records_sample--------------------start')
    kinesis_get_records_sample()
    print('kinesis_get_records_sample--------------------end')


if __name__ == '__main__':
    main()
