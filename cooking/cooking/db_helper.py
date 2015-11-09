import psycopg2
from contextlib import closing
from cooking import app
from cooking.config import Config

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

from datetime import datetime
def format_timestamp(date):
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
    return datetime.strftime(date, TIMESTAMP_FORMAT)

from hashlib import sha384
import urllib
def download_photo(url):
    try:
        photo_hash = sha384(url).digest().encode('base64')[0:-1]
        localname = photo_hash+".jpg"
        urllib.urlretrieve(url, Config.PHOTO_DIR+localname)
        return localname
    except:
        print "\t NO PHOTO"
        return "default.jpg"

import numpy as np
def get_random_nutritional_info():
    options = ["Eh it's not too good.",
               "This thing is a super food!",
               "Chances of quadruple bypass after eating this are 50/50...",
               "Pretty average I guess.",
               "Freakin awesome!"
              ]
    choice = int(np.floor(np.random.rand()*len(options)))
    return options[choice] + " (NOTE: This was randomly generated)"

import json
def db_seed3():
    conn = db_connect()
    cur = conn.cursor()
    # create the main user
    user = {
        'email' : "chef@goodfood.com",
        'first_name': "Anthony",
        'last_name': "Bourdain",
        'hashed_password':User.hash_password("ILoveCooking"),
        'icon_code':1,
        'created_at' : format_timestamp(datetime.now()),
        'last_login_at' : format_timestamp(datetime.now())
    }

    cur.execute("""INSERT INTO users (email, first_name, last_name, 
                                       hashed_password, icon_code, created_at, last_login_at)
                VALUES (%(email)s, %(first_name)s, %(last_name)s, %(hashed_password)s, %(icon_code)s, 
                        %(created_at)s, %(last_login_at)s)""", user)
    cur.execute("SELECT id FROM users  WHERE email=%(email)s", {'email':user['email']})
    user_id = cur.fetchone()

    
    print "CHEF ID: ", user_id
    with open('data/recipe_data.json' ,'r') as f:
        data = json.loads(f.read())

    # load all of the ingredients
    print "INSERTING ALL INGREDIENTS"
    unique_ingredients = list(set([i['name'] for d in data for i in d['ingredients']]))
    ingredients = [{'name':i} for i in unique_ingredients]
    cur.executemany("""INSERT INTO ingredients (name) VALUES (%(name)s)""", ingredients)
    
    # load all of the categories
    print "INSERTING ALL CATEGORIES"
    unique_categories = list(set([ t['name'] for d in data for t in d['tags']]))
    categories = [{'name':i} for i in unique_categories]
    cur.executemany("""INSERT INTO categories (name) VALUES (%(name)s)""", categories)

    # for each recipe, load it, get its id, then load its steps, ingredients, and categories
    for r in data:
        recipe = {
            'name':r['name'],
            'servings':r['yield'],
            'preparation_time':r['preparation_time'],
            'photo_file':download_photo(r['photo_url']),
            'nutritional_info':r['description'],#get_random_nutritional_info(),
            'creator_id':user_id,
            'created_at':format_timestamp(datetime.now())
        }
        cur.execute("""INSERT INTO recipes (name, servings, preparation_time, photo_file, nutritional_info, creator_id, created_at)
                       VALUES (%(name)s, %(servings)s, %(preparation_time)s, %(photo_file)s,
                               %(nutritional_info)s, %(creator_id)s, %(created_at)s)""", recipe)
        cur.execute("SELECT id FROM recipes ORDER BY id DESC LIMIT 1;")
        recipe_id = cur.fetchone()
        print "RECIPE NUM: ", recipe_id[0]

        categories = [{'recipe_id':recipe_id, 'category_name':t['name']} for t in r['tags']]
        cur.executemany("""INSERT INTO categories_recipes (recipe_id, category_name)
                           VALUES (%(recipe_id)s, %(category_name)s)""", categories)
        
        steps = [ {'id':recipe_id, 'n':s['number'], 'instructions':s['instructions']} for s in r['steps'] ]
        cur.executemany("""INSERT INTO steps (recipe_id, number, instructions)
                           VALUES (%(id)s, %(n)s, %(instructions)s)""", steps)

        ingredients = [{'name':i['name'], 'id':recipe_id, 'q':i['quantity'], 'u':i['unit'],\
                        'comment':i['comment']} for i in r['ingredients'] ]
        cur.executemany("""INSERT INTO ingredients_recipes (ingredient_name, recipe_id, quantity, unit, comment)
                           VALUES (%(name)s, %(id)s, %(q)s, %(u)s, %(comment)s)""", ingredients)

    conn.commit()
    conn.close()
    print "DONE"
