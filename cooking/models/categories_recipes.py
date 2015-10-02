from sqlalchemy.types import *
from sqlalchemy import Table, Column, PrimaryKeyConstraint, ForeignKey
from cooking.orm_setup import metadata

categories_recipes = Table('categories_recipes', metadata,
    Column('category_id', BIGINT, ForeignKey('categories.id', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    PrimaryKeyConstraint('category_id', 'recipe_id')
)