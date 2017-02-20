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
from orm_classes.blog import Category, Tag
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
    def create_gra(email):
        return create_gravatar(email)
    return dict(create_gra=create_gra)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


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
            session['username'] = registered_user.username
            return redirect(url_for('index'))

    else:
        return render_template('register.html')


@app.route('/about', methods=['GET'])
def about():
    current_username = session['username']
    user = db.get_user_by_username(current_username)
    return render_template('about.html', user=user)


@app.route('/')
def index():
    current_username = session['username']
    user = db.get_user_by_username(current_username)
    #db.follow_user(user.id, 2)
    following = db.get_user_following(user.id, 1, 9)
    followers = db.get_user_follower(user.id, 1, 9)
    categories = db.get_categories()
    tags = db.get_tags()
    return render_template('main_page.html',
                           gravatar_url=create_gravatar(user.email),
                           categories=categories,
                           followers=followers,
                           following=following,
                           tags=tags)


@app.route('/user/<int:user_id>', methods=['GET'])
def view_user(user_id):
    return view_user


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        return 'Search POST'
    else:
        all_users = db.get_users()
        current_user = db.get_user_by_username(session['username'])
        current_following =  db.get_user_following(
            current_user.id, page=1, page_size=9999)
        following_id_list = [o.following_id for o in current_following.data]
        print following_id_list
        return render_template('search.html', users=all_users,
                               following=following_id_list,
                               current_user=current_user)

    current_username = session['username']
    user = db.get_user_by_username(current_username)
    return 'Search'


@app.route('/following')
@app.route('/following/<int:user_id>')
def get_following(user_id=None):
    current_username = session['username']
    user = db.get_user_by_username(current_username)
    return 'Error'


@app.route('/follewers')
@app.route('/follewers/<int:user_id>')
def get_followers(user_id=None):
    current_username = session['username']
    user = db.get_user_by_username(current_username)
    return 'Error'


@app.route('/c')
def category_list():
    return render_template('category_list.html', category=db.get_categories())


@app.route('/c/edit', methods=['GET', 'POST'])
@app.route('/c/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id=None):
    if request.method == 'GET':
        if category_id:
            ex_cat = db.get_category(category_id)
            if ex_cat:
                return render_template('edit_cat.html', category=ex_cat)
            else:
                return redirect(url_for('edit_category'))
        else:
            return render_template('edit_cat.html')
    else:
        if category_id:
            ex_cat = db.get_category(category_id)
            if ex_cat:
                ex_cat.name = request.form.get('Name')
                if db.get_category_by_name(ex_cat.name):
                    errors = []
                    errors.append(Error('Existing Category',
                                        'Name is used by another category.'))
                    return render_template('edit_cat.html', category=ex_cat, errorr=errors)
                db.update_category(ex_cat)
                # TO DO: add redirect url
                return redirect(url_for('category_list'))
            else:
                # Maybe throw errors
                return redirect(url_for('category_list'))
        else:
            new_cat = Category(name=request.form.get('Name'))
            if db.get_category_by_name(new_cat.name):
                errors = []
                errors.append(Error('Existing Category',
                                    'Name is used by another category.'))
                return render_template('edit_cat.html', category=new_cat, error=errors)
            db.add_category(new_cat.name)
            # TO DO: add redirect url
            return redirect(url_for('category_list'))


@app.route('/t')
def tag_list():
    return render_template('tag_list.html', tag=db.get_tags())


@app.route('/t/edit', methods=['GET', 'POST'])
@app.route('/t/edit/<int:tag_id>', methods=['GET', 'POST'])
def edit_tag(tag_id=None):
    if request.method == 'GET':
        if tag_id:
            ex_tag = db.get_tag(tag_id)
            if ex_tag:
                return render_template('edit_tag.html', tag=ex_tag)
            else:
                return redirect(url_for('edit_tag'))
        else:
            return render_template('edit_tag.html')
    else:
        if tag_id:
            ex_tag = db.get_tag(tag_id)
            if ex_tag:
                ex_tag.name = request.form.get('Name')
                if db.get_tag_by_name(ex_tag.name):
                    errors = []
                    errors.append(Error('Existing Tag',
                                        'Name is used by another tag.'))
                    return render_template('edit_tag.html', tag=ex_tag, errorr=errors)
                db.update_tag(ex_tag)
                # TO DO: add redirect url
                return redirect(url_for('tag_list'))
            else:
                # Maybe throw errors
                return redirect(url_for('tag_list'))
        else:
            new_tag = Tag(name=request.form.get('Name'))
            if db.get_tag_by_name(new_tag.name):
                errors = []
                errors.append(Error('Existing Tag',
                                    'Name is used by another tag.'))
                return render_template('edit_tag.html', tag=new_tag, error=errors)
            db.add_tag(new_tag.name)
            # TO DO: add redirect url
            return redirect(url_for('tag_list'))


@app.route('/b')
def blog():
    return 'Get all the blocks'


@app.route('/b/edit/<blog_id>', methods=['GET', 'POST'])
def blog_edit(blog_id=None):
    return 'Error'


@app.route('/bc/<int:category_id>')
def category_blog(category_id):
    return 'Welcome ' + str(category_id)


@app.route('/bt/<int:tag_id>')
def tag_blog(tag_id):
    return 'Welcome ' + str(tag_id)


@app.route('/user/')
@app.route('/user/<user_id>')
def get_user(user_id=None):
    return ("User " + str(user_id))


@app.errorhandler(404)
def error():
    return 'Error Page'
# [END form]
