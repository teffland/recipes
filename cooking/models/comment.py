from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session, engine
import datetime
from models.base_model import BaseModel
import models

class Comment(object):
    query = db_session.query_property()

    def __init__(self, user_id=None, recipe_id=None, text=None):
        self.id = None
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.text = text
        self.created_at = None
        self.updated_at = None

    @classmethod
    def load_comments(cls, recipe_id):
        attributes = ['id', 'user_id', 'text', 'created_at', 'updated_at']
        results = engine.execute("SELECT %s FROM comments WHERE recipe_id=%s ORDER BY created_at ASC" % (",".join(attributes), '%s'), long(recipe_id))
        comments = []
        for result in results:
            comment = Comment()
            comment.id = long(result[0])
            comment.user_id = long(result[1])
            comment.text = result[2]
            comment.created_at = result[3]
            comment.updated_at = result[4]
            comment.creator = models.user.User.load_user_by_id(comment.user_id)

            comments.append(comment)

        return comments

    @classmethod
    def load_last_comment(cls, recipe_id):
        attributes = ['id', 'user_id', 'text', 'created_at', 'updated_at']
        results = engine.execute("SELECT %s FROM comments WHERE recipe_id=%s ORDER BY created_at DESC LIMIT 1" % (",".join(attributes), '%s'), long(recipe_id))
        comment = None
        for result in results:
            comment = Comment()
            comment.id = long(result[0])
            comment.user_id = long(result[1])
            comment.text = result[2]
            comment.created_at = result[3]
            comment.updated_at = result[4]
            comment.creator = models.user.User.load_user_by_id(comment.user_id)

        return comment

    @classmethod
    def create_comment(cls, user, recipe_id, text):
        user_id = long(user.id)
        recipe_id = long(recipe_id)
        created_at = datetime.datetime.now()
        updated_at = created_at

        engine.execute("INSERT INTO comments (user_id, recipe_id, text, created_at, updated_at) VALUES (%s,%s,%s,%s,%s)", (user_id, recipe_id, text, BaseModel.timestamp_to_db(created_at), BaseModel.timestamp_to_db(updated_at)))

    @classmethod
    def delete_comment(cls, comment_id, user_id):
        engine.execute("DELETE FROM comments WHERE id=%s AND user_id=%s", (
            comment_id,
            user_id
        ))

    def commented_at_string(self):
        return self.created_at.strftime('%m/%d/%y %H:%M')

    def __repr__(self):
        return '<Comment id=%i:user_id=%i:recipe_id=%i>' % (self.id,self.user_id,self.recipe_id)

def before_insert_listener(mapper, connection, target):
    target.created_at = datetime.datetime.now()
    target.updated_at = datetime.datetime.now() 
event.listen(Comment, 'before_insert', before_insert_listener)

def before_update_listener(mapper, connection, target):
    target.updated_at = datetime.datetime.now() 
event.listen(Comment, 'before_update', before_update_listener)

comments = Table('comments', metadata,
    Column('id', BIGINT, primary_key=True),
    Column('user_id', BIGINT, ForeignKey('users.id', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('text', TEXT),
    Column('created_at', TIMESTAMP),
    Column('updated_at', TIMESTAMP)
)
mapper(Comment, comments)
