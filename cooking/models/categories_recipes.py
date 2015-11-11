from sqlalchemy.types import *
from sqlalchemy import Table, Column, PrimaryKeyConstraint, ForeignKey
from cooking.orm_setup import metadata, engine

def insert_category_recipe(catname, recipeid):
    d = {'recipe_id':recipeid, 'category_name':catname}
    engine.execute("""INSERT INTO categories_recipes (recipe_id, category_name)
                           VALUES (%(recipe_id)s, %(category_name)s)""", d)

categories_recipes = Table('categories_recipes', metadata,
    Column('category_name', VARCHAR(128), ForeignKey('categories.name', ondelete="CASCADE")),
    Column('recipe_id', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE")),
    PrimaryKeyConstraint('category_name', 'recipe_id')
)
