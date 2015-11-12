
from flask import *
from cooking import app

# Load models
from models.user import User
from models.recipe import Recipe
from models.step import Step
from models.rating import Rating
from models.saved import Saved
from models.category import Category
from models.ingredient import Ingredient
from models.ingredients_recipes import IngredientRecipe
from models.comment import Comment
from timeit import default_timer as timer
from psycopg2.extensions import adapt
from orm_setup import engine

# Manual SQL connection management
# from cooking import db_helper
# @app.before_request
# def before_request():
#     g.db = db_helper.db_connect()

# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()


@app.before_request
def load_user():
    if '/static/' in request.path:
        return

    if request.endpoint  == 'home':
        return

    g.current_user = None

    if 'email' in session:
        g.current_user = User.load_user(session['email'])
        if not g.current_user:
            session.pop('email', None)

    if request.endpoint == 'login' and g.current_user != None:
        flash('You are already logged in.')
        return redirect(url_for('recent_recipes'))

    if request.endpoint != 'login' and g.current_user == None:
        flash('You need to login to access this page.')
        return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = User.check_if_authentic(request.form['email'], request.form['password'])
        if email:
            session['email'] = email
            flash('Logged in successfully.')
            return redirect(url_for('recent_recipes'))
        else:
            error = 'Username or password incorrect.'
            return render_template('login.html', error=error)

    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('email', None)
    flash('Logged out successfully.')
    return redirect(url_for('login'))  

@app.route('/recent_recipes/')
def recent_recipes():
    page = request.args.get('page', default=1, type=int)
    limit = 8
    recipes, page_count, recipe_count = Recipe.load_recipes(g.current_user, page=page, limit=limit)
    return render_template('recipes.html', 
        recipes=recipes, 
        page_count=page_count, 
        page=page,
        current_query_params={})

@app.route('/highest_rated_recipes/')
def highest_rated_recipes():
    page = request.args.get('page', default=1, type=int)
    limit = 8
    recipes, page_count, recipe_count = Recipe.load_recipes(g.current_user, 
        page=page, 
        limit=limit,
        order_by='avg_ratings.avg_rating DESC',
        join=['avg_ratings'],
        where=['avg_ratings.avg_rating IS NOT NULL', 'avg_ratings.avg_rating >=3'])
    return render_template('recipes.html', 
        recipes=recipes, 
        page_count=page_count, 
        page=page,
        current_query_params={})  

@app.route('/search_results/<query>')
def search_results(query=''):
    page = request.args.get('page', default=1, type=int)
    limit = 8
    where_clause = "recipes.name ILIKE '%%%%%s%%%%'" % adapt(str(query.replace('+','%%'))).getquoted()[1:-1]

    start_time = timer()
    recipes, page_count, recipe_count = Recipe.load_recipes(g.current_user, 
        page=page, 
        limit=limit,
        where=[where_clause])
    end_time = timer()

    natural_search_string = ' '.join(query.split('+'))

    return render_template('recipes.html', 
        recipes=recipes, 
        page_count=page_count, 
        page=page,
        current_query_params={'query':query},
        search_string=natural_search_string,
        success="We found %i result%s for '%s' (%.4f seconds)" % (recipe_count, ('s' if recipe_count != 1 else ''), natural_search_string, end_time - start_time))    

@app.route('/favorites/')
def favorites():
    page = request.args.get('page', default=1, type=int)
    limit = 16
    recipes, page_count, recipe_count = Recipe.load_recipes(g.current_user, 
        page=page, 
        limit=limit,
        order_by='saved.saved_at DESC',
        join=['saved'])
    return render_template('recipes.html', 
        recipes=recipes, 
        page_count=page_count, 
        page=page,
        current_query_params={})

@app.route('/recipe/<recipe_id>')
def recipe(recipe_id=None):
    if recipe_id:
        recipe = Recipe.load_recipe(long(recipe_id), g.current_user)
        if recipe:
            return render_template('recipe.html', recipe=recipe)
        else:
            abort(404)
    else:
        abort(404)

