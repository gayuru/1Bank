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

print("db created", flush=True)


@application.route('/')
def hello_world():
  return 'iSwift'

@application.route('/users', methods=['POST', 'GET'])
def users():
  if request.method == 'POST':
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    password = request.form['password']

    user = User(firstName=firstName, lastName=lastName, password=password)
    user_schema = UserSchema()
    db.session.add(user)
    db.session.commit()
    user_schema.dump(user)
    return make_response('User created')
  elif request.method == 'GET':
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.jsonify(users)

#get all acounts
@application.route('/accounts', methods=['GET'])
def accounts_get():
  if request.method == 'GET':
    tasks= BankAccount.query.all()
    result = bank_account_schema.load(tasks)
    return jsonify({'data': result})
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

#get all transactions by a specific account
@application.route('/accounts/:accId/transactions', methods=['GET'])
def transactions_accid_get():
  if request.method == 'GET':
    tasks= Transaction.queryfilter_by(request.body.bank_account_id).all
    return tasks

# #get all transactions by a specific account
# @application.route('/accounts/:accId/transactions&filter=debit', methods=['GET'])
# def transactions_accid_get():
#   if request.method == 'GET':
#     tasks= Transaction.queryfilter_by(request.body.bank_account_id).all
#     return tasks

if __name__ == '__main__':
  application.run()
