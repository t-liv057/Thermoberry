#!/usr/bin/python

import requests
from flask import Flask, render_template, request
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    relay_status = requests.get('192.168.1.69:80/status')
    return render_template('index.html', **relay_status)


if __name__ == '__main__':
    application.run(host='0.0.0.0')
