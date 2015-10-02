from sqlalchemy.types import *
from sqlalchemy import Table, Column, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper
from cooking.orm_setup import metadata, db_session

class IngredientRecipe(object):
    query = db_session.query_property()

    def __init__(self, ingredient_id=None, recipe_id=None, quantity=None, unit=None, comment=None):
        self.ingredient_id = ingredient_id
        self.recipe_id = recipe_id
        self.quantity = quantity
        self.unit = unit
        self.comment = comment

    def __repr__(self):
        return '<IngredientRecipe ingredient_id=%i:recipe_id=%i>' % (self.ingredient_id,self.recipe_id)

ingredients_recipes = Table('ingredients_recipes', metadata,
    Column('ingredient_id', BIGINT, ForeignKey('ingredients.id', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('quantity', VARCHAR(32)),
    Column('unit', VARCHAR(32)),
    Column('comment', VARCHAR(128)),
    PrimaryKeyConstraint('ingredient_id', 'recipe_id')
)
mapper(IngredientRecipe, ingredients_recipes)