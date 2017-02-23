from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


FollowRelation = Table(
    'FollowRelation', Base.metadata,
    Column('follower_id', Integer, ForeignKey('User.id'),
           primary_key=True),
    Column('followee_id', Integer, ForeignKey('User.id'),
           primary_key=True)
)

LikeRelation = Table(
    'LikeRelation', Base.metadata,
    Column('blog_id', Integer, ForeignKey('Blog.id'),
           primary_key=True),
    Column('user_id', Integer, ForeignKey('User.id'),
           primary_key=True)
)

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(500), nullable=False)
    password = Column(String(100), nullable=False)
    password_salt = Column(String(100), nullable=False)

    blogs = relationship('Blog', back_populates='blog_user')
    comments = relationship('Comment', back_populates='comment_user')

    user_likes = relationship("Blog", secondary=LikeRelation, back_populates="blog_likes")

    followers = relationship("User", secondary=FollowRelation,
                             primaryjoin= id == FollowRelation.c.followee_id,
                             secondaryjoin= id == FollowRelation.c.follower_id
                             )

    following = relationship("User", secondary=FollowRelation,
                             primaryjoin= id == FollowRelation.c.follower_id,
                             secondaryjoin= id == FollowRelation.c.followee_id
                             )


class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    category_blogs = relationship('Blog', back_populates='blog_category')


TagRelation = Table(
    'TagRelation', Base.metadata,
    Column('blog_id', Integer, ForeignKey('Blog.id'),
           primary_key=True),
    Column('tag_id', Integer, ForeignKey('Tag.id'),
           primary_key=True)
)


class Tag(Base):
    __tablename__ = 'Tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    tag_blogs = relationship(
        "Blog", secondary=TagRelation, back_populates="blog_tags")




class Blog(Base):
    __tablename__ = 'Blog'
    id = Column(Integer, primary_key=True)
    blog_title = Column(String(150), nullable=False)
    blog_content = Column(String(1000), nullable=False)
    blog_category_id = Column(Integer, ForeignKey('Category.id'))
    blog_category = relationship('Category', back_populates='category_blogs')
    blog_user_id = Column(Integer, ForeignKey('User.id'))
    blog_user = relationship('User',  back_populates='blogs')
    blog_date = Column(DateTime, nullable=False)
    blog_comments = relationship('Comment', back_populates='comment_blog')
    blog_tags = relationship(
        "Tag", secondary=TagRelation, back_populates="tag_blogs")

    blog_likes = relationship("User", secondary=LikeRelation, back_populates="user_likes")


class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True)
    comment_content = Column(String(500), nullable=False)
    comment_blog_id = Column(Integer, ForeignKey('Blog.id'))
    comment_blog = relationship('Blog', back_populates='blog_comments')
    comment_user_id = Column(Integer, ForeignKey('User.id'))
    comment_user = relationship('User', back_populates='comments')
    comment_date = Column(DateTime, nullable=False)

engine = create_engine(
    'mysql+pymysql://Udacity:UdacityFullStack@188.121.44.181/UdacityBackEnd')
Base.metadata.create_all(engine)
