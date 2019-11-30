from flask import Flask, request, jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import SQLALCHEMY_DATABASE_URI
import sys

application = Flask(__name__)

application.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
application.debug = True

db = SQLAlchemy(application)
ma = Marshmallow(application)

class User(db.Model):
  __tablename__='users'
  id = db.Column(db.Integer, primary_key=True)
  firstName = db.Column(db.String(200), unique=False, nullable=True)
  lastName = db.Column(db.String(200), unique=False, nullable=True)
  password = db.Column(db.String(200), unique=False,nullable=True)

  bankAccounts = db.relationship("BankAccount", backref='users')

  def __init__(self, firstName, lastName, password):
    self.firstName = firstName
    self.lastName = lastName
    self.password = password

class BankAccount(db.Model):
  __tablename__='bank_accounts'
  id = db.Column(db.Integer, primary_key=True)
  accountName = db.Column(db.String(200), unique=False, nullable=True)
  bankName = db.Column(db.String(200), unique=False, nullable=True)
  verificationId = db.Column(db.String(200), unique=False, nullable=True)
  accountType = db.Column(db.String(200), unique=False, nullable=True)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  cards = db.relationship('Card', backref='bank_accounts', lazy = True)
  transactions = db.relationship('Transaction', backref='bank_accounts', lazy = True)


class Transaction(db.Model):
  __tablename__='transactions'
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  amount = db.Column(db.Float)

  bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable = False)
  transaction_groups = db.relationship('TransactionGroup', backref='transactions', lazy = True)

class TransactionGroup(db.Model):
  __tablename__='transaction_groups'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(200), unique= False)

  transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable = False)


class Card(db.Model):
  __tablename__='cards'
  number = db.Column(db.String(200), primary_key=True)
  type = db.Column(db.String(200), unique= False)
  expiryDate = db.Column(db.Date, unique= False)

  bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable = False)

class UserSchema(ma.ModelSchema):
  class Meta:
    model = User

class BankAccountSchema(ma.ModelSchema):
  class Meta:
    model = BankAccount

class TransactionSchema(ma.ModelSchema):
  class Meta:
    model = Transaction

class TransactionGroupSchema(ma.ModelSchema):
  class Meta:
    model = TransactionGroup

class CardSchema(ma.ModelSchema):
  class Meta:
    model = Card

db.drop_all()
db.create_all()

user_schema = UserSchema()
users_schema = UserSchema(many = True)

bank_account_schema = BankAccountSchema()
bank_accounts_schema = BankAccountSchema(many = True)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many = True)

transaction_group_schema = TransactionGroupSchema()
transaction_groups_schema = TransactionGroupSchema(many = True)

card_schema = CardSchema()
@application.route('/')
def hello_world():
  return 'iSwift'

print("db created", flush=True)

@application.route('/users', methods=['POST', 'GET'])
def users():
  if request.method == 'POST':
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    password = request.form['password']

    user = User(firstName=firstName, lastName=lastName, password=password)
    db.session.add(user)
    db.session.commit()
    user_schema.dump(user)
    return make_response('User created')
  elif request.method == 'GET':
    users = User.query.all()
    return users_schema.jsonify(users)

cards_schema = CardSchema(many = True)

#get user
@application.route('/users/<userId>', methods=['GET'])
def user_get(userId):
  if request.method == 'GET':
    user = User.query.filter_by(id = userId).first()
    return user_schema.jsonify(user)

#user accounts
@application.route('/users/<userId>/accounts', methods=['GET'])
def user_accounts_get(userId):
  if request.method == 'GET':
    accounts = BankAccount.query.filter_by(user_id = userId).all()
    return bank_accounts_schema.jsonify(accounts)

#get all accounts
@application.route('/accounts', methods=['GET', 'POST'])
def accounts_get():
  if request.method == 'POST':
    accountName = request.form['accountName']
    bankName = request.form['bankName']
    verificationId = request.form['verificationId']
    accountType = request.form['accountType']

    account = BankAccount(accountName=accountName, bankName=bankName, verificationId=verificationId, accountType=accountType)
    db.session.add(account)
    db.session.commit()
    bank_account_schema.dump(account)
    return make_response('Account created')
  elif request.method == 'GET':
    accounts = BankAccount.query.all()
    return bank_accounts_schema.jsonify(accounts)

@application.route('/accounts/<accId>', methods=['DELETE'])
def account_close(accId):
  pass

#get account by id
@application.route('/accounts/<accId>', methods=['GET'])
def accid_accounts_get(accId):
  if request.method == 'GET':
    account = BankAccount.query.filter_by(id = accId).first()
    return bank_account_schema.jsonify(account)

#get all transactions by a specific account
@application.route('/accounts/<accId>/transactions', methods=['GET'])
def transactions_accid_get(accId):
  transactions = Transaction.query.filter_by(accId).all()
  return transactions_schema.jsonify(transactions)

@application.route('/transactions', methods=['POST', 'GET'])
def transactions():
  if request.method == 'POST':
    date = request.form['date']
    amount = request.form['amount']

    transaction = Transaction(date=date, amount=amount)
    db.session.add(transaction)
    db.session.commit()
    transaction_schema.dump(transaction)
    return make_response('Transaction created')
  elif request.method == 'GET':
    transactions = Transaction.query.all()
    return transactions_schema.jsonify(transactions)

#get transaction
@application.route('/transactions/<transId>', methods=['GET'])
def transaction_get(transId):
  transaction = Transaction.query.filter_by(id = transId).first()
  return transaction_schema.jsonify(transaction)



if __name__ == '__main__':
  application.run()
