import datetime as dt
import json

from flask_db import db
from typing import Optional
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base

import enum
from sqlalchemy import Enum

class profiles(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    time_unit = db.Column(db.String(1), nullable=False, default='d')
    time_unit_iterval = db.Column(db.Integer, nullable=False, default=0)
    code = db.Column(db.Text,  nullable=False)
    last_update = db.Column(db.String(64), nullable=False, default=dt.datetime.now())
    
    def __init__(self, name: str, description: str, time_unit: str, time_unit_interval: int, code: str, last_update: dt.datetime):
        self.name = name
        self.description = description
        self.time_unit = time_unit
        self.time_unit_iterval = time_unit_interval
        self.code = code
        self.last_update = last_update

    def __repr__(self):
        return f"<RuleResult {self.id}>"

class RULE_RESULT_STATUS(enum.Enum):
    ALLOW = 1
    DECLINE = 2

class active_rule(db.Model):
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    code = db.Column(db.Text,  nullable=False)
    rule_result_status = Column("Rule result status", Enum(RULE_RESULT_STATUS), nullable=False)
    last_update = db.Column(db.String(64), nullable=False, default=dt.datetime.now())
    
    def __init__(self, name: str, description: str, code: str, last_update: dt.datetime, rule_result_status: RULE_RESULT_STATUS):
        self.name = name
        self.description = description
        self.code = code
        self.last_update = last_update
        self.rule_result_status = rule_result_status

    def __repr__(self):
        return f"<RuleResult {self.id}>"

class rule_result(db.Model):
    __tablename__ = 'rule_result'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(64), nullable=False)
    normalized_datetime = db.Column(db.DateTime,  nullable=False)
    rule_name = db.Column(db.String(64), nullable=False)
    rule_result = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, transactionId: str, normalized_datetime: dt.datetime, rule_name: str, rule_result: bool):
        self.transaction_id = transactionId
        self.normalized_datetime = normalized_datetime
        self.rule_name = rule_name
        self.rule_result = rule_result

    def __repr__(self):
        return f"<RuleResult {self.id}>"

Base = declarative_base()
 
class STATUS_CHOICES_ENUM(enum.Enum):
    FRAUD = 1
    NEW = 2
    LEGITIMATE = 3

class alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(64), nullable=False)
    client_id = db.Column(db.String(64), nullable=False)
    normalized_datetime = db.Column(db.DateTime,  nullable=False)
    triggered_rules = db.Column(db.String(1024), nullable=False)
    status = Column('Alert status', Enum(STATUS_CHOICES_ENUM), nullable=False)
    
    def __init__(self, transactionId: str, client_id: str, normalized_datetime: dt.datetime, triggered_rules: str, status: STATUS_CHOICES_ENUM):
        self.transaction_id = transactionId
        self.client_id = client_id
        self.normalized_datetime = normalized_datetime
        self.triggered_rules = triggered_rules
        self.status = status

    def __repr__(self):
        return f"<RuleResult {self.id}>"

class PlatformList(db.Model):
    __tablename__ = 'platform_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    
    def __repr__(self) -> str:
        attrs = []
        for attr, value in self.__dict__.items():
            attrs.append(f"{attr}={value}")
        return f"<Transaction {' '.join(attrs)}>"

class dummy_list():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    valid = db.Column(db.Boolean, nullable=False)
    valid_from = db.Column(db.Date)
    valid_until = db.Column(db.Date)

    def __repr__(self):
        return f"<dummy_list {self.id}>"

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