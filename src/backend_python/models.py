from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), unique=False, nullable=True)
    lastName = db.Column(db.String(200), unique=False, nullable=True)