from sqlalchemy.types import *
from sqlalchemy import Table, Column
from sqlalchemy.orm import mapper
from cooking.orm_setup import metadata, db_session, engine
import datetime


class Category(object):
    query = db_session.query_property()

    def __init__(self, name=None, description=None):
        self.id = None
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Category name=%i>' % (self.name)

    @classmethod
    def load_categories(cls, recipe_id):
        attributes = ['name', 'description']
        results = engine.execute("SELECT %s FROM categories_recipes JOIN categories ON categories_recipes.category_id=categories.id WHERE recipe_id=%i ORDER BY name ASC" % (",".join(attributes), long(recipe_id)))
        categories = []
        for result in results:
            category = Category()
            category.name = result[0]
            category.description = result[1]
            categories.append(category)

        return categories


categories = Table('categories', metadata,
    Column('id', BIGINT, primary_key=True),
    Column('name', VARCHAR(128)),
    Column('description', TEXT)
)
mapper(Category, categories)


