from orm_classes.orm import User, Category, Tag, FollowRelation, LikeRelation, Blog, Comment, TagRelation
from classes.list_result import ListResult
from sqlalchemy.orm import sessionmaker
from utils.utils import check_password_sha256, hash_password_sha256, generate_random_string


class DatabaseOperations:

    def __init__(self, session):
        self.session = session

    def add_user(self, first_name, last_name, username, email, password, password_salt):
        try:
            password_salt = generate_random_string(10)
            newUser = User(first_name=first_name, last_name=last_name, username=username,
                           password=hash_password_sha256(password, password_salt), email=email, password_salt=password_salt)
            self.session.add(newUser)
            self.session.commit()
            self.session.refresh(newUser)
            return newUser
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_users(self, page=1, page_size=25):
        try:
            return ListResult(self.session.query(User).order_by(User.id).all(), 0, page, page_size)
        except Exception as e:
            print e
        finally:
            print 'Done'


    def get_users_by_username(self, name, page=1, page_size=25):
        try:
            return ListResult(self.session.query(User).filter(User.username.contains(name)).all(), 0, page, page_size)
        except Exception as e:
            print e
        finally:
            print 'Done'
    def get_user(self, id):
        try:
            return self.session.query(User).filter(User.id == id).first()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_user_by_email(self, email):
        try:
            return self.session.query(User).filter(User.email == email).one()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_user_by_username(self, username):
        try:
            return self.session.query(User).filter(User.username == username).one()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def follow_user(self, user, following_user):
        try:
            self.session.execute(FollowRelation.insert().values(
                [(user.id, following_user.id)]))
            self.session.refresh(user)
        except Exception as e:
            print e
        finally:
            print 'Done'

    def unfollow_user(self, user, unfollow_user):
        try:
            self.session.execute(FollowRelation.delete(user.id == FollowRelation.c.follower_id
                                                       and unfollow_user.id == FollowRelation.c.followee_id))
            self.session.refresh(user)
        except Exception as e:
            print e
        finally:
            print 'Done'

    def like_blog(self, user, blog):
        try:
            self.session.execute(LikeRelation.insert().values(
                [(blog.id, user.id)]))
            self.session.refresh(user)
        except Exception as e:
            print e
        finally:
            print 'Done'

    def unlike_blog(self, user, blog):
        try:
            self.session.execute(LikeRelation.delete(user.id == LikeRelation.c.user_id
                                                     and blog.id == LikeRelation.c.blog_id))
            self.session.refresh(user)
        except Exception as e:
            print e
        finally:
            print 'Done'

    def comment_blog(self, comment):
        try:
            self.session.add(comment)
            self.session.commit()
            self.session.refresh(comment)
            return comment
        except Exception as e:
            print e
        finally:
            print 'Done'

    def delete_comment(self, comment):
        try:
            self.session.commit()
            self.session.refresh(comment)
            return comment
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_categories(self, page=1, page_size=25):
        try:
            cat_list = ListResult(self.session.query(Category).all(),
                                  0, page, page_size)
            return cat_list
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_category(self, id):
        try:
            return self.session.query(Category).filter(Category.id == id).first()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_category_by_name(self, name):
        try:
            return self.session.query(Category).filter(Category.name == name).first()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def add_category(self, name):
        try:
            category = Category(name=name)
            self.session.add(category)
            self.session.commit()
            self.session.refresh(category)
            return category
        except Exception as e:
            print e
        finally:
            print 'Done'

    def update_category(self, category):
        try:
            existing_cat = self.session.query(Category).get(category.id)
            existing_cat.name = category.name
            self.session.commit()
            return existing_cat
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_tags(self, page=1, page_size=25):
        try:
            tag_list = ListResult(self.session.query(Tag).order_by(
                Tag.name).all(),
                0, page, page_size)
            return tag_list
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_tag(self, id):
        try:
            return self.session.query(Tag).filter(Tag.id == id).first()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_tag_by_name(self, name):
        try:
            return self.session.query(Tag).filter(Tag.name == name).first()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def add_tag(self, name):
        try:
            tag = Tag(name=name)
            self.session.add(tag)
            self.session.commit()
            self.session.refresh(tag)
            return tag
        except Exception as e:
            print e
        finally:
            print 'Done'

    def update_tag(self, tag):
        try:
            existing_tag = self.session.query(Tag).get(tag.id)
            existing_tag.name = tag.name
            self.session.commit()
            return existing_tag
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_blogs(self, page=1, page_size=25):
        try:
            return ListResult(self.session.query(Blog).order_by(
                Blog.blog_date).all(),
                0, page, page_size)
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_blog(self, id):
        try:
            return self.session.query(Blog).filter(Blog.id == id).first()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def add_blog(self, blog, blog_tags):
        try:
            self.session.add(blog)
            self.session.commit()
            self.session.refresh(blog)
            for tag in blog_tags:
                self.session.execute(
                    TagRelation.insert().values([(blog.id, tag.id)]))
            self.session.refresh(blog)
            return blog
        except Exception as e:
            print e
        finally:
            print 'Done'

    def delete_blog(self, blog):
        try:
            self.session.delete(blog)
            self.session.commit()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def update_blog(self, blog, blog_tags):
        try:
            self.session.commit()
            self.session.refresh(blog)
            self.session.execute(TagRelation.delete(
                blog.id == TagRelation.c.blog_id))
            for tag in blog_tags:
                self.session.execute(TagRelation.insert().values(
                    [(blog.id, tag.id)]))
            self.session.refresh(blog)
            return blog
        except Exception as e:
            print e
        finally:
            print 'Done'

    def get_comment(self, comment_id):
        try:
            return self.session.query(Comment).filter(Comment.id == comment_id).first()
        except Exception as e:
            print e
        finally:
            print 'Done'

    def delete_comment(self, comment):
        try:
            self.session.delete(comment)
            self.session.commit()
        except Exception as e:
            print e
        finally:
            print 'Done'
