from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session
import datetime
from models.step import Step, steps
from models.rating import Rating
from models.saved import Saved
from models.categories_recipes import categories_recipes
from models.category import Category
from models.ingredients_recipes import IngredientRecipe
from models.comment import Comment

class Recipe(object):
    query = db_session.query_property()

    def __init__(self, name=None, servings=None, preparation_time=None, nutritional_info=None, photo_path=None, creator_id=None):
        self.name = name
        self.servings = servings
        self.preparation_time = preparation_time
        self.nutritional_info = nutritional_info
        self.photo_path = photo_path
        self.creator_id = creator_id


    def __repr__(self):
        return '<Recipe id=%s:name=%r>' % (self.id,self.name)


def before_insert_listener(mapper, connection, target):
    target.created_at = datetime.datetime.now()
event.listen(Recipe, 'before_insert', before_insert_listener)

recipes = Table('recipes', metadata,
    Column('id', BIGINT, primary_key=True),
    Column('name', VARCHAR(128)),
    Column('servings', VARCHAR(32)),
    Column('preparation_time', VARCHAR(32)),
    Column('nutritional_info', TEXT),
    Column('photo_path', TEXT),
    Column('creator_id', BIGINT, ForeignKey('users.id', ondelete="CASCADE")),
    Column('created_at', TIMESTAMP)
)
mapper(Recipe, recipes, properties={
    'steps' : relationship(Step, backref='recipe', order_by=steps.c.number),
    'ratings': relationship(Rating, backref='recipe'),
    'saves': relationship(Saved, backref='recipe'),
    'categories': relationship(Category, backref='recipes', secondary=categories_recipes),
    'ingredients_recipes': relationship(IngredientRecipe, backref='recipe'),
    'comments': relationship(Comment, backref='recipe')
})

