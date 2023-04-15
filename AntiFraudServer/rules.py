from flask_db import db
from datetime import datetime

class rule(db.Model):
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    code = db.Column(db.Text,  nullable=False)
    last_update = db.Column(db.String(64), nullable=False, default=datetime.now())
    
    def __init__(self, name: str, description: str, code: str, last_update: datetime):
        self.name = name
        self.description = description
        self.code = code
        self.last_update = last_update

    def __repr__(self):
        return f"<RuleResult {self.id}>"