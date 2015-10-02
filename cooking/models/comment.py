from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session

class Comment(object):
    query = db_session.query_property()

    def __init__(self, user_id=None, recipe_id=None, text=None):
        self.id = None
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.text = text
        self.created_at = None
        self.updated_at = None

    def __repr__(self):
        return '<Rating id=%i:user_id=%i:recipe_id=%i>' % (self.id,self.user_id,self.recipe_id)

def before_insert_listener(mapper, connection, target):
    target.created_at = datetime.datetime.now()
    target.updated_at = datetime.datetime.now() 
event.listen(Saved, 'before_insert', before_insert_listener)

def before_update_listener(mapper, connection, target):
    target.updated_at = datetime.datetime.now() 
event.listen(Saved, 'before_update', before_update_listener)

comments = Table('comments', metadata,
    Column('id', BIGINT, primary_key=True)
    Column('user_id', BIGINT, ForeignKey('users.id', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('text', TEXT),
    Column('created_at', TIMESTAMP),
    Column('updated_at', TIMESTAMP)
)
mapper(Comment, comments)
