import psycopg2
from contextlib import closing
from cooking import app

# function to connect to db
def db_connect():
    try:
        connection = psycopg2.connect("dbname='%s' user='%s' host='localhost' password='%s'" % (app.config['DATABASE'], app.config['DB_USER'], app.config['DB_PASSWORD']))
        return connection
    except:
        print "I am unable to connect to the database"
        return None

def db_init():
    with closing(db_connect()) as db_connection:
        with app.open_resource('schema.sql', mode='r') as f:
            db_connection.cursor().execute(f.read())
        db_connection.commit()
        db_connection.close()

from models.user import User
from models.recipe import Recipe
from models.step import Step
from models.rating import Rating
from models.saved import Saved
from models.category import Category
from models.ingredient import Ingredient
from models.ingredients_recipes import IngredientRecipe
from cooking.orm_setup import db_session

def db_seed():    
    user = User(email='abc@abc.com', first_name='Abc', last_name='Abc', password='qwerty')
    db_session.add(user)
    db_session.commit()

    db_session.bulk_insert_mappings(Category,
        [dict(name="Mexican", description="Mexican style food (don't say!)"), dict(name="Japanese", description="Japanese style food")]
    )
    db_session.commit()
    mexican = Category.query.first()

    db_session.bulk_insert_mappings(Ingredient,
        [dict(name="Mac & Cheese"), dict(name='Milk')]
    )
    db_session.commit()
    ingredients = Ingredient.query.all()
    mac_and_cheese = ingredients[0]
    milk = ingredients[1]

    recipe = Recipe(name='Mac & Cheese', servings='1 person', preparation_time='15 min', photo_path='fakepath')
    recipe.steps.append(Step(number=1,title='Open the box',instructions='Get the box of Mac & cheese you bought and open it. Watch out that opening those boxes can be tricky.'))
    recipe.steps.append(Step(number=2,title='Follow the instructions on the box',instructions="Read whatever is written in the box and follow it. You're welcome."))
    recipe.categories.append(mexican)
    recipe.ingredients_recipes.append(IngredientRecipe(ingredient_id=mac_and_cheese.id, quantity='1', unit='box'))
    recipe.ingredients_recipes.append(IngredientRecipe(ingredient_id=milk.id, quantity='half', unit='pint'))
    user.recipes.append(recipe)
    db_session.add(user)
    db_session.commit()

    rating = Rating()
    rating.recipe = recipe
    rating.user = user
    rating.rating = 5
    db_session.add(rating)
    db_session.commit()

    saved = Saved()
    saved.recipe = recipe
    saved.user = user
    db_session.add(saved)
    db_session.commit()

    comment = Comment(text='I like my recipe.', recipe_id=recipe.id, user_id=user.id)
    db_session.add(comment)
    db_session.commit()


    db_session.close()

def db_seed2():
    with closing(db_connect()) as db_connection:
        with app.open_resource('seed.sql', mode='r') as f:
            db_connection.cursor().execute(f.read())
        db_connection.commit()
        db_connection.close()

