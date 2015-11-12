from cooking.orm_setup import metadata, engine

def insert_category_recipe(catname, recipeid):
    d = {'recipe_id':recipeid, 'category_name':catname}
    engine.execute("""INSERT INTO categories_recipes (recipe_id, category_name)
                           VALUES (%(recipe_id)s, %(category_name)s)""", d)

