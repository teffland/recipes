from sqlalchemy.types import *
from sqlalchemy import Table, Column, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper
from cooking.orm_setup import metadata, db_session, engine

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

    @classmethod
    def load_ingredients(cls, recipe_id):
        attributes = ['ingredient_id', 'quantity', 'unit', 'comment', 'name']
        results = engine.execute("SELECT %s FROM ingredients_recipes a JOIN ingredients b ON a.ingredient_id=b.id WHERE recipe_id=%i" % (",".join(attributes), long(recipe_id)))
        ingredients = []
        for result in results:
            ingredient = cls()
            ingredient.id = int(result[0])
            ingredient.quantity = result[1]
            ingredient.unit = result[2]
            ingredient.comment = result[3]
            ingredient.name = result[4]
            ingredients.append(ingredient)

        return ingredients

    def description(self):
        output = ''
        if self.quantity:
            output += self.quantity + ' '
        if self.unit:
            output += self.unit + ' '
        output += self.name
        if self.comment:
            output += ', ' + self.comment

        return output

ingredients_recipes = Table('ingredients_recipes', metadata,
    Column('ingredient_id', BIGINT, ForeignKey('ingredients.id', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('quantity', VARCHAR(32)),
    Column('unit', VARCHAR(32)),
    Column('comment', VARCHAR(128)),
    PrimaryKeyConstraint('ingredient_id', 'recipe_id')
)
mapper(IngredientRecipe, ingredients_recipes)