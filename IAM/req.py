import requests
import json
from aws_requests_auth.aws_auth import AWSRequestsAuth


# STSToken
response = {"Credentials": {"AccessKeyId": "XXXXXXXX"}}
credentials = response['Credentials']

# request info
aws_host = 'XXXXXXXX.execute-api.ap-northeast-1.amazonaws.com'
url = 'https://' + aws_host + '/prod/functionA-1'
body_dict = {"k": "v"}

# execute
auth = AWSRequestsAuth(aws_access_key=credentials['AccessKeyId'],
                       aws_secret_access_key=credentials['SecretAccessKey'],
                       aws_host=aws_host,
                       aws_region='ap-northeast-1',
                       aws_service='execute-api')
headers = {'x-amz-security-token':credentials['SessionToken']}
body = json.dumps(body_dict)
# res = requests.get(url, auth=auth, headers=headers)
res = requests.post(url, data=body, auth=auth, headers=headers)


print("code: " + str(res.status_code)
print("content: " + res.text)
