# coding: utf-8

import boto3
import json

def lambda_handler(event, context):

    # 引数
    input_event = {
        "param1": 1,
        "param2": 2,
        "param3": 3
    }
    Payload = json.dumps(input_event) # jsonシリアライズ

    # 呼び出し
    response = boto3.client('lambda').invoke(
        FunctionName='lambda1',
        InvocationType='RequestResponse',
        Payload=Payload
    )

    # レスポンス読出し
    response_payload = json.loads(response["Payload"].read()) # jsonデコード
    print("response_payload")
    print(response_payload)

    return response_payload
