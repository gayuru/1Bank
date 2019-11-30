from flask import Flask
application = Flask(__name__)

@application.route('/')
def hello_world():
  return 'Hey its Python Flask application!'

if __name__ == '__main__':
  application.run()
