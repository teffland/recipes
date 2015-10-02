from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session

class Rating(object):
    query = db_session.query_property()

    def __init__(self, user_id=None, recipe_id=None, rating=None):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.rating = rating

    def __repr__(self):
        return '<Rating user_id=%i:recipe_id=%i:rating=%i>' % (self.user_id,self.recipe_id,self.rating)


ratings = Table('ratings', metadata,
    Column('user_id', BIGINT, ForeignKey('users.id', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('rating', SmallInteger),
    PrimaryKeyConstraint('user_id', 'recipe_id')
)
mapper(Rating, ratings)
