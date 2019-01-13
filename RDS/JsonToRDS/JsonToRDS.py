import sys
import logging
import rds_config
import pymysql

import boto3
from boto3.dynamodb.conditions import Key, Attr
import datetime
import json

# rds settings
rds_host = "{xxxx}.{xxxxx}.ap-northeast-1.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name


logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    print('mysqlstart01')
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

'''
dictfetchall()
    return json_dict
'''
def dictfetchall(cu):
  print("dictfetchall")
  dict = {}
  for row in cu.fetchall():
      dict[row["id"]] = {"conId": row["conId"], "mgmId":row["mgmId"]}
      print(row)
  return dict

'''
lambda_handler()
    return json_str
'''
def lambda_handler(event, context):
    print("EVENT:%s" % event)

    conId = event['controllersId']
    print ("conId=%s" % conId)

    mgmId = event["mgmtpointsId"]
    print ("mgmId=%s" % mgmId)

    print('start mysql DML')
    selectConId = "select * from CONTROLLER"
    #selectConId = "select * from CONTROLLER where CONTROLLER_ID=" + conId
    with conn.cursor() as cur:
        cur.execute(selectConId)

    #store DB all data
    resultsraw = cur.fetchall()

    #column name
    listColumns = [rds_config.CONTROLLER_ID, rds_config.CONTROLLER_NAME]
    #Put dictionary data for each record
    listTmp =[]

    for conTaple in resultsraw:  #parsing with each record
        dictTemp = {}
        for column in range(len(conTaple)):  #parsing with each column
            dictTemp.update({listColumns[column]:conTaple[column]})

        listTmp.append(dictTemp)

    res = json.dumps(listTmp)
    print(res)

    return res
