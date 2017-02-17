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
import json
# [START imports]
from flask import Flask, session, redirect, url_for, escape, request, render_template
from database import init_table
from insert import insert_user
from selection import select_user, select_user_by_id, select_user_by_email, select_user_by_username
from utils.utils import check_password_sha256, hash_password_sha256
from classes.user import User
from classes.error import Error
from utils.validate import validate_user_data

# [END imports]

app = Flask(__name__)
cnx = mysql.connector.connect(user='Udacity', password='UdacityFullStack',
                              host='188.121.44.181',
                              database='UdacityBackEnd')
init_table(cnx)
temp_salt = '1475asd'


def validate_session():
    if 'email' in session:
        print 'Session'
        current_email = session['email']
        current_password = session['password']
        current_user = select_user_by_email(cnx, email)
        if current_user is not None:
            if check_password_sha256(current_password, current_user.password, _user.password_salt):
                return current_user
    return None


def validate_cookie():
    if request.cookies.get('email') is not None:
        print 'Cookie'
        current_email = request.cookies.get('email')
        current_password = request.cookies.get('password')
        current_user = select_user_by_email(cnx, email)
        if current_user is not None:
            if check_password_sha256(current_password, current_user.password, _user.password_salt):
                return current_user
    return None


def set_session(_user):
    if _user is not None:
        session['email'] = _user.email
        session['password'] = hash_password_sha256(
            _user.password, _user.password_salt)
        return True
    return False


def set_cookie(_user):
    if _user is not None:
        resp.set_cookie('email', _user.email)
        resp.set_cookie('password', hash_password_sha256(
            _user.password, _user.password_salt))
        return True
    return False


@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'$'):
        return u'{1}{0:.2f}'.format(amount, currency)
    return dict(format_price=format_price)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print('TO DO Validate data')
    else:
        valid_session = validate_session()
        valid_cookie = validate_cookie()
        if valid_session is None and valid_cookie is None:
            return render_template('login.html')
        if valid_session is not None:
            set_session(valid_session)
        if valid_cookie is not None:
            set_cookie(valid_cookie)
            set_session(valid_cookie)
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_user = User._make((0, request.form.get('FirstName'), request.form.get('LastName'), request.form.get(
            'Username'), request.form.get('Email'), request.form.get('Password'), temp_salt))
        errors = validate_user_data(register_user, request.form.get('RetypePassword'))
        if len(errors) > 0:
            return render_template('register.html', user=register_user, error = errors)
        else:
            if(select_user_by_email(cnx, register_user.email) is not None):
                errors.append(Error('User Register', 'Email is associated with another account'))
                return render_template('register.html', user=register_user, error = errors)
            if(select_user_by_username(cnx, register_user.username) is not None):
                errors.append(Error('User Register', 'Username is taken by another user'))
                return render_template('register.html', user=register_user, error = errors)
            insert_user(cnx, register_user)
            return 'Success'

    else:
        valid_session = validate_session()
        valid_cookie = validate_cookie()
        if valid_session is None and valid_cookie is None:
            return render_template('register.html')
        if valid_session is not None:
            set_session(valid_session)
        if valid_cookie is not None:
            set_cookie(valid_cookie)
            set_session(valid_cookie)
        return redirect(url_for('index'))


@app.route('/user/')
@app.route('/user/<user_id>')
def get_user(user_id=None):
    return ("User " + str(user_id))


@app.route('/u/edit', methods=['GET', 'POST'])
def user_edit():
    return 'Error'


@app.route('/b/edit', methods=['GET', 'POST'])
def blog_edit():
    return 'Error'


@app.route('/')
def index():
    if 'email' in session:
        return render_template('main_page.html')
    else:
        return redirect(url_for('login', returnUrl='index'))


@app.errorhandler(404)
def error():
    return 'Error Page'
# [END form]