@app.route('/account/', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        return render_template('account.html', user=g.current_user) 
    elif request.method == 'POST':
        f = request.form
        attributes = {}
        attributes['first_name'] = f['first_name']
        attributes['last_name'] = f['last_name']

        errors = []
        if len(attributes['first_name']) == 0:
            errors.append('first name cannot be blank')
        elif len(attributes['first_name']) >= 128:
            errors.append('first name is too long')
        if len(attributes['last_name']) == 0:
            errors.append('last name cannot be blank')
        elif len(attributes['last_name']) >= 128:
            errors.append('last name is too long')

        if f['new_password']:
            if f['new_password'] != f['confirm_new_password']:
                errors.append("password confirmation doesn't match")
            else:
                attributes['hashed_password'] = User.hash_password(f['new_password'])

        if len(errors) > 0:
            user = g.current_user
            user.first_name = attributes['first_name']
            user.last_name = attributes['last_name']
            return render_template('account.html', user=user, error='An errors has occured while saving your account: ' + ', '.join(errors)) 
        else:
            User.update(g.current_user.id, attributes)
            flash('Account updated.')
            return redirect(url_for('account'))

def first_lower(s):
    if len(s) == 0:
        return s
    return s[0].lower() + s[1:]

@app.route('/create_recipe/', methods=['GET', 'POST'])
def create_recipe():
    categories = [str(c.name) for c in Category.load_unique_categories()]
    ingredients = [str(i.name.encode('utf-8')) for i in Ingredient.load_unique_ingredients()]

    if request.method == 'GET':
        recipe = Recipe()
        
        # TESTING FORM REFILL
        # recipe.name = 'name'
        # recipe.servings = 'servings'
        # recipe.preparation_time = 'prep_time'
        # recipe.nutritional_info = 'nut_info'
        # recipe.categories_string = 'cat1, cat2'
        # recipe.ingredients = []
        # ingredient = Ingredient()
        # ingredient.name = 'ing1-name'
        # ingredient.quantity = 'ing1-quantity'
        # ingredient.unit = 'ing1-unit'
        # ingredient.comment = 'ing1-comment'
        # recipe.ingredients.append(ingredient)
        # ingredient = Ingredient()
        # ingredient.name = 'ing2-name'
        # ingredient.quantity = 'ing2-quantity'
        # ingredient.unit = 'ing2-unit'
        # ingredient.comment = 'ing2-comment'
        # recipe.ingredients.append(ingredient)
        # recipe.steps = []
        # step = Step()
        # step.number = 1
        # step.instructions = 'inst1'
        # recipe.steps.append(step)
        # step = Step()
        # step.number = 2
        # step.instructions = 'inst2'
        # recipe.steps.append(step)

        return render_template('create_recipe.html', categories=categories, ingredients=ingredients, recipe=recipe)

    elif request.method == 'POST':
        f = request.form

        recipe = Recipe()
        recipe.name = f['recipe_name'].strip()
        recipe.servings = f['recipe_servings'].strip()
        recipe.preparation_time = f['recipe_preparation_time'].strip()
        recipe.nutritional_info = f['recipe_nutritional_info'].strip()
        recipe.creator_id = g.current_user.id

        # file
        recipe.upload_file = request.files['recipe_image']

        recipe.category_names = [cat_name.strip().title()[0:29] for cat_name in f['recipe_categories'].split(',') if cat_name.strip()]
        recipe.categories_string = ', '.join(recipe.category_names)

        recipe.ingredients = []
        ingredient_names = f.getlist('recipe_ingredients[name][]')[0:-1]
        ingredient_quantities = f.getlist('recipe_ingredients[quantity][]')[0:-1]
        ingredient_units = f.getlist('recipe_ingredients[unit][]')[0:-1]
        ingredient_comments = f.getlist('recipe_ingredients[comment][]')[0:-1]
        lengths = [len(ingredient_names), len(ingredient_quantities), len(ingredient_units), len(ingredient_comments)]
        ingredient_count = min(lengths)
        for i in xrange(ingredient_count):
            if ingredient_names[i].strip():
                ingredient = Ingredient()
                ingredient.name = first_lower(ingredient_names[i].strip())
                ingredient.quantity = ingredient_quantities[i].strip()
                ingredient.unit = ingredient_units[i].strip()
                ingredient.comment = ingredient_comments[i].strip()
                recipe.ingredients.append(ingredient)

        recipe.steps = []
        step_descriptions = f.getlist('recipe_steps[]')[0:-1]
        step_number = 1
        for description in step_descriptions:
            if description.strip():
                step = Step()
                step.instructions = description.strip()
                step.number = step_number
                recipe.steps.append(step)
                step_number += 1

        if recipe.valid():
            if recipe.save(categories, ingredients):
                return redirect(url_for('recent_recipes'))
            else:
                return render_template('create_recipe.html', categories=categories, ingredients=ingredients, recipe=recipe, error="An error has occured while saving the recipe: " + recipe.error_message)
        else:
            return render_template('create_recipe.html', categories=categories, ingredients=ingredients, recipe=recipe, error="An error has occured while saving the recipe: " + recipe.error_message)      


@app.route('/favorite/<recipe_id>', methods=['PUT'])
def favorite(recipe_id=None):
    if recipe_id:
        Saved.mark_as_favorite(g.current_user, recipe_id)
    return ''

@app.route('/unfavorite/<recipe_id>', methods=['PUT'])
def unfavorite(recipe_id=None):
    if recipe_id:
        Saved.unmark_as_favorite(g.current_user, recipe_id)
    return ''

@app.route('/rate/<recipe_id>/<rating>', methods=['PUT'])
def rate(recipe_id=None, rating=None):
    if recipe_id != None and rating != None:
        Rating.rate(g.current_user, recipe_id, rating)
    return ''

@app.route('/comment/<recipe_id>', methods=['POST'])
def comment(recipe_id=None):
    if recipe_id != None and 'comment_text' in request.form and len(request.form['comment_text'].strip()) > 0:
        Comment.create_comment(g.current_user, recipe_id, request.form['comment_text'].strip())
        comment = Comment.load_last_comment(recipe_id)
        return render_template('comment.html', comment=comment)
    else:
        return ''

@app.route('/delete_comment/<comment_id>', methods=['DELETE'])
def delete_comment(comment_id=None):
    if comment_id != None:
        Comment.delete_comment(comment_id, g.current_user.id)
    return ''
