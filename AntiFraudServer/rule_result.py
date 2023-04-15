from flask_db import db
from datetime import datetime

class rule_result(db.Model):
    __tablename__ = 'rule_result'

    id = db.Column(db.Integer, primary_key=True)
    transactionId = db.Column(db.String(64), nullable=False)
    normalizedDatetime = db.Column(db.DateTime,  nullable=False)
    rule_name = db.Column(db.String(64), nullable=False)
    rule_result = db.Column(db.Boolean, nullable=False)
    
    def __init__(self, transactionId: str, normalizedDatetime: datetime, rule_name: str, rule_result: bool):
        self.transactionId = transactionId
        self.normalizedDatetime = normalizedDatetime
        self.rule_name = rule_name
        self.rule_result = rule_result

    def __repr__(self):
        return f"<RuleResult {self.id}>"