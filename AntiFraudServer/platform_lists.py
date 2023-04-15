from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_db import db

class PlatformList(db.Model):
    __tablename__ = 'platform_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        attrs = []
        for attr, value in self.__dict__.items():
            attrs.append(f"{attr}={value}")
        return f"<Transaction {' '.join(attrs)}>"
