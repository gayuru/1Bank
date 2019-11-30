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
  firstName = db.Column(db.String(200), unique=False, nullable=False)
  lastName = db.Column(db.String(200), unique=False, nullable=False)
  password = db.Column(db.String(200), unique=False,nullable=False)

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
  name = db.Column(db.String(200), unique=False, nullable=False)

  transactions = db.relationship('Transaction', backref='transaction_groups', lazy = True)

class Transaction(db.Model):
  __tablename__='transactions'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200))
  icon = db.Column(db.String(1000))
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

class TransactionGroupSchema(ma.ModelSchema):
  class Meta:
    model = TransactionGroup

class TransactionSchema(ma.ModelSchema):
  class Meta:
    model = Transaction

class CardSchema(ma.ModelSchema):
  class Meta:
    model = Card

db.drop_all()
db.create_all()
db.session.commit()

user_schema = UserSchema()
users_schema = UserSchema(many = True)

bank_account_schema = BankAccountSchema()
bank_accounts_schema = BankAccountSchema(many = True)

transaction_group_schema = TransactionGroupSchema()
transaction_groups_schema = TransactionGroupSchema(many=True)

transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many = True)

card_schema = CardSchema()
cards_schema = CardSchema(many = True)

def addSampleData():
  print("Adding sample data", flush=True)
  # # Transaction groups
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
  transactions = [
    # Peter - 1st account
    Transaction(name='Spotify Ltd.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjuoqChmZLmAhVSyDgGHbPkBZMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.spotify.com%2F&psig=AOvVaw2lA03VuvLHGOSHZdMPn8-s&ust=1575212305580875', date='2019-01-01', amount=-5.00, bank_account_id=1, transaction_group_id=9),
    Transaction(name='McDonalds Bourke St.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjT2KPlm5LmAhU9zzgGHfuoClsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMcDonald%2527s&psig=AOvVaw2_dX5VKst1lR1HxfJj3bZS&ust=1575212983926499', date='2019-01-01', amount= -50.49, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Starbucks Spencer Mall', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwii-NDNnJLmAhUgxzgGHZEXAUIQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.stickpng.com%2Fimg%2Ficons-logos-emojis%2Ficonic-brands%2Fstarbucks-logo&psig=AOvVaw0jY0CPjjovvbm4DpTjx4e7&ust=1575213193222643', date='2019-01-03', amount=-7.5, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Amazon AU Sydney', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjSts6PnZLmAhWjzjgGHecTCUwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F1298723%2Famazon_icon&psig=AOvVaw0jFGclV-prggRr8FYVOBf2&ust=1575213341548464', date='2019-01-11', amount=-150.49, bank_account_id=1, transaction_group_id=6),
    Transaction(name='Withdrawal ATM CBA ATM', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwijzsqunZLmAhW1zDgGHcH3A2UQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.commbank.com.au%2F&psig=AOvVaw1l0OQ-RToTOtPDJDcIVIxu&ust=1575213406160310', date='2019-01-15', amount=-50, bank_account_id=1, transaction_group_id=10),
    Transaction(name='Liza Hot Springs', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjwmu3anZLmAhUtwzgGHQjkBJsQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F887037%2Fcash_cash_flow_dollars_money_icon&psig=AOvVaw1zapOJydiUSLC1jFr5wpGM&ust=1575213490236989', date='2019-01-18', amount=250, bank_account_id=1, transaction_group_id=10),
    Transaction(name='Jetts Fitness Aus Card', icon='http://vlcl.com.au/wp-content/uploads/2017/03/1389_12508888_1070540622976287_9031922848091024375_n.jpg', date='2019-01-20', amount=-27.5, bank_account_id=1, transaction_group_id=7),
    Transaction(name='McDonalds Bourke St.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjT2KPlm5LmAhU9zzgGHfuoClsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMcDonald%2527s&psig=AOvVaw2_dX5VKst1lR1HxfJj3bZS&ust=1575212983926499', date='2019-01-22', amount= -42.4, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Spotify Ltd.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjuoqChmZLmAhVSyDgGHbPkBZMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.spotify.com%2F&psig=AOvVaw2lA03VuvLHGOSHZdMPn8-s&ust=1575212305580875', date='2019-01-22', amount=-5.00, bank_account_id=1, transaction_group_id=9),
    Transaction(name='Amazon AU Sydney', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjSts6PnZLmAhWjzjgGHecTCUwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F1298723%2Famazon_icon&psig=AOvVaw0jFGclV-prggRr8FYVOBf2&ust=1575213341548464', date='2019-01-23', amount=-100.99, bank_account_id=1, transaction_group_id=6),
    Transaction(name='Public Bar Pty Ltd Docklands', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjkrbHRnpLmAhUVzzgGHY8xA1cQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F4018538%2Fcocktail_drinks_icon&psig=AOvVaw1ZWLStD9wIxC6S232LSmlo&ust=1575213747368138', date='2019-01-25', amount=-10, bank_account_id=1, transaction_group_id=9),
    Transaction(name='Withdrawal ATM CBA ATM', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwijzsqunZLmAhW1zDgGHcH3A2UQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.commbank.com.au%2F&psig=AOvVaw1l0OQ-RToTOtPDJDcIVIxu&ust=1575213406160310', date='2019-01-15', amount=-50, bank_account_id=1, transaction_group_id=10),    # Peter - 1st account

    Transaction(name='Spotify Ltd.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjuoqChmZLmAhVSyDgGHbPkBZMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.spotify.com%2F&psig=AOvVaw2lA03VuvLHGOSHZdMPn8-s&ust=1575212305580875', date='2019-01-01', amount=-5.00, bank_account_id=1, transaction_group_id=9),
    Transaction(name='McDonalds Bourke St.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjT2KPlm5LmAhU9zzgGHfuoClsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMcDonald%2527s&psig=AOvVaw2_dX5VKst1lR1HxfJj3bZS&ust=1575212983926499', date='2019-01-01', amount= -50.49, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Starbucks Spencer Mall', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwii-NDNnJLmAhUgxzgGHZEXAUIQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.stickpng.com%2Fimg%2Ficons-logos-emojis%2Ficonic-brands%2Fstarbucks-logo&psig=AOvVaw0jY0CPjjovvbm4DpTjx4e7&ust=1575213193222643', date='2019-01-03', amount=-7.5, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Amazon AU Sydney', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjSts6PnZLmAhWjzjgGHecTCUwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F1298723%2Famazon_icon&psig=AOvVaw0jFGclV-prggRr8FYVOBf2&ust=1575213341548464', date='2019-01-11', amount=-150.49, bank_account_id=1, transaction_group_id=6),
    Transaction(name='Withdrawal ATM CBA ATM', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwijzsqunZLmAhW1zDgGHcH3A2UQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.commbank.com.au%2F&psig=AOvVaw1l0OQ-RToTOtPDJDcIVIxu&ust=1575213406160310', date='2019-01-15', amount=-50, bank_account_id=1, transaction_group_id=10),
    Transaction(name='Liza Hot Springs', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjwmu3anZLmAhUtwzgGHQjkBJsQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F887037%2Fcash_cash_flow_dollars_money_icon&psig=AOvVaw1zapOJydiUSLC1jFr5wpGM&ust=1575213490236989', date='2019-01-18', amount=250, bank_account_id=1, transaction_group_id=10),
    Transaction(name='Jetts Fitness Aus Card', icon='http://vlcl.com.au/wp-content/uploads/2017/03/1389_12508888_1070540622976287_9031922848091024375_n.jpg', date='2019-01-20', amount=-27.5, bank_account_id=1, transaction_group_id=7),
    Transaction(name='McDonalds Bourke St.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjT2KPlm5LmAhU9zzgGHfuoClsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMcDonald%2527s&psig=AOvVaw2_dX5VKst1lR1HxfJj3bZS&ust=1575212983926499', date='2019-01-22', amount= -42.4, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Spotify Ltd.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjuoqChmZLmAhVSyDgGHbPkBZMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.spotify.com%2F&psig=AOvVaw2lA03VuvLHGOSHZdMPn8-s&ust=1575212305580875', date='2019-01-22', amount=-5.00, bank_account_id=1, transaction_group_id=9),
    Transaction(name='Amazon AU Sydney', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjSts6PnZLmAhWjzjgGHecTCUwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F1298723%2Famazon_icon&psig=AOvVaw0jFGclV-prggRr8FYVOBf2&ust=1575213341548464', date='2019-01-23', amount=-100.99, bank_account_id=1, transaction_group_id=6),
    Transaction(name='Public Bar Pty Ltd Docklands', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjkrbHRnpLmAhUVzzgGHY8xA1cQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F4018538%2Fcocktail_drinks_icon&psig=AOvVaw1ZWLStD9wIxC6S232LSmlo&ust=1575213747368138', date='2019-01-25', amount=-10, bank_account_id=1, transaction_group_id=9),
    Transaction(name='Withdrawal ATM CBA ATM', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwijzsqunZLmAhW1zDgGHcH3A2UQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.commbank.com.au%2F&psig=AOvVaw1l0OQ-RToTOtPDJDcIVIxu&ust=1575213406160310', date='2019-01-15', amount=-50, bank_account_id=1, transaction_group_id=10),    # Peter - 1st account

    Transaction(name='Spotify Ltd.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjuoqChmZLmAhVSyDgGHbPkBZMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.spotify.com%2F&psig=AOvVaw2lA03VuvLHGOSHZdMPn8-s&ust=1575212305580875', date='2019-01-01', amount=-5.00, bank_account_id=1, transaction_group_id=9),
    Transaction(name='McDonalds Bourke St.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjT2KPlm5LmAhU9zzgGHfuoClsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMcDonald%2527s&psig=AOvVaw2_dX5VKst1lR1HxfJj3bZS&ust=1575212983926499', date='2019-01-01', amount= -50.49, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Starbucks Spencer Mall', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwii-NDNnJLmAhUgxzgGHZEXAUIQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.stickpng.com%2Fimg%2Ficons-logos-emojis%2Ficonic-brands%2Fstarbucks-logo&psig=AOvVaw0jY0CPjjovvbm4DpTjx4e7&ust=1575213193222643', date='2019-01-03', amount=-7.5, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Amazon AU Sydney', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjSts6PnZLmAhWjzjgGHecTCUwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F1298723%2Famazon_icon&psig=AOvVaw0jFGclV-prggRr8FYVOBf2&ust=1575213341548464', date='2019-01-11', amount=-150.49, bank_account_id=1, transaction_group_id=6),
    Transaction(name='Withdrawal ATM CBA ATM', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwijzsqunZLmAhW1zDgGHcH3A2UQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.commbank.com.au%2F&psig=AOvVaw1l0OQ-RToTOtPDJDcIVIxu&ust=1575213406160310', date='2019-01-15', amount=-50, bank_account_id=1, transaction_group_id=10),
    Transaction(name='Liza Hot Springs', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjwmu3anZLmAhUtwzgGHQjkBJsQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F887037%2Fcash_cash_flow_dollars_money_icon&psig=AOvVaw1zapOJydiUSLC1jFr5wpGM&ust=1575213490236989', date='2019-01-18', amount=250, bank_account_id=1, transaction_group_id=10),
    Transaction(name='Jetts Fitness Aus Card', icon='http://vlcl.com.au/wp-content/uploads/2017/03/1389_12508888_1070540622976287_9031922848091024375_n.jpg', date='2019-01-20', amount=-27.5, bank_account_id=1, transaction_group_id=7),
    Transaction(name='McDonalds Bourke St.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjT2KPlm5LmAhU9zzgGHfuoClsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMcDonald%2527s&psig=AOvVaw2_dX5VKst1lR1HxfJj3bZS&ust=1575212983926499', date='2019-01-22', amount= -42.4, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Spotify Ltd.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjuoqChmZLmAhVSyDgGHbPkBZMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.spotify.com%2F&psig=AOvVaw2lA03VuvLHGOSHZdMPn8-s&ust=1575212305580875', date='2019-01-22', amount=-5.00, bank_account_id=1, transaction_group_id=9),
    Transaction(name='Amazon AU Sydney', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjSts6PnZLmAhWjzjgGHecTCUwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F1298723%2Famazon_icon&psig=AOvVaw0jFGclV-prggRr8FYVOBf2&ust=1575213341548464', date='2019-01-23', amount=-100.99, bank_account_id=1, transaction_group_id=6),
    Transaction(name='Public Bar Pty Ltd Docklands', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjkrbHRnpLmAhUVzzgGHY8xA1cQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F4018538%2Fcocktail_drinks_icon&psig=AOvVaw1ZWLStD9wIxC6S232LSmlo&ust=1575213747368138', date='2019-01-25', amount=-10, bank_account_id=1, transaction_group_id=9),
    Transaction(name='Withdrawal ATM CBA ATM', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwijzsqunZLmAhW1zDgGHcH3A2UQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.commbank.com.au%2F&psig=AOvVaw1l0OQ-RToTOtPDJDcIVIxu&ust=1575213406160310', date='2019-01-15', amount=-50, bank_account_id=1, transaction_group_id=10),    # Peter - 1st account

    Transaction(name='Spotify Ltd.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjuoqChmZLmAhVSyDgGHbPkBZMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.spotify.com%2F&psig=AOvVaw2lA03VuvLHGOSHZdMPn8-s&ust=1575212305580875', date='2019-01-01', amount=-5.00, bank_account_id=1, transaction_group_id=9),
    Transaction(name='McDonalds Bourke St.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjT2KPlm5LmAhU9zzgGHfuoClsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMcDonald%2527s&psig=AOvVaw2_dX5VKst1lR1HxfJj3bZS&ust=1575212983926499', date='2019-01-01', amount= -50.49, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Starbucks Spencer Mall', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwii-NDNnJLmAhUgxzgGHZEXAUIQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.stickpng.com%2Fimg%2Ficons-logos-emojis%2Ficonic-brands%2Fstarbucks-logo&psig=AOvVaw0jY0CPjjovvbm4DpTjx4e7&ust=1575213193222643', date='2019-01-03', amount=-7.5, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Amazon AU Sydney', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjSts6PnZLmAhWjzjgGHecTCUwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F1298723%2Famazon_icon&psig=AOvVaw0jFGclV-prggRr8FYVOBf2&ust=1575213341548464', date='2019-01-11', amount=-150.49, bank_account_id=1, transaction_group_id=6),
    Transaction(name='Withdrawal ATM CBA ATM', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwijzsqunZLmAhW1zDgGHcH3A2UQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.commbank.com.au%2F&psig=AOvVaw1l0OQ-RToTOtPDJDcIVIxu&ust=1575213406160310', date='2019-01-15', amount=-50, bank_account_id=1, transaction_group_id=10),
    Transaction(name='Liza Hot Springs', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjwmu3anZLmAhUtwzgGHQjkBJsQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F887037%2Fcash_cash_flow_dollars_money_icon&psig=AOvVaw1zapOJydiUSLC1jFr5wpGM&ust=1575213490236989', date='2019-01-18', amount=250, bank_account_id=1, transaction_group_id=10),
    Transaction(name='Jetts Fitness Aus Card', icon='http://vlcl.com.au/wp-content/uploads/2017/03/1389_12508888_1070540622976287_9031922848091024375_n.jpg', date='2019-01-20', amount=-27.5, bank_account_id=1, transaction_group_id=7),
    Transaction(name='McDonalds Bourke St.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjT2KPlm5LmAhU9zzgGHfuoClsQjRx6BAgBEAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FMcDonald%2527s&psig=AOvVaw2_dX5VKst1lR1HxfJj3bZS&ust=1575212983926499', date='2019-01-22', amount= -42.4, bank_account_id=1, transaction_group_id=5),
    Transaction(name='Spotify Ltd.', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjuoqChmZLmAhVSyDgGHbPkBZMQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.spotify.com%2F&psig=AOvVaw2lA03VuvLHGOSHZdMPn8-s&ust=1575212305580875', date='2019-01-22', amount=-5.00, bank_account_id=1, transaction_group_id=9),
    Transaction(name='Amazon AU Sydney', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjSts6PnZLmAhWjzjgGHecTCUwQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F1298723%2Famazon_icon&psig=AOvVaw0jFGclV-prggRr8FYVOBf2&ust=1575213341548464', date='2019-01-23', amount=-100.99, bank_account_id=1, transaction_group_id=6),
    Transaction(name='Public Bar Pty Ltd Docklands', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwjkrbHRnpLmAhUVzzgGHY8xA1cQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.iconfinder.com%2Ficons%2F4018538%2Fcocktail_drinks_icon&psig=AOvVaw1ZWLStD9wIxC6S232LSmlo&ust=1575213747368138', date='2019-01-25', amount=-10, bank_account_id=1, transaction_group_id=9),
    Transaction(name='Withdrawal ATM CBA ATM', icon='https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=2ahUKEwijzsqunZLmAhW1zDgGHcH3A2UQjRx6BAgBEAQ&url=https%3A%2F%2Fwww.commbank.com.au%2F&psig=AOvVaw1l0OQ-RToTOtPDJDcIVIxu&ust=1575213406160310', date='2019-01-15', amount=-50, bank_account_id=1, transaction_group_id=10),
  ]

  # Cards

  all = [(transactionGroups, transaction_group_schema), (users, user_schema), (bankAccounts, bank_account_schema), (transactions, transaction_schema)]

  for model in all:
    for entry in model[0]:
      db.session.add(entry)
      db.session.commit()
      model[1].dump(entry)

  print("Finished adding data...")

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
    userId = int(request.form['userId'])

    account = BankAccount(accountName=accountName, bankName=bankName, verificationId=verificationId, accountType=accountType, user_id=userId)
    db.session.add(account)
    db.session.commit()
    bank_account_schema.dump(account)
    return make_response('Account created')
  elif request.method == 'GET':
    accounts = BankAccount.query.all()
    return bank_accounts_schema.jsonify(accounts)

@application.route('/accounts/<accId>', methods=['DELETE'])
def account_close(accId):
  task_to_delete = BankAccount.query.get_or_404(accId)
  try:
    db.session.delete(task_to_delete)
    db.session.commit()
    return 'Congrats'
  except:
    return 'there was an issue adding the data'

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
    name = request.form['name']
    icon = request.form['icon']
    date = request.form['date']
    amount = request.form['amount']
    bankAccountId = int(request.form['bankAccountId'])
    transactionGroupId = int(request.form['transactionGroupId'])

    transaction = Transaction(date=date, amount=amount, bank_account_id=bankAccountId, transaction_group_id=transactionGroupId)
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
  addSampleData()
  application.run(use_reloader=False)
