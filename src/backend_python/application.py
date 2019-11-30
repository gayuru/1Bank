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

db.create_all()
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



if __name__ == '__main__':
  application.run()
