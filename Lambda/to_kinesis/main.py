import logging
import boto3
import json
import gzip

def lambda_handler(event, context):

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        logger.info(event)
        data ={"k":"v"}

        pk='pk001'
        data_str = json.dumps(data)
        data_str_b = data_str.encode('utf-8')
        data_zip = gzip.compress(data_str_b)

        response = boto3.client('kinesis').put_record(
            StreamName = "streamname",
            Data = data_zip,
            PartitionKey = "pk001",
        )
        logger.info(response)
        return response

    except Exception as e:
        logger.error(e)
        raise e
