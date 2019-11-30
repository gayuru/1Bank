from flask import Flask
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

@application.route('/')
def hello_world():
  return 'iSwift'

if __name__ == '__main__':
  application.run()
