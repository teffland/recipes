from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session
import datetime

class Step(object):
    query = db_session.query_property()

    def __init__(self, recipe_id=None, number=None, title=None, instructions=None):
        self.recipe_id = recipe_id
        self.number = number
        self.title = title
        self.instructions = instructions

    def __repr__(self):
        return '<Step recipe_id=%i:number=%i>' % (self.recipe_id,self.number)


steps = Table('steps', metadata,
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('number', SmallInteger),
    Column('title', VARCHAR(128)),
    Column('instructions', TEXT),
    PrimaryKeyConstraint('recipe_id', 'number')
)
mapper(Step, steps)

