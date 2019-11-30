from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI
import sys

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
application.debug = True

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
  verificationId = db.Column(db.String(200), unique=False, nullable=True)

  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  cards = db.relationship('Card', backref='bank_account', lazy = True)
  transactions = db.relationship('Transaction', backref='bank_account', lazy = True)

  def __repr__(self):
    return '<Bank Account  %r>' % self.id

class Transaction(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  amount = db.Column(db.Float)

  bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable = False)
  transaction_groups = db.relationship('TransactionGroup', backref='transaction', lazy = True)

class TransactionGroup(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(200), unique= False)

  transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable = False)

class Card(db.Model):
  number = db.Column(db.String(200), primary_key=True)
  type = db.Column(db.String(200), unique= False)
  expiryDate = db.Column(db.Date, unique= False)

  bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'), nullable = False)

db.create_all()
print("db created", flush=True)



@application.route('/')
def hello_world():
  return 'iSwift'

@application.route('/users', methods=['POST', 'GET'])
def users():
  if request.method == 'POST':
    firstName = request.body.firstName
    lastName = request.body.lastName
    password = request.body.password

    user = User(firstName=firstName, lastName=lastName, password=password)
    db.session.add(user)
    result = db.session.commit()
    return result
  elif request.method == 'GET':
    users = User.query.all()
    return users

#get all acounts
@application.route('/accounts', methods=['GET'])
def accounts_get():
  if request.method == 'GET':
    tasks= BankAccount.query.all()
    return tasks

#get user
@application.route('/users/:userId', methods=['GET'])
def user_get():
  if request.method == 'GET':
    tasks = User.query.filter_by(request.body.id).first()
    return tasks

#user accounts
@application.route('/users/:userId/accounts', methods=['GET'])
def user_accounts_get():
  if request.method == 'GET':
    tasks= BankAccount.queryfilter_by(request.body.user_id).all
    return tasks

#get account by id
@application.route('/accounts/:accId', methods=['GET'])
def accid_accounts_get():
  if request.method == 'GET':
    tasks= BankAccount.queryfilter_by(request.body.id).all
    return tasks

#get account by id
@application.route('/accounts/:accId/transactions', methods=['GET'])
def transactions_accid_get():
  if request.method == 'GET':
    tasks= Transaction.queryfilter_by(request.body.bank_account_id).all
    return tasks
if __name__ == '__main__':
  application.run()
