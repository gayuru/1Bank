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


class TransactionGroup(db.Model):
  __tablename__='transaction_groups'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200), unique=True)
  # description = db.Column(db.String(200), unique= False, nullable=True)

  transactions = db.relationship('Transaction', backref='transactions', lazy = True)

class Transaction(db.Model):
  __tablename__='transactions'
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  amount = db.Column(db.Float)
  bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_accounts.id'), nullable = False)
  transaction_group_id = db.Column(db.Integer, db.ForeignKey('transaction_groups.id'), nullable = False)


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

# db.drop_all()
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
cards_schema = CardSchema(many = True)

def addSampleData():
  # Transaction groups
  transactionGroups = [
    TransactionGroup(name='Business'),
    TransactionGroup(name='Donations'),
    TransactionGroup(name='Education'),
    TransactionGroup(name='Uncategorised'),
    TransactionGroup(name='Eating Out'),
    TransactionGroup(name='Shopping'),
    TransactionGroup(name='Health'),
    TransactionGroup(name='Groceries'),
    TransactionGroup(name='Entertainment'),
    TransactionGroup(name='Cash'),
    TransactionGroup(name='Utilities'),
    TransactionGroup(name='Transport'),
    TransactionGroup(name='Travel'),
    TransactionGroup(name='Home'),
    TransactionGroup(name='Fees & Interest'),
    TransactionGroup(name='Tax Paid')
  ]

  # Users
  users = [
    User(firstName="John", lastName="Lee", password=123),
    User(firstName="Jessica", lastName="Iskandr", password=123),
    User(firstName="Peter", lastName="Nguyen", password=123),
    User(firstName="Liza", lastName="Tawaf", password=123)
  ]

  # Bank accounts
  bankAccounts = [
    BankAccount(accountName='Japan Trip', bankName='NAB', verificationId='y7NzhTn6', accountType='Savings', user_id = 3),
    BankAccount(accountName='Everyday', bankName='Commonwealth Bank', verificationId='7XPMaRQq', accountType='Checking', user_id = 3),
    BankAccount(accountName='Usual Spending', bankName='Commonwealth Bank', verificationId='tQ9iTHHj', accountType='Checking', user_id = 4),
    BankAccount(accountName='Europe Trip', bankName='ANZ', verificationId='kuPEe9aT', accountType='Savings', user_id = 4)
  ]

  # Transactions
  # transactions = [
  #   Transaction()
  # ]

  # Cards

  all = [(transactionGroups, transaction_group_schema), (users, user_schema), (bankAccounts, bank_account_schema)]

  for model in all:
    for entry in model[0]:
      db.session.add(entry)
      db.session.commit()
      model[1].dump(entry)

addSampleData()
print("db created", flush=True)

@application.route('/')
def index():
  return 'iSwift'

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
  delete = User.query.filter_by(id = accId).delete()

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
