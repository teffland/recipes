from sqlalchemy.types import *
from sqlalchemy import Table, Column, PrimaryKeyConstraint, ForeignKey
from cooking.orm_setup import metadata

categories_recipes = Table('categories_recipes', metadata,
    Column('category_name', BIGINT, ForeignKey('categories.name', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    PrimaryKeyConstraint('category_name', 'recipe_id')
)