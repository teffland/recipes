from sqlalchemy.types import *
from sqlalchemy import Table, Column
from sqlalchemy.orm import mapper
from cooking.orm_setup import metadata, db_session
import datetime


class Category(object):
    query = db_session.query_property()

    def __init__(self, name=None, description=None):
        self.id = None
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Category name=%i>' % (self.name)


categories = Table('categories', metadata,
    Column('id', BIGINT, primary_key=True),
    Column('name', VARCHAR(128)),
    Column('description', TEXT)
)
mapper(Category, categories)


