import boto3
import os
import os.path
import tarfile
import shutil
import json

def lambda_handler(event, context):

    bucket_name = '20171002-test-labmbdatos3'
    key = 'sess-info2.txt'

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name,key)

    obj.put(Body = bytearray(json.dumps(event)))
