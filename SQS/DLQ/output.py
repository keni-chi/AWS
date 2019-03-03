import json
from datetime import datetime
import time

def lambda_handler(event, context):
    
    print('output--------------------start')
    now = datetime.utcnow()
    now_str = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S.%fZ')
    print('Output-start: ' + now_str)
    x = {"a": 1}
    y = x['b']  #エラー発生

    print('output---------------end')
