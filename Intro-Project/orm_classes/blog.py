from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


engine = create_engine(
    'mysql+pymysql://Udacity:UdacityFullStack@188.121.44.181/UdacityBackEnd')
Base.metadata.create_all(engine)
