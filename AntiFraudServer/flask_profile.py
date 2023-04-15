from flask_db import db

class flask_profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(30), nullable=False)
    date_segment = db.Column(db.String(2), nullable=False)
    ds_number = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Profile {self.id}>"