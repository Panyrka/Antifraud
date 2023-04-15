from flask_db import db

class dummy_list():
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    valid = db.Column(db.Boolean, nullable=False)
    valid_from = db.Column(db.Date)
    valid_until = db.Column(db.Date)

    def __repr__(self):
        return f"<dummy_list {self.id}>"
