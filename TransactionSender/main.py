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
    "clientId": str(1),
    "cardKey": "1",
    "phone": "+1",
    "clientName": "a Filippov",
    "payeeAccNumber": '1',
    "payeeName": "фa Konovalova",
    "payeePhone": "1",
    "normalizedAmount": 123400,
    "amount": None,
    "currency": "",
    "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "datetime": None,
    "timezone": "no",
    "clientIp": "125.20.10.22",
    "clientLocation": "Saint Petersburg",
    "deviceId": "1"
}

#json_data = json.dumps(data)

#responsed = requests.post(url, headers=headers, data=json_data)

#print(responsed)
#print(responsed.text)



data1 = [{
    "transactionId": str(randint(1,100000)),
    "channel": channel,
    "transactionType": "FL" if randint(0,1) else "UL",
    "clientId": str(6633388821),
    "cardKey": "6600234567891200",
    "phone": "+73332221100",
    "clientName": "Ivan Petrov",
    "payeeAccNumber": '66688844455556666',
    "payeeName": "Olga Sokolova",
    "payeePhone": "73332881100",
    "normalizedAmount": 100000,
    "amount": None,
    "currency": "",
    "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "datetime": None,
    "timezone": "no",
    "clientIp": "105.10.10.20",
    "clientLocation": "MOSCOW",
    "deviceId": "666778"
},{
    "transactionId": str(randint(1,100000)),
    "channel": channel,
    "transactionType": "FL" if randint(0,1) else "UL",
    "clientId": str(6633388812),
    "cardKey": "2233445566009988",
    "phone": "+73332881100",
    "clientName": "Olga Sokolova",
    "payeeAccNumber": '66688844455886666',
    "payeeName": "Dmitry Ivanov",
    "payeePhone": "73388881100",
    "normalizedAmount": 500,
    "amount": None,
    "currency": "",
    "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "datetime": None,
    "timezone": "no",
    "clientIp": "105.10.10.22",
    "clientLocation": "LOBNYA",
    "deviceId": "35345435"
},{
    "transactionId": str(randint(1,100000)),
    "channel": channel,
    "transactionType": "FL" if randint(0,1) else "UL",
    "clientId": str(6633388832),
    "cardKey": "2200343466633300",
    "phone": "+799132881100",
    "clientName": "Maria Smirnova",
    "payeeAccNumber": '77788844455886666',
    "payeeName": "Olga Sokolova",
    "payeePhone": "79928881100",
    "normalizedAmount": 100000,
    "amount": None,
    "currency": "",
    "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "datetime": None,
    "timezone": "no",
    "clientIp": "105.20.10.22",
    "clientLocation": "Saint Petersburg",
    "deviceId": "435435435"
},{
    "transactionId": str(randint(1,100000)),
    "channel": channel,
    "transactionType": "UL" if randint(0,1) else "FL",
    "clientId": str(6633388826),
    "cardKey": "3322664455998877",
    "phone": "+799132885533",
    "clientName": "Maxim Filippov",
    "payeeAccNumber": '77788844455886666',
    "payeeName": "Ekaterina Konovalova",
    "payeePhone": "79928881100",
    "normalizedAmount": 123400,
    "amount": None,
    "currency": "",
    "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "datetime": None,
    "timezone": "no",
    "clientIp": "125.20.10.22",
    "clientLocation": "Saint Petersburg",
    "deviceId": "435435435"
},{
    "transactionId": str(randint(1,100000)),
    "channel": channel,
    "transactionType": "UL" if randint(0,1) else "FL",
    "clientId": str(6633388820),
    "cardKey": "2200343465633377",
    "phone": "+799132885533",
    "clientName": "Alexey Popov",
    "payeeAccNumber": '77788844455886666',
    "payeeName": "Ekaterina Konovalova",
    "payeePhone": "79928881100",
    "normalizedAmount": 12400,
    "amount": None,
    "currency": "",
    "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "datetime": None,
    "timezone": "no",
    "clientIp": "125.25.10.22",
    "clientLocation": "Saint Petersburg",
    "deviceId": "3457657445"
},{
    "transactionId": str(randint(1,100000)),
    "channel": channel,
    "transactionType": "UL" if randint(0,1) else "FL",
    "clientId": str(6633388820),
    "cardKey": "2200343465633377",
    "phone": "+799132885533",
    "clientName": "Anna Volkova",
    "payeeAccNumber": '77788844455886666',
    "payeeName": "Sergey Kuznetsov",
    "payeePhone": "79928881100",
    "normalizedAmount": 300,
    "amount": None,
    "currency": "",
    "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "datetime": None,
    "timezone": "no",
    "clientIp": "125.25.10.22",
    "clientLocation": "Saint Petersburg",
    "deviceId": "3457657445"
}]

for d in data1:
    
    json_data = json.dumps(d)

    responsed = requests.post(url, headers=headers, data=json_data)

    print(responsed)
    print(responsed.text)
