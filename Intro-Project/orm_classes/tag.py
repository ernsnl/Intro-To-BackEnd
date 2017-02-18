from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

engine = create_engine(
    'mysql+pymysql://Udacity:UdacityFullStack@188.121.44.181/UdacityBackEnd')
Base.metadata.create_all(engine)
