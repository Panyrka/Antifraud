import requests
import json
from datetime import date

url = "http://localhost:2000/transactions"
headers = {"Content-Type": "application/json"}

data = {
    "transactionId": 5,
    "channel": "Web",
    "transactionType": "FL",
    "clientId": 1234,
    "cardKey": "2200567812345678",
    "phone": "+73332221100",
    "clientName": "Igor YEYEE",
    "payeeAccNumber": '666888',
    "payeeName": "chel kakoito",
    "payeePhone": "888666",
    "normalizedAmount": 500,
    "amount": None,
    "currency": "",
    "normalizedDatetime": "2019-12-11 10:58:37",
    "datetime": None,
    "timezone": "no",
    "clientIp": "105.10.10.2",
    "clientLocation": "Ancap",
    "deviceId": "666777"
}

json_data = json.dumps(data)

responsed = requests.post(url, headers=headers, data=json_data)

print(responsed)
print(responsed.text)
