import json
from datetime import datetime
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):

    #PkSk
    resData = get_PkSk('pk','sk')

    #GSI
    resData = get_GSI('pk')

    #Pk_filter
    resData = get_Pk_filter('pk')

    return resData


#構成チェックNGリスト検索_PkSk
def get_PkSk(partition_key,sort_key):
  resource = boto3.resource('dynamodb')
  table = resource.Table('テーブル名')

  queryData = table.query(
	  KeyConditionExpression = Key('pk').eq(partition_key)& Key('sk').eq(sort_key)
  )

  item = queryData['Items']
  return item

# GSI
def get_GSI(partition_key):
  resource = boto3.resource('dynamodb')
  table = resource.Table('テーブル名')

  queryData = table.query(
    IndexName = 'GSI名',
    #FilterExpression=Attr('connectState').eq(True),
	  KeyConditionExpression = Key('pk').eq(partition_key)
  )

  item = queryData['Items']
  return item

# filter
def get_Pk_filter(partition_key):
  resource = boto3.resource('dynamodb')
  table = resource.Table('テーブル名')

  queryData = table.query(
      FilterExpression = Attr('属性1').eq('値') | Attr('属性2').eq('値') ,
	  KeyConditionExpression = Key('edgeId').eq(partition_key)
  )

  item = queryData['Items']
  return item
