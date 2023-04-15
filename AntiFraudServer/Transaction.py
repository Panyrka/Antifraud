import json
from typing import Optional
from flask_db import db
import datetime as dt


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transactionId = db.Column(db.String(64))
    channel = db.Column(db.String(64))
    transactionType = db.Column(db.String(16))
    clientId = db.Column(db.String(64))
    cardKey = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    clientName = db.Column(db.String(100))
    payeeAccNumber = db.Column(db.String(20))
    payeeName = db.Column(db.String(100))
    payeePhone = db.Column(db.String(20))
    normalizedAmount = db.Column(db.Numeric)
    amount = db.Column(db.Numeric)
    currency = db.Column(db.String(3))
    normalizedDatetime = db.Column(db.DateTime)
    datetime = db.Column(db.DateTime)
    timezone = db.Column(db.String(20))
    clientIp = db.Column(db.String(15))
    clientLocation = db.Column(db.String(100))
    deviceId = db.Column(db.String(20))

    def __init__(
        self,
        transactionId: str,
        channel: str,
        transactionType: str,
        clientId: str,
        cardKey: str,
        phone: str,
        clientName: str,
        payeeAccNumber: str,
        payeeName: str,
        payeePhone: str,
        normalizedAmount: float,
        amount: Optional[float],
        currency: str,
        normalizedDatetime: dt.datetime,
        datetime: Optional[dt.datetime],
        timezone: str,
        clientIp: str,
        clientLocation: str,
        deviceId: str
    ) -> None:
        self.transactionId = transactionId
        self.channel = channel
        self.transactionType = transactionType
        self.clientId = clientId
        self.cardKey = cardKey
        self.phone = phone
        self.clientName = clientName
        self.payeeAccNumber = payeeAccNumber
        self.payeeName = payeeName
        self.payeePhone = payeePhone
        self.normalizedAmount = normalizedAmount
        self.amount = amount
        self.currency = currency
        self.normalizedDatetime = normalizedDatetime
        self.datetime = datetime
        self.timezone = timezone
        self.clientIp = clientIp
        self.clientLocation = clientLocation
        self.deviceId = deviceId

    @classmethod
    def from_json(cls, json_str: str) -> 'Transaction':
        json_dict = json.loads(json_str)
        return cls(**json_dict)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        return cls(
            transactionId=data['transactionId'],
            channel=data['channel'],
            transactionType=data['transactionType'],
            clientId=data['clientId'],
            cardKey=data['cardKey'],
            phone=data['phone'],
            clientName=data['clientName'],
            payeeAccNumber=data['payeeAccNumber'],
            payeeName=data['payeeName'],
            payeePhone=data['payeePhone'],
            normalizedAmount=data['normalizedAmount'],
            amount=data.get('amount'),
            currency=data['currency'],
            normalizedDatetime=data['normalizedDatetime'],
            datetime=data.get('datetime'),
            timezone=data['timezone'],
            clientIp=data['clientIp'],
            clientLocation=data['clientLocation'],
            deviceId=data['deviceId']
        )

    def __repr__(self):
        return f'Transaction({self.transaction_id}, {self.channel}, {self.transaction_type}, {self.client_id}, {self.card_key}, {self.phone}, {self.client_name}, {self.payee_acc_number}, {self.payee_name}, {self.payee_phone}, {self.normalized_amount}, {self.amount}, {self.currency}, {self.normalized_datetime}, {self.datetime}, {self.timezone}, {self.client_ip}, {self.client_location}, {self.device_id})'