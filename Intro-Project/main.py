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
from utils.utils import check_password_sha256, hash_password_sha256, create_gravatar
from orm_classes.user import User
from orm_classes.category import Category
from classes.error import Error
from utils.validate import validate_user_data, validate_login_data
from orm_database import DatabaseOperations


# [END imports]

app = Flask(__name__, static_url_path='/build')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
db = DatabaseOperations()
temp_salt = '1475asd'


@app.before_request
def before_request():
    if 'username' not in session:
        if request.endpoint != 'login' and request.endpoint != 'register':
            return redirect(url_for('login', returnUrl=request.path))


@app.context_processor
def utility_processor():
    def format_price(amount, currency=u'$'):
        return u'{1}{0:.2f}'.format(amount, currency)
    return dict(format_price=format_price)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/about', methods=['GET'])
def about():
    current_username = session['username']
    user = db.get_user_by_username(current_username)
    return render_template('about.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_user = User(password=request.form.get('Password'),
                          email=request.form.get('Email'), first_name='', last_name='', password_salt='', username='')
        errors = validate_login_data(login_user)
        if(len(errors) > 0):
            return render_template('login.html', user=login_user, error=errors)
        else:
            if(db.get_user_by_email(login_user.email) is None):
                errors.append(
                    Error('User Login', 'Email is not associated with any account.'))
            else:
                existing_user = db.get_user_by_email(login_user.email)
                if(check_password_sha256(existing_user.password, login_user.password, existing_user.password_salt)):
                    print existing_user.username
                    session['username'] = existing_user.username

                    print 'Remember ME: ' + str(request.form.get('RememberMe'))
                    return redirect(url_for('index'))
                else:
                    errors.append(
                        Error('User Login', 'Email and password don\'t match.'))
                    return render_template('login.html', user=login_user, error=errors)
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        register_user = User(first_name=request.form.get('FirstName'), last_name=request.form.get('LastName'),
                             username=request.form.get('Username'), password=request.form.get('Password'),
                             email=request.form.get('Email'), password_salt=temp_salt)
        errors = validate_user_data(
            register_user, request.form.get('RetypePassword'))
        if len(errors) > 0:
            return render_template('register.html', user=register_user, error=errors)
        else:
            if(db.get_user_by_email(register_user.email) is not None):
                errors.append(
                    Error('User Register', 'Email is associated with another account'))
                return render_template('register.html', user=register_user, error=errors)
            if(db.get_user_by_username(register_user.username) is not None):
                errors.append(
                    Error('User Register', 'Username is taken by another user'))
                return render_template('register.html', user=register_user, error=errors)
            registered_user = db.add_user(first_name=register_user.first_name, last_name=register_user.last_name,
                                          username=register_user.username, email=register_user.email,
                                          password=register_user.password, password_salt=register_user.password_salt)
            return redirect(url_for('index'))

    else:
        return render_template('register.html')


@app.route('/')
def index():
    current_username = session['username']
    user = db.get_user_by_username(current_username)
    print create_gravatar(user.email)
    return render_template('main_page.html', gravatar_url=create_gravatar(user.email))


@app.route('/c/edit', methods=['GET', 'POST'])
@app.route('/c/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id=None):
    if request.method == 'GET':
        if category_id:
            ex_cat = db.get_category(category_id)
            return render_template('edit_cat.html', category=ex_cat)
        else:
            return render_template('edit_cat.html')
    else:
        print category_id
        if category_id:
            ex_cat = db.get_category(category_id)
            if ex_cat:
                ex_cat.name = request.form.get('Name')
                if db.get_category_by_name(ex_cat.name):
                    errors = []
                    errors.append(Error('Existing Category', 'Name is used by another category.'))
                    return render_template('edit_cat.html', category=ex_cat, errorr=errors)
                db.update_category(ex_cat)
                #TO DO: add redirect url
                return redirect(url_for('index'))
            else:
                #Maybe throw errors
                return redirect(url_for('index'))
        else:
            new_cat = Category(name=request.form.get('Name'))
            if db.get_category_by_name(new_cat.name):
                errors = []
                errors.append(Error('Existing Category', 'Name is used by another category.'))
                return render_template('edit_cat.html', category=new_cat, error=errors)
            db.add_category(new_cat.name)
            #TO DO: add redirect url
            return redirect(url_for('index'))


@app.route('/user/')
@app.route('/user/<user_id>')
def get_user(user_id=None):
    return ("User " + str(user_id))


@app.route('/b/view/<blog_id>', methods=['GET'])
def view_blog(blog_id=None):
    return 'Error'


@app.route('/b/edit/<blog_id>', methods=['GET', 'POST'])
def blog_edit(blog_id=None):
    return 'Error'


@app.errorhandler(404)
def error():
    return 'Error Page'
# [END form]
