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
import json
import datetime
# [START imports]
from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response
from utils.utils import check_password_sha256, hash_password_sha256, create_gravatar
from orm_classes.orm import User, Category, Tag, Blog, Comment
from classes.error import Error
from classes.list_result import ListResult
from utils.validate import validate_user_data, validate_login_data

from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from orm_database import DatabaseOperations


# [END imports]

app = Flask(__name__, static_url_path='/build')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

Base = declarative_base()

engine = create_engine(
    'mysql+pymysql://Udacity:UdacityFullStack@188.121.44.181/UdacityBackEnd')
Base.metadata.bind = engine
Base.metadata.create_all(engine)

temp_salt = '1475asd'


@app.before_request
def before_request():
    if 'username' not in session:
        if request.endpoint != 'login' and request.endpoint != 'register':
            return redirect(url_for('login', returnUrl=request.path))
    else:
        if request.endpoint == 'login' or request.endpoint == 'register':
            return redirect(url_for('index'))


@app.context_processor
def utility_processor():
    def create_gra(email):
        return create_gravatar(email)

    def shorthen_content(content):
        return content if len(content) < 150 else content[0:150] + "..."
    return dict(create_gra=create_gra, shorthen_content=shorthen_content)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        if request.method == 'POST':
            login_user = User(password=request.form.get('Password'),
                              email=request.form.get('Email'), first_name='', last_name='', password_salt='', username='')

            errors = validate_login_data(login_user)
            if(len(errors) > 0):
                return render_template('login.html', user=login_user, error=errors)
            else:
                if db.get_user_by_email(login_user.email) is None:
                    errors.append(
                        Error('User Login', 'Email is not associated with any account.'))
                else:
                    existing_user = db.get_user_by_email(login_user.email)
                    if(check_password_sha256(existing_user.password, login_user.password, existing_user.password_salt)):
                        print existing_user.username
                        session['username'] = existing_user.username
                        return redirect(url_for('index'))
                    else:
                        errors.append(
                            Error('User Login', 'Email and password don\'t match.'))
                        return render_template('login.html', user=login_user, error=errors)
        else:
            return render_template('login.html')
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
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
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/about', methods=['GET'])
@app.route('/about/<int:user_id>', methods=['GET'])
def about(user_id=None):
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        if user_id is None:
            current_username = session['username']
            user = db.get_user_by_username(current_username)
            return render_template('about.html', user=user)
        else:
            user = db.get_user(user_id)
            return render_template('about.html', user=user)
    except Exception as e:
        print e
    finally:
        current_session.close()



@app.route('/')
def index():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        current_username = session['username']
        user = db.get_user_by_username(current_username)
        categories = db.get_categories()
        tags = db.get_tags()
        posts = user.blogs
        return render_template('main_page.html',
                               current_user=user,
                               viewed_user=user,
                               gravatar_url=create_gravatar(user.email),
                               categories=categories,
                               followers=user.followers,
                               following=user.following,
                               tags=tags,
                               blogs=posts)
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/search', methods=['GET', 'POST'])
def search():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        if request.method == 'POST':
            all_users = db.get_users()
            if len(str(request.form.get('u')).strip()) > 0:
                all_users = db.get_users_by_username(str(request.form.get('u')).strip())
            current_user = db.get_user_by_username(session['username'])
            following_id_list = [o.id for o in current_user.following]
            return render_template('search.html',
                                   users=all_users,
                                   following=following_id_list,
                                   current_user=current_user,
                                   search_text= request.form.get('u').strip())
        else:
            all_users = db.get_users()
            current_user = db.get_user_by_username(session['username'])
            following_id_list = [o.id for o in current_user.following]
            return render_template('search.html',
                                   users=all_users,
                                   following=following_id_list,
                                   current_user=current_user)
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/user/')
@app.route('/user/<int:user_id>')
def view_user(user_id=None):
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        if user_id:
            current_user = db.get_user_by_username(session['username'])
            print current_user.user_likes
            if user_id == current_user.id:
                return redirect(url_for('index'))
            request_user = db.get_user(id=user_id)
            if request_user is None:
                return redirect(url_for('index'))
            categories = db.get_categories()
            tags = db.get_tags()
            return render_template('main_page.html',
                                   current_user=current_user,
                                   viewed_user=request_user,
                                   gravatar_url=create_gravatar(
                                       request_user.email),
                                   categories=categories,
                                   followers=request_user.followers,
                                   following=request_user.following,
                                   tags=tags,
                                   blogs=request_user.blogs)

        return redirect(url_for('index'))
    except Exception as e:
        print e
    finally:
        current_session.close()



@app.route('/follow', methods=['GET'])
def follow():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        follow_id = request.args.get('follow_id')
        if follow_id:
            current_user = db.get_user_by_username(session['username'])
            follow_user = db.get_user(follow_id)
            print follow_user in current_user.following
            if not follow_user in current_user.following:
                db.follow_user(current_user, follow_user)
                return 'Success#Unfollow'
            else:
                db.unfollow_user(current_user, follow_user)
                return 'Success#Follow'
    except Exception as e:
        print e
    finally:
        current_session.close()



