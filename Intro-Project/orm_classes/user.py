from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import urllib, hashlib

Base = declarative_base()



class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(500), nullable=False)
    password = Column(String(100), nullable=False)
    password_salt = Column(String(100), nullable=False)

class Follower(Base):
    __tablename__ = 'Follower'
    user_id = Column(Integer, ForeignKey('User.id'), primary_key=True, autoincrement=False)
    following_id = Column(Integer, ForeignKey('User.id'), primary_key=True, autoincrement=False)

    follower = relationship("User", foreign_keys="Follower.following_id")
    following = relationship("User", foreign_keys="Follower.user_id")

engine = create_engine(
    'mysql+pymysql://Udacity:UdacityFullStack@188.121.44.181/UdacityBackEnd')
Base.metadata.create_all(engine)
