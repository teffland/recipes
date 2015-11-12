from cooking.orm_setup import metadata, db_session, engine
import datetime
from models.base_model import BaseModel
from cooking.config import Config
import models.user
from models.step import Step
from models.rating import Rating
from models.saved import Saved
from models.category import Category
from models.ingredients_recipes import IngredientRecipe
from models.comment import Comment
from models.photo import Photo
import math
from psycopg2.extensions import adapt

from hashlib import sha384
import urllib
def download_photo(url):
    try:
        photo_hash = sha384(url).digest().encode('base64')[0:-1]
        #print photo_hash.replace
        localname = photo_hash.replace('/', '-')+".jpg"
        print localname
        urllib.urlretrieve(url, Config.PHOTO_DIR+localname)
        return localname
    except:
    #    print "\t NO PHOTO"
        return "default.jpg"

class Recipe(object):
    query = db_session.query_property()

    def __init__(self, name=None, servings=None, preparation_time=None, nutritional_info=None, photo_file='default.jpg', creator_id=None):
        self.name = name
        self.servings = servings
        self.preparation_time = preparation_time
        self.nutritional_info = nutritional_info
        self.photo_file = photo_file
        self.creator_id = creator_id


    def __repr__(self):
        return '<Recipe id=%s:name=%r>' % (self.id,self.name)

    @classmethod
    def load_recipes(cls, current_user, limit=8, page=1, order_by='created_at DESC', join=[], where=[]):
        attributes = ['id','name','servings','preparation_time','photo_file','created_at','creator_id']
        if page == 1:
            offset = ''
        else:
            offset = 'OFFSET %s' % adapt(str(limit * (page-1))).getquoted()[1:-1]

        join_sql = ''
        if len(join) > 0:
            join_list = []
            for join_desc in join:
                if join_desc == 'avg_ratings':
                    join_list.append("LEFT OUTER JOIN (SELECT recipe_id, AVG(rating) AS avg_rating FROM ratings GROUP BY recipe_id) AS avg_ratings ON recipes.id=avg_ratings.recipe_id")
                if join_desc == 'saved':
                    join_list.append("INNER JOIN saved ON recipes.id=saved.recipe_id AND saved.user_id=%s" % adapt(str(current_user.id)).getquoted())
            join_sql = ' '.join(join_list)

        where_array = where
        where_sql = ''
        if len(where_array) > 0:
            where_sql += ("WHERE " + (" AND ".join(where_array)))

        result = engine.execute("SELECT %s FROM recipes %s %s ORDER BY %s LIMIT %s %s" % 
            (",".join(attributes), join_sql, where_sql, order_by, adapt(str(limit)).getquoted(), offset))
        
        dicts = []
        for values in result:
            attrs = {attributes[i]:value for i, value in enumerate(values) }
            dicts.append(attrs)

        recipes = cls.create_from_dicts(dicts)
        page_count = 1
        recipe_count = 0

        if len(recipes) > 0:
            # get total recipe count
            result = engine.execute("SELECT COUNT(*) FROM recipes %s %s" % (join_sql, where_sql))
            recipe_count = None
            for result_tuple in result:
                recipe_count = result_tuple[0]
            page_count = int(math.ceil(float(recipe_count) / limit))
            if page_count == 0:
                page_count = 1 

            # get avg ratings
            recipe_ids = [str(recipe.id) for recipe in recipes]
            ratings = Rating.avg_rating_by_recipe(recipe_ids)

            # get favorited
            favorites = Saved.favorites(recipe_ids, current_user.id)

            # inject things on recipes
            for recipe in recipes:
                recipe.avg_rating = ratings[recipe.id]
                recipe.round_rating = round(recipe.avg_rating)
                recipe.is_user_favorite = (recipe.id in favorites)

        return recipes, page_count, recipe_count

    @classmethod
    def create_from_dicts(cls, dicts):
        recipes = []
        for attrs in dicts:
            obj = cls()
            for attr, val in attrs.items():
                setattr(obj,attr,val)
            recipes.append(obj)

        return recipes

    @classmethod
    def load_recipe(cls, recipe_id, current_user):
        attributes = ['id','name','servings','preparation_time','photo_file','created_at','creator_id','nutritional_info',
            'avg_ratings.avg_rating', 'my_ratings.rating', 'saved_counts.saved_count', 'saved.saved_at', 'avg_ratings.rating_count']

        join_list = []
        join_list.append("LEFT OUTER JOIN (SELECT recipe_id, AVG(rating) AS avg_rating, COUNT(rating) AS rating_count FROM ratings GROUP BY recipe_id) AS avg_ratings ON recipes.id=avg_ratings.recipe_id")
        join_list.append("LEFT OUTER JOIN ratings AS my_ratings ON recipes.id=my_ratings.recipe_id AND my_ratings.user_id=%s" % adapt(str(current_user.id)).getquoted())
        join_list.append("LEFT OUTER JOIN (SELECT recipe_id, COUNT(user_id) AS saved_count FROM saved GROUP BY recipe_id) AS saved_counts ON recipes.id=saved_counts.recipe_id")
        join_list.append("LEFT OUTER JOIN saved ON recipes.id=saved.recipe_id AND saved.user_id=%s" % adapt(str(current_user.id)).getquoted())
        join_sql = ' '.join(join_list)

        where_sql = "WHERE recipes.id=%s" % adapt(str(recipe_id)).getquoted()

        results = engine.execute("SELECT %s FROM recipes %s %s" % (",".join(attributes), join_sql, where_sql))

        recipe = None
        for result in results:
            recipe = Recipe()
            recipe.id = result[0]; recipe.name = result[1]; recipe.servings = result[2]; recipe.preparation_time = result[3];
            recipe.photo_file = result[4]; recipe.created_at = result[5]; recipe.creator_id = result[6]; 
            recipe.nutritional_info = result[7]; recipe.avg_rating = result[8]; recipe.rating = result[9]; 
            recipe.favorite_count = result[10]; recipe.is_favorite = (result[11] != None); recipe.rating_count = result[12];

            if not recipe.favorite_count:
                recipe.favorite_count = 0

            if not recipe.rating_count:
                recipe.rating_count = 0
            
            if not recipe.avg_rating:
                recipe.avg_rating = 0.0
            else:
                recipe.avg_rating = round(recipe.avg_rating,1)

            user = models.user.User.load_user_by_id(recipe.creator_id)
            recipe.creator = user

            recipe.steps = Step.load_steps(recipe.id)
            recipe.ingredients_recipes = IngredientRecipe.load_ingredients(recipe.id)
            recipe.categories = Category.load_categories(recipe.id)
            recipe.category_count = len(recipe.categories)
            recipe.comments = Comment.load_comments(recipe.id)

        return recipe

    def valid(self):
        errors = []

        if not self.name:
            errors.append('recipe name cannot be blank')
        if len(self.name) > 128:
            errors.append('recipe name is too long')
        if len(self.servings) > 128:
            errors.append('servings text is too long')
        if len(self.preparation_time) > 128:
            errors.append('preparation time text is too long')
        
        if self.upload_file.filename and not Photo.allowed_file(self.upload_file):
            errors.append('image must be .png .jpg or .jpeg')

        for category_name in self.category_names:
            if not category_name:
                errors.append('all category names should be set')
            if len(category_name) > 128:
                errors.append('category name is too long')

        for ingredient in self.ingredients:
            if len(ingredient.name) == 0:
                errors.append('ingredient name cannot be blank')
            elif len(ingredient.name) > 128:
                errors.append('ingredient name is too long')
            if len(ingredient.quantity) > 128:
                errors.append('ingredient quantity is too long')
            if len(ingredient.unit) > 128:
                errors.append('ingredient unit is too long')
            if len(ingredient.comment) > 128:
                errors.append('ingredient comment is too long')

        if len(self.ingredients) == 0:
            errors.append('must have at least one ingredient')

        for step in self.steps:
            if len(step.instructions) == 0:
                errors.append('instructions cannot be blank')
            elif len(step.instructions) > 500:
                errors.append('instructions of a single step are too long')

        if len(self.steps) == 0:
            errors.append('must have at least one instruction step')

        errors = list(set(errors))
        if len(errors) > 0:
            self.error_message = ', '.join(errors)
        else:
            self.error_message = ''

        return (len(errors) == 0)

    def save(self, existing_categories, existing_ingredients):
        connection = engine.connect()
        transaction = connection.begin()
        try:
            # upload photo
            if not self.upload_file.filename:
                self.photo_file = Photo.DEFAULT_IMAGE
            else:
                self.photo_file = Photo.upload_photo(self.upload_file)

            connection.execute("""
                INSERT INTO recipes (name, servings, preparation_time, nutritional_info, photo_file, creator_id, created_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s)""", 
                (self.name,
                self.servings,
                self.preparation_time,
                self.nutritional_info,
                self.photo_file,
                self.creator_id,
                BaseModel.timestamp_to_db(datetime.datetime.now())
                ))

            # get recipe_id
            results = connection.execute("SELECT id FROM recipes ORDER BY id DESC LIMIT 1;")
            recipe_id = None
            for result in results:
                recipe_id = result[0]
            
            # create categories
            for category_name in self.category_names:
                if category_name not in existing_categories:
                    connection.execute("INSERT INTO categories (name) VALUES (%s)", category_name)
                connection.execute("INSERT INTO categories_recipes (recipe_id, category_name) VALUES (%s,%s)", (recipe_id, category_name))

            # create ingredients
            for ingredient in self.ingredients:
                if ingredient.name not in existing_ingredients:
                    connection.execute("INSERT INTO ingredients (name) VALUES (%s)", ingredient.name)
                connection.execute("""
                    INSERT INTO ingredients_recipes (ingredient_name, recipe_id, quantity, unit, comment)
                    VALUES (%s,%s,%s,%s,%s)""", (ingredient.name, recipe_id, ingredient.quantity, ingredient.unit, ingredient.comment))

            # create steps
            for step in self.steps:
                connection.execute("""
                    INSERT INTO steps (recipe_id, number, instructions)
                    VALUES (%s,%s,%s)""", (recipe_id, step.number, step.instructions))

            transaction.commit()
        except Exception as e:
            transaction.rollback()
            self.error_message = e.message
            return False

        return True