@app.route('/like', methods=['GET'])
def like():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        blog_id = request.args.get('post_id')
        if blog_id:
            current_user = db.get_user_by_username(session['username'])
            like_blog = db.get_blog(blog_id)
            if not like_blog in current_user.user_likes:
                db.like_blog(current_user, like_blog)
                return 'Success#Dislike'
            else:
                db.unlike_blog(current_user, like_blog)
                return 'Success#Like'
    except Exception as e:
        print e
    finally:
        current_session.close()



@app.route('/comment', methods=['GET', 'POST'])
def comment():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        if request.method == 'POST':
            current_user = db.get_user_by_username(session['username'])
            current_blog = request.form.get('BlogID')
            comment_content = request.form.get('Content')
            new_comment = Comment(comment_user_id=current_user.id, comment_blog_id=current_blog,comment_content=comment_content, comment_date=datetime.datetime.now())
            db.comment_blog(new_comment)
            return redirect(url_for('view_blog', id=current_blog))
        else:
            return 'Error'
    except Exception as e:
        print e
    finally:
        current_session.close()



@app.route('/categorylist')
def category_list():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        return render_template('category_list.html', category=db.get_categories())
    except Exception as e:
        print e
    finally:
        current_session.close()



@app.route('/category/edit', methods=['GET', 'POST'])
@app.route('/category/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id=None):
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
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
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/taglist')
def tag_list():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        return render_template('tag_list.html', tag=db.get_tags())
    except Exception as e:
        print e
    finally:
        current_session.close()



@app.route('/tag/edit', methods=['GET', 'POST'])
@app.route('/tag/edit/<int:tag_id>', methods=['GET', 'POST'])
def edit_tag(tag_id=None):
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
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
                    if db.get_tag_by_name(request.form.get('Name')):
                        print 'asdasd'
                        ex_tag.name = request.form.get('Name')
                        errors = []
                        errors.append(Error('Existing Tag',
                                            'Name is used by another tag.'))
                        return render_template('edit_tag.html', tag=ex_tag, errorr=errors)
                    ex_tag.name = request.form.get('Name')
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
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/posts')
def blog_posts():
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        current_user = db.get_user_by_username(session['username'])
        return render_template('blog_list.html', blogs=db.get_blogs(), current_user=current_user)
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/category_post/<int:category_id>')
def category_blog(category_id):
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        category = db.get_category(category_id)
        blogs = ListResult(category.category_blogs, 0, 0, 0)
        current_user = db.get_user_by_username(session['username'])
        return render_template('blog_list.html', blogs=blogs, current_user=current_user)
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/tag_post/<int:tag_id>')
def tag_blog(tag_id):
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        tag = db.get_tag(tag_id)
        blogs = ListResult(tag.tag_blogs, 0, 0, 0)
        current_user = db.get_user_by_username(session['username'])
        return render_template('blog_list.html', blogs=blogs, current_user=current_user)
    except Exception as e:
        print e
    else:
        current_session.close()


@app.route('/view', methods=['GET'])
def view_blog():
    post_id = request.args.get('id')
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        current_blog = db.get_blog(post_id)
        if current_blog is not None:
            current_username = session['username']
            user = db.get_user_by_username(current_username)
            categories = db.get_categories()
            tags = db.get_tags()
            return render_template('blog.html',current_user=user,categories=categories,tags=tags,blog=current_blog)
        else:
            return redirect(url_for('index'))
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.route('/posts/edit', methods=['GET', 'POST'])
@app.route('/posts/edit/<int:blog_id>', methods=['GET', 'POST'])
def edit_blog(blog_id=None):
    database_session = sessionmaker(bind=engine)
    current_session = database_session()
    db = DatabaseOperations(current_session)
    try:
        current_user = db.get_user_by_username(session['username'])
        if request.method == 'POST':
            if blog_id:
                get_existing_blog = db.get_blog(blog_id)
                get_existing_blog.blog_title = request.form.get('Title')
                get_existing_blog.blog_content = request.form.get('Content')
                get_existing_blog.blog_category_id = request.form.get(
                    'Category')
                get_existing_blog.blog_user = current_user
                blog_tags = []
                for tag in request.form.getlist('Tags'):
                    blog_tags.append(db.get_tag(int(tag)))
                db.update_blog(get_existing_blog, blog_tags)
                return redirect(url_for('blog_posts'))
            else:
                new_blog = Blog()
                new_blog.blog_title = request.form.get('Title')
                new_blog.blog_content = request.form.get('Content')
                new_blog.blog_category_id = request.form.get('Category')
                new_blog.blog_user = current_user
                new_blog.blog_date = datetime.datetime.now()
                new_blog.blog_tags = []
                blog_tags = []
                for tag in request.form.getlist('Tags'):
                    blog_tags.append(db.get_tag(int(tag)))
                db.add_blog(new_blog, blog_tags)
                return redirect(url_for('blog_posts'))
        else:
            if blog_id is None:
                return render_template('edit_blog.html',
                                       categories=db.get_categories(),
                                       tags=db.get_tags())
            else:
                requested_blog = db.get_blog(blog_id)
                if requested_blog and requested_blog.blog_user_id == current_user.id:
                    return render_template('edit_blog.html',
                                           categories=db.get_categories(),
                                           tags=db.get_tags(),
                                           blog=requested_blog)
                else:
                    return redirect(url_for('blog_posts'))
    except Exception as e:
        print e
    finally:
        current_session.close()


@app.errorhandler(404)
def error():
    return 'Error Page'
# [END form]
