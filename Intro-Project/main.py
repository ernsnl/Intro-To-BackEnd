# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
import mysql.connector
# [START imports]
from flask import Flask, render_template, request
from database import init_table
# [END imports]

app = Flask(__name__)
cnx = mysql.connector.connect(user='Udacity', password='UdacityFullStack',
                              host='188.121.44.181',
                              database='UdacityBackEnd')
cursor = cnx.cursor()
init_table(cursor)


@app.context_processor
def utility_processor():
  def format_price(amount, currency=u'$'):
    return u'{1}{0:.2f}'.format(amount, currency)
  return dict(format_price=format_price)

@app.route('/')
def index():
    return render_template('main_page.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('TO DO Validate data')
    else:
        return render_template('login.html')

@app.route('/register',methods= ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print('TO DO Validate data')
    else:
        return render_template('register.html')

@app.route('/user/')
@app.route('/user/<user_id>')
def get_user(user_id=None):
    return ("User "  + str(user_id))


@app.route('/publish', methods = ['POST'])
def publish():
    return 'Error'
# [END form]
