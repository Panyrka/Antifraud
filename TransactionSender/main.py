import requests
import json
from datetime import datetime
from random import randint, choice
import names

url = "http://127.0.0.1:2000/transactions"
headers = {"Content-Type": "application/json"}

channels = ['Web', 'App', 'Ter']
cities = ['Saint Petersburg', 'Moscow', 'Novosibirsk', 'Omsk', 'Kazan', 'Tver', 'Vladivastok']

def get_amount():
    if randint(1, 10) > 8:
        return randint(50_000, 2_000_000)
    return randint(100, 50_000)

def ger_random_card():
    return "550043215566"+str(randint(1111,8888))

def get_random_phone():
    return "+7911555"+str(randint(1111,9999))

def get_random_id():
    return str(randint(100000,200000));

def get_random_person():
    return [names.get_full_name(), get_random_phone(), ger_random_card(), get_random_id()]

NUMBER_OF_CLIENTS = int(input('Введите количество клиентов: '))
COUNT = int(input('Введите количество транзакций: '))
answers = {'DECLINE': 0, 'ALLOW': 0}
persons = []

for i in range(NUMBER_OF_CLIENTS):
    persons.append(get_random_person())

for i in range(COUNT):
    client = choice(persons)
    payee = choice(persons)
    while payee == client:
        payee = choice(persons)
    data = {
        "transactionId": str(randint(10_000_000, 20_000_000)),
        "channel": choice(channels),
        "transactionType": "FL" if randint(0,1) else "UL",
        "clientId": client[3],
        "cardKey": client[2],
        "phone": client[1],
        "clientName": client[0],
        "payeeAccNumber": payee[2],
        "payeeName": payee[0],
        "payeePhone": payee[1],
        "normalizedAmount": str(get_amount()),
        "amount": None,
        "currency": "",
        "normalizedDatetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "datetime": None,
        "timezone": "no",
        "clientIp": "90.12."+str(randint(1,254))+"."+str(randint(1,254)),
        "clientLocation": choice(cities),
        "deviceId": "AB-836-"+str(randint(50000,70000))
    }

    responsed = requests.post(url, headers=headers, data=json.dumps(data))
    # print(responsed)
    print('Результат транзакции #' + str(i) + ": " + responsed.text)
    
    answers[responsed.text] += 1

print(answers)

exit(1)
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
