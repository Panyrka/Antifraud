import requests
import json
from datetime import datetime
from random import randint

url = "http://localhost:2000/transactions"
headers = {"Content-Type": "application/json"}

channel = randint(0,2)
if channel == 0:
    channel = 'Web'
elif channel == 1:
    channel = 'App'
else:
    channel = "Ter"

data = {
    "transactionId": str(randint(1,100000)),
    "channel": channel,
    "transactionType": "FL" if randint(0,1) else "UL",
    "clientId": str(1234),
    "cardKey": "2200567812345678",
    "phone": "+73332221100",
    "clientName": "Igor YEYEE",
    "payeeAccNumber": '666888',
    "payeeName": "chel kakoito",
    "payeePhone": "888666",
    "normalizedAmount": 999,
    "amount": None,
    "currency": "",
    "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "datetime": None,
    "timezone": "no",
    "clientIp": "105.10.10.2",
    "clientLocation": "Ancap",
    "deviceId": "666778"
}

json_data = json.dumps(data)

responsed = requests.post(url, headers=headers, data=json_data)

print(responsed)
print(responsed.text)
