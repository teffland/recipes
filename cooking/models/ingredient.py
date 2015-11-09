from sqlalchemy.types import *
from sqlalchemy import Table, Column
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session
import datetime
from models.ingredients_recipes import IngredientRecipe
from collections import defaultdict


class Ingredient(object):
    query = db_session.query_property()

    def __init__(self, name=None):
        self.id = None
        self.name = name

    def __repr__(self):
        return '<Ingredient name=%i>' % (self.name)



ingredients = Table('ingredients', metadata,
    Column('id', INTEGER, primary_key=True),
    Column('name', VARCHAR(128))
)
mapper(Ingredient, ingredients, properties={
    'ingredients_recipes': relationship(IngredientRecipe, backref='ingredient')
})


