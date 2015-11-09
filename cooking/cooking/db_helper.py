import psycopg2
from contextlib import closing
from cooking import app
<<<<<<< HEAD
from cooking.config import Config
=======
import random
>>>>>>> 89f222effea5bd89756882277d4ab396c347b54b

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
from cooking.orm_setup import db_session, engine

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

from datetime import datetime, timedelta
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

def get_comments(count=1):
    options = ["Too much hassle.",
               "This thing is a super food!",
               "I cooked this for my kids and they loved it! It's quick and easy, and certainly a recipe you should try out.",
               "Nice, I can't wait to try to cook this.",
               "This recipe requires a little bit of practice, I tried cooking it a few times and still didn't get it right. The good part is that even when it is not perfect it is still yummy!",
               "Anyone knows if this recipe can be done in the microwave oven???",
               "I love easy recipes like that =)",
               "Also, instead of doing step 2 above, try leaving it to rest for 10-15min and then mixing the ingredients. It will become lighter and it will need less cooking time.",
               "Super!!!!!",
               "Anyone want to come over to try? haha",
               "Where can I find those ingredients? (I live in NYC)",
               "Whooaa",
               "This was a nice way to prepare fresh corn. Yummy. On the highest heat on my stove, the corn was golden brown and ready (and beginning to pop all over the place) in 5 minutes. I took it off at that point and served it, and it was perfect. Next time I'll cook it at 3/4 heat for closer to the suggested 10 mins - with the aim of having the corn cooked well but not popping so quickly.",
               "Delicious and very simple. I made with frozen corn. Two of us ate the whole pound of corn.",
               "wow! this was so good! I halved the butter, you honestly don't need a whole stick of butter. I'd add more mint next time.",
               "Certainly simple to make using the freshest ingredients available at the Farmer's Market at this time of year. My husband suggested the pancake could be sweeter. If asked would I make it again in the future, the answer most likely will be \"no,\" but simply because we have so many other breakfast favorites that we prefer.",
               "I used bok choi instead of spinach..cook it a little longe..and enjoy",
               "Did not find green garlic cloves at the farm market but there were scares, which added some tang and texture.",
               "I sort of cooked this. No anchovies or green onions. Substituted a little broccoli and sweet onions. Black olives. But the techniques were the same, and it was delicious and speedy! Next time, I'll do it with green garlic and spring onions from the farmer's market, where I got the spinach.",
               "I love this recipe because it is satisfying without the need for cheese. I've served this twice to toddlers and they love it. I chop everything finely and it practically dissolves into a sauce that they think is great, but don't know what it is, and can't pick \"stuff\" out.",
               "Made my own creme fraiche (milk + buttermilk set out on the counter overnight), but it didn't thicken much. Even still, recipe turned out great!",
              ]
    comments = random.sample(options, count)
    random.shuffle(comments)
    return comments

import json
def db_seed3():
    random.seed(1)

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

    
    # Create other users 
    engine.execute("""
        INSERT INTO 
            users (email, first_name, last_name, hashed_password, icon_code, created_at, last_login_at) 
        VALUES
            ('abc@abc.com', 'Abc', 'Xyz', 'GrYOEQ1BqarF4w0IbEkIGb/jRhs4x2uWAv6WhqoKo9KMY8lqEBnjeIxAoU9CkuUP', 0, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
            ('frank@whitehouse.fake', 'Franklin', 'Roosevelt', '36f104ac393b8431b57e78670c350359059f5bac353ef3ce620ee7c8ccf38928', 1, '2015-10-09 12:00:00', '2015-10-09 12:00:00'),
            ('george@whitehouse.fake', 'George', 'Washington', '1bd918318467b5edf3243b90633427d2facaf630747d2d33bce137638a8719d4', 2, '2015-10-10 12:00:00', '2015-10-10 12:00:00'),
            ('bush@whitehouse.fake', 'George', 'Bush', '1bd918318467b5edf3243b90633427d2facaf630747d2d33bce137638a8719d4', 0, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
            ('bill@whitehouse.fake', 'Bill', 'Clinton', '237cef09c18de58503d79d9dd966c73c9736a8a9b8def484ba08f4d97bd2d3aa', 1, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
            ('teo@whitehouse.fake', 'Theodore', 'Roosevelt', 'a8979eec0be4e79b40e969c701e012c56dc3dbec3ba63611e597f605fe26eac8', 2, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
            ('rick@whitehouse.fake', 'Richard', 'Nixon', '5f872912d9b2b6f312711902991ac83fd854c746a8922e36715ff3aff18574b1', 3, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
            ('tom@whitehouse.fake', 'Thomas', 'Jefferson', '62660e10f69dcf92334c3bcae6330673947c2863982a9e8af92f141ad9587ce2', 0, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
            ('john@whitehouse.fake', 'John', 'Kennedy', '9c4b7a6b4af91b44be8d9bb66d41e82589f01974702d3bf1d9b4407a55593c3c', 1, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
            ('harry@whitehouse.fake', 'Harry', 'Truman', '79ff9c4d2fe456cc3015d157cf941fa51a4b2c51629d73b057629cdbb9801416', 2, '2015-10-08 12:00:00', '2015-10-08 12:00:00');
        """)
    results = engine.execute("SELECT id from users;")
    all_user_ids = [tup[0] for tup in results]

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
    recipe_ids = []
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
        recipe_ids.append(recipe_id[0])
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

    for recipe_id in recipe_ids:
        # for each recipe, use a Bernoulli do define if the recipe should be rated/favorited or not
        if random.uniform(0,10) >= 2:
            # randomly select target expected rating
            target_rating = random.randint(1,5)
            offset = target_rating - 3

            # select how many users are going to rate thsi recipe
            rating_count = random.randint(3,len(all_user_ids))

            # select which users are going to rate this recipe
            rating_user_ids = random.sample(all_user_ids, rating_count)

            # for each user, randomly select and create rating
            for ruid in rating_user_ids:
                rating = random.randint(1,5) + offset
                if rating < 1:
                    rating = 1
                elif rating > 5:
                    rating = 5
                engine.execute("INSERT INTO ratings (user_id, recipe_id, rating) VALUES (%s,%s,%s)", (ruid, recipe_id, int(rating)))

                # each user that rated has 1/3 chance of favoriting the recipe
                if random.randint(1,3) == 1:
                    engine.execute("INSERT INTO saved (user_id, recipe_id, saved_at) VALUES (%s,%s,%s)", (
                        ruid,
                        recipe_id,
                        format_timestamp(datetime.now())
                    ))

            # select how many users are going to comment (max is rating count)
            comment_count = random.randint(1,rating_count)
            comments = get_comments(comment_count)

            # select which users are going to comment in this recipe
            comment_user_ids = random.sample(rating_user_ids, comment_count)

            # for each user, randomly select and create comment
            for i, cuid in enumerate(comment_user_ids):
                engine.execute("INSERT INTO comments (user_id, recipe_id, text, created_at, updated_at) VALUES (%s,%s,%s,%s,%s)", 
                    (cuid, recipe_id, comments[i], 
                        format_timestamp(datetime.now()-timedelta(minutes=(comment_count - i))), 
                        format_timestamp(datetime.now()-timedelta(minutes=(comment_count - i)))
                    ))
    



    print "DONE"
