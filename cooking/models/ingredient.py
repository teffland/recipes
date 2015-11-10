from sqlalchemy.types import *
from sqlalchemy import Table, Column
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session, engine
import datetime
from models.ingredients_recipes import IngredientRecipe
from collections import defaultdict


class Ingredient(object):
    query = db_session.query_property()

    def __init__(self, name=None):
        self.id = None
        self.name = name

    def __repr__(self):
        return '<Ingredient name=%r>' % (self.name)


    @classmethod
    def load_unique_ingredients(cls):
        results = engine.execute("SELECT name FROM ingredients;")
        ingredients = []
        for result in results:
            ingredients.append(Ingredient(name=result[0]))
        return ingredients
   
    @classmethod
    def insert_ingredient(cls, name):
        d = {'name':name}
        engine.execute("INSERT INTO ingredients (name) VALUES %(name)s", d)

ingredients = Table('ingredients', metadata,
    Column('name', VARCHAR(128), primary_key=True)
)
mapper(Ingredient, ingredients, properties={
    'ingredients_recipes': relationship(IngredientRecipe, backref='ingredient_obj')
})


