from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), unique=False, nullable=True)
    lastName = db.Column(db.String(200), unique=False, nullable=True)
    password = db.Column(db.String(200), unique=False,nullable=True)

    def __repr__(self):
        return '<User  %r>' % self.id

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountName = db.Column(db.String(200), unique=False, nullable=True)
    bankName = db.Column(db.String(200), unique=False, nullable=True)
    def __repr__(self):
        return '<Bank Account  %r>' % self.id

class Transaction(db.Model):
    transId = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    amount = db.Column(db.Float)

class TransactionGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), unique= False)

class Card(db.Model):
    number = db.Column(db.String(200), primary_key=True)
    type = db.Column(db.String(200), unique= False)
    expiryDate = db.Column(db.Date, unique= False)

