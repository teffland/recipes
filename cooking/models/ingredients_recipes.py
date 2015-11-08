from sqlalchemy.types import *
from sqlalchemy import Table, Column, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper
from cooking.orm_setup import metadata, db_session, engine

class IngredientRecipe(object):
    query = db_session.query_property()

    def __init__(self, ingredient_name=None, recipe_id=None, quantity=None, unit=None, comment=None):
        self.ingredient_name = ingredient_name
        self.recipe_id = recipe_id
        self.quantity = quantity
        self.unit = unit
        self.comment = comment

    def __repr__(self):
        return '<IngredientRecipe ingredient_name=%s:recipe_id=%i>' % (self.ingredient_name,self.recipe_id)

    @classmethod
    def load_ingredients(cls, recipe_id):
        attributes = ['name', 'quantity', 'unit', 'comment']
        results = engine.execute("SELECT %s FROM ingredients_recipes a JOIN ingredients b ON a.ingredient=b.name WHERE recipe_id=%s" % (",".join(attributes), '%s'), long(recipe_id))
        ingredients = []
        for result in results:
            ingredient = cls()
            ingredient.name = result[0]
            ingredient.quantity = result[1]
            ingredient.unit = result[2]
            ingredient.comment = result[3]
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
    Column('id', BIGINT, primary_key=True),
    Column('ingredient', VARCHAR(128), ForeignKey('ingredients.name', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('quantity', VARCHAR(32)),
    Column('unit', VARCHAR(32)),
    Column('comment', VARCHAR(128))
)
mapper(IngredientRecipe, ingredients_recipes)