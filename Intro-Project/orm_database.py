from orm_classes.user import User
from orm_classes.category import Category
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.utils import check_password_sha256, hash_password_sha256, generate_random_string

Base = declarative_base()

engine = create_engine(
    'mysql+pymysql://Udacity:UdacityFullStack@188.121.44.181/UdacityBackEnd')
Base.metadata.bind = engine
database_session = sessionmaker(bind=engine)
session = database_session()


class DatabaseOperations:

    def add_user(self, first_name, last_name, username, email, password, password_salt):

        password_salt = generate_random_string(10)
        newUser = User(first_name=first_name, last_name=last_name, username=username,
                       password=hash_password_sha256(password, password_salt), email=email, password_salt=password_salt)
        session.add(newUser)
        session.flush()
        session.refresh(newUser)
        print newUser.id
        return newUser

    def get_users(self):
        user_list = []
        for _u in session.query(User).order_by(User.id):
            user_list.append(_u)
        return user_list

    def get_user_by_email(self, email):
        try:
            if engine.dialect.has_table(engine, User.__tablename__):
                return session.query(User).filter(User.email == email).first()
            return None
        except Exception as e:
            return None
        else:
            pass

    def get_user_by_username(self, username):
        try:
            if engine.dialect.has_table(engine, User.__tablename__):
                return session.query(User).filter(User.username == username).first()
            return None
        except Exception as e:
            return None
        else:
            pass

    def get_categories(self):
        cat_list = []
        for _c in session.query(Category).order_by(Category.id):
            cat_list.append(_c)
        return cat_list

    def get_category(self, id):
        return session.query(Category).filter(Category.id == id).first()

    def get_category_by_name(self, name):
        return session.query(Category).filter(Category.name == name).first()

    def add_category(self, name):
        category = Category(name=name)
        session.add(category)
        session.flush()
        session.refresh(category)
        return category

    def update_category(self, category):
        existing_cat = session.query(Category).get(category.id)
        existing_cat.name = category.name
        session.commit()
        return existing_cat
