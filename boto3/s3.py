import boto3
import json

S3_BUCKET_TESTTEST = 'xxxxxxxxxxxxxxxxx'
S3_KEY = 'test4/data.json'
S3_KEY_CSV = 'test4/data.csv'

data = {"k": "v"}


def s3_put_obj(data):
    resource = boto3.resource('s3')
    obj = resource.Object(S3_BUCKET_TESTTEST, S3_KEY)
    res = obj.put(Body = bytes(json.dumps(data), 'utf-8'))
    print(res)


def s3_get_obj():
    resource = boto3.resource('s3')
    obj = resource.Object(S3_BUCKET_TESTTEST, S3_KEY)
    res_raw = obj.get()
    res = res_raw['Body'].read()
    res_str = str(res, 'utf-8')
    print(res_str)


def s3_delete_obj():
    resource = boto3.resource('s3')
    obj = resource.Object(S3_BUCKET_TESTTEST, S3_KEY)
    res = obj.delete()
    print(res)


def s3_select():
    s3 = boto3.client('s3', 'ap-northeast-1')

    response_s3select = s3.select_object_content(
        Bucket = S3_BUCKET_TESTTEST,
        Key = S3_KEY_CSV,
        ExpressionType = 'SQL',
        Expression = 'Select s.id, s.name, s.price from S3Object s',
        # Expression = 'Select count(*) from S3Object s',
        # Expression = 'Select s.id, s.name, s.price from S3Object s where cast(s.id as int) > 3',
        # Expression = 'Select sum(cast(s.price as int)) from S3Object s',
        # Expression = 'Select max(cast(s.price as int)), avg(cast(s.price as int)), min(cast(s.price as int)) from S3Object s',
        # Expression = '',
        InputSerialization = {
            'CompressionType': 'NONE',
            'CSV': {
                'FileHeaderInfo' : 'Use',
                'RecordDelimiter': '\n',
                'FieldDelimiter': ','
            }
        },
        OutputSerialization= {
            'CSV': {
                'RecordDelimiter': '\n',
                'FieldDelimiter': ','
            }
        }
    )
    for event in response_s3select['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            print('s3 selecting----')
            print(records)


def main():
    """main."""
    
    # s3_put_obj
    print('s3_put_obj--------------------start')
    s3_put_obj(data)
    print('s3_put_obj--------------------end')

    # s3_get_obj
    print('s3_get_obj--------------------start')
    s3_get_obj()
    print('s3_get_obj--------------------end')

    # s3_delete_obj
    print('s3_delete_obj--------------------start')
    s3_delete_obj()
    print('s3_delete_obj--------------------end')

    # s3_select
    print('s3_select--------------------start')
    s3_select()
    print('s3_select--------------------end')


if __name__ == '__main__':
    main()
