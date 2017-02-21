from orm_classes.user import User, Category, Tag, FollowRelation, LikeRelation, Blog, Comment
from classes.list_result import ListResult
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

    def get_users(self, page=1, page_size=25):
        return ListResult(session.query(User).order_by(User.id).all(), session.query(User).count(), page, page_size)

    def get_user(self, id):
        return session.query(User).filter(User.id == id).first()

    def get_user_by_email(self, email):
        try:
            if engine.dialect.has_table(engine, User.__tablename__):
                return session.query(User).join(FollowRelation).filter(User.email == email).first()
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
            print e
            return None
        else:
            pass

    def follow_user(self, user, following_user):
        session.execute(FollowRelation.insert().values(
            [(user.id, following_user.id)]))

    def unfollow_user(self, user, unfollow_user):
        try:
            session.execute(FollowRelation.delete(user.id == FollowRelation.c.follower_id
                                                  and unfollow_user.id == FollowRelation.c.followee_id))
        except Exception as e:
            print e
        else:
            pass

    def get_categories(self, page=1, page_size=25):
        cat_list = ListResult(session.query(Category).order_by(
            Category.name).all(),
            session.query(Category).order_by(Category.id).count(), page, page_size)
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

    def get_tags(self, page=1, page_size=25):
        tag_list = ListResult(session.query(Tag).order_by(
            Tag.name).all(),
            session.query(Tag).order_by(Tag.id).count(), page, page_size)
        return tag_list

    def get_tag(self, id):
        return session.query(Tag).filter(Tag.id == id).first()

    def get_tag_by_name(self, name):
        return session.query(Tag).filter(Tag.name == name).first()

    def add_tag(self, name):
        tag = Tag(name=name)
        session.add(tag)
        session.flush()
        session.refresh(tag)
        return tag

    def update_tag(self, tag):
        existing_tag = session.query(Tag).get(tag.id)
        existing_tag.name = tag.name
        session.commit()
        return existing_tag
