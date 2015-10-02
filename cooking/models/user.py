from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session
import datetime
import hashlib
from models.recipe import Recipe, recipes
from models.rating import Rating
from models.saved import Saved
from models.comment import Comment


class User(object):
    query = db_session.query_property()

    def __init__(self, email=None, first_name=None, last_name=None, icon_code=0, password=None):
        self.id = None
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.icon_code = icon_code
        self.created_at = None
        self.last_login_at = None
        self.hashed_password = User.hash_password(password)

    @classmethod
    def hash_password(cls, password):
        if password:
            sha = hashlib.sha384()
            sha.update(password)
            return sha.digest().encode('base64')
        else:
            return None

    def __repr__(self):
        return '<User id=%s:email=%r>' % (self.id,self.email)

def before_insert_listener(mapper, connection, target):
    target.created_at = datetime.datetime.now()
    target.last_login_at = datetime.datetime.now()
event.listen(User, 'before_insert', before_insert_listener)

users = Table('users', metadata,
    Column('id', BIGINT, primary_key=True),
    Column('email', VARCHAR(128)),
    Column('first_name', VARCHAR(128)),
    Column('last_name', VARCHAR(128)),
    Column('hashed_password', VARCHAR(128)),
    Column('icon_code', SmallInteger),
    Column('created_at', TIMESTAMP),
    Column('last_login_at', TIMESTAMP)
)
mapper(User, users, properties={
    'recipes' : relationship(Recipe, backref='creator', foreign_keys=[recipes.c.creator_id]),
    'ratings': relationship(Rating, backref='user'),
    'saved': relationship(Saved, backref='user'),
    'comments': relationship(Comment, backref='user')
})


