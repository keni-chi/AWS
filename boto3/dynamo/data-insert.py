import logging
import boto3

table_name = '{table_name}'
pk = '{pk}'
dummy_k = 'dummy_k'

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
DYNAMO = boto3.resource('dynamodb')

def lambda_handler(event, context):
    '''
    DynamoDB put item
    '''

    print('start')
    try:
        table = DYNAMO.Table(table_name)
        with table.batch_writer() as batch:
            for i in range(10000):
                batch.put_item(
                    Item={
                        pk: 'pk' + str(i),
                        dummy_k: 'dummy' + str(i),
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
        LOGGER.info('Completed registration')
        return 'end'
    except Exception as error:
        LOGGER.error(error)
        raise error
