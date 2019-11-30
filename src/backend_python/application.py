from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
import sys

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(application)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstName = db.Column(db.String(200), unique=False, nullable=True)
  lastName = db.Column(db.String(200), unique=False, nullable=True)
  password = db.Column(db.String(200), unique=False,nullable=True)
  bankAccounts = db.relationship("BankAccount", backref='user')

  def __repr__(self):
    return '<User  %r>' % self.id

class BankAccount(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  accountName = db.Column(db.String(200), unique=False, nullable=True)
  bankName = db.Column(db.String(200), unique=False, nullable=True)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  cards = db.relationship('Card', backref='bankAccount', lazy = True)
  transactions = db.relationship('Transaction', backref='bankAccount', lazy = True)

  def __repr__(self):
    return '<Bank Account  %r>' % self.id

class Transaction(db.Model):
  transId = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  amount = db.Column(db.Float)

  bankaccount_id = db.Column(db.Integer, db.ForeignKey('bankAccount.id'), nullable = False)
  transactionGroup = db.relationship('TransactionGroup', backref='transaction', lazy = True)

class TransactionGroup(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(200), unique= False)

  transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable = False)

class Card(db.Model):
  number = db.Column(db.String(200), primary_key=True)
  type = db.Column(db.String(200), unique= False)
  expiryDate = db.Column(db.Date, unique= False)

  bankaccount_id = db.Column(db.Integer, db.ForeignKey('bankAccount.id'), nullable = False)

# db.create_all()
print("db created", flush=True)

@application.route('/')
def hello_world():
  return 'iSwift'

@application.route('/users', methods=['POST'])
def users():
  if request.method == 'POST':

    user = User(firstName='Nicholas', lastName='Chong')
    db.session.add(user)
    db.session.commit()
    print(user, flush=True)
    return 'done!'

#liza
@application.route('/accounts', methods=['GET'])
def users():
  if request.method == 'GET':
    tasks= BankAccount.query.all()
    return tasks

#liza
@application.route('/users/:userId', methods=['GET'])
def users():
  if request.method == 'GET':
    tasks= User.query.
    return tasks


if __name__ == '__main__':
  application.run()
