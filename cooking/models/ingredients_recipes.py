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
        attributes = ['ingredient_name', 'quantity', 'unit', 'comment', 'name']
        results = engine.execute("SELECT %s FROM ingredients_recipes a JOIN ingredients b ON a.ingredient_name=b.name WHERE recipe_id=%i" % (",".join(attributes), long(recipe_id)))
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
    
    @classmethod
    def insert_ingredient_recipe(cls, ing, q, u, d, rid):
        data = {'ingredient':ing,
                'quantity':q,
                'unit':u,
                'comment':d,
                'recipe_id':rid
                 }
        engine.execute("""INSERT INTO ingredients_recipes (ingredient_name, recipe_id, quantity, unit, comment)
                           VALUES (%(ingredient)s, %(recipe_id)s, %(quantity)s, %(unit)s, %(comment)s)""", data)

