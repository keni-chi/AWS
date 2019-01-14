import urllib.request
import time
import json


# 計測準備
url = 'https://xxxxxx.execute-api.ap-northeast-1.amazonaws.com/xxxxxx'

# 計測開始---------------------------
startPd = time.time()

# リクエスト処理
req = urllib.request.Request(url)



# 結果確認
with urllib.request.urlopen(req) as res:
    body_b = res.read()

# 計測結果---------------------------
elapsedTime = time.time() - startPd
print ("elapsedTime:{0}".format(elapsedTime) + "[sec]")


body = json.loads(body_b.decode('utf-8'))
#print (body)
