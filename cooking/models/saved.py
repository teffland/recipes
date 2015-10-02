from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session
import datetime

class Saved(object):
    query = db_session.query_property()

    def __init__(self, user_id=None, recipe_id=None, saved_at=None):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.saved_at = saved_at

    def __repr__(self):
        return '<Saved user_id=%i:recipe_id=%i>' % (self.user_id,self.recipe_id)

def before_insert_listener(mapper, connection, target):
    target.saved_at = datetime.datetime.now()
event.listen(Saved, 'before_insert', before_insert_listener)


saved = Table('saved', metadata,
    Column('user_id', BIGINT, ForeignKey('users.id', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('saved_at', TIMESTAMP),
    PrimaryKeyConstraint('user_id', 'recipe_id')
)
mapper(Saved, saved)
