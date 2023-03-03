## Описание транзакций

### Сырая транзакция из системы источника:

 - id (int, not null): Уникальный идентификатор для записи транзакции.
 - transactionId (char, not null): Уникальный идентификатор для самой транзакции.
 - channel (char, not null): Канал, по которому была совершена транзакция (например, online, in-person, mobile).
 - transactionType (char, not null): Тип транзакции (например, purchase, refund, transfer).
 - clientId (char, not null): Уникальный идентификатор клиента, совершившего транзакцию.
 - cardKey (char): Уникальный идентификатор платежной карты клиента.
 - phone (char, not null): Номер телефона, связанный со счетом клиента.
 - clientName (char, not null): Имя клиента, совершающего транзакцию.
 - payeeAccNumber (char, not null): Номер счета получателя платежа (т.е. получателя транзакции).
 - payeeName (char, not null): Имя получателя платежа.
 - payeePhone (char, not null): Номер телефона, связанный со счетом получателя платежа.
 - normalizedAmount (double, not null): Сумма транзакции, нормализованная к стандартной валюте.
 - amount (double): Исходная сумма транзакции до нормализации.
 - currency (char): Валюта, в которой была произведена транзакция.
 - normalizedDatetime (datetime, not null): Дата и время транзакции, нормализованные к стандартному часовому поясу.
 - datetime (datetime): Исходные дата и время транзакции, до нормализации.
 - timezone (char): Часовой пояс, в котором была произведена транзакция.

### Данные enrichment:

 - clientIp (char, not null): IP-адрес устройства, используемого клиентом для совершения транзакции.
 - clientLocation (char, not null): Местоположение устройства, используемого клиентом для совершения транзакции.
 - deviceId (char, not null): Уникальный идентификатор устройства, используемого клиентом для совершения транзакции.

### Примеры:

Без enrichment:
```
json: {
  "id": 123,
  "transactionId": "ABC123",
  "channel": "online",
  "transactionType": "purchase",
  "clientId": "129389",
  "cardKey": null,
  "phone": "+1234567890",
  "clientName": "John Doe",
  "payeeAccNumber": "28478548",
  "payeeName": "Jane Smith",
  "payeePhone": "+0987654321",
  "normalizedAmount": 7530.10,
  "amount": 100.00,
  "currency": "USD",
  "normalizedDatetime": "2023-03-03T09:30:00Z",
  "datetime": "2023-03-03T11:30:00+02:00",
  "timezone": "GMT+3"
}
```

С enrichment:
```
{
  "id": 123,
  "transactionId": "ABC123",
  "channel": "online",
  "transactionType": "purchase",
  "clientId": "129389",
  "cardKey": null,
  "phone": "+1234567890",
  "clientName": "John Doe",
  "payeeAccNumber": "28478548",
  "payeeName": "Jane Smith",
  "payeePhone": "+0987654321",
  "normalizedAmount": 7530.10,
  "amount": 100.00,
  "currency": "USD",
  "normalizedDatetime": "2023-03-03T09:30:00Z",
  "datetime": "2023-03-03T11:30:00+02:00",
  "timezone": "GMT+3",
  "clientIp": "192.168.0.1",
  "clientLocation": "Moscow, Russia",
  "deviceId": "D123"
}
```

## Описание дополнительной информации

### Типы каналов

 - online
 - in-person
 - mobile

### Типы транзакций

- purchase
- refund
- transfer


Но вообще надо будет переписать всю тематику под русские реалии. 
