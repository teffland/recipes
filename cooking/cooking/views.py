
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
from models.categories_recipes import insert_category_recipe
from models.comment import Comment
from timeit import default_timer as timer
from psycopg2.extensions import adapt

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

@app.route('/account/')
def account():
    return '' 

@app.route('/create-recipe/', methods=['GET', 'POST'])
def create_recipe():
    categories = [str(c.name) for c in Category.load_unique_categories()]
    ingredients = [str(i.name.encode('utf-8')) for i in Ingredient.load_unique_ingredients()]
    if request.method == 'POST':
        print request.form.keys()
        f = request.form
        recipe_dict = {'name':f['name'],
                  'servings':f['servings'],
                  'prep':f['preptime'],
                  'photo':f['uploadimg'],
                  'nutri':f['nutrition'],
                  'creator':g.current_user.id
                }
        rid = Recipe.insert_recipe(recipe_dict)      
        c_count = int(f['c-count'])
        for c in range(1,c_count+1):
            cat = f['c'+str(c)]
            if not cat: continue # handle empty fields
            elif cat in categories:
                insert_category_recipe(cat, rid)
            else:
                Category.insert_category(cat)
                insert_category_recipe(cat, rid)

        i_count = int(f['i-count'])
        for i in range(1,i_count+1):
            ing = f['i'+str(i)]
            q = f['q'+str(i)]
            u = f['u'+str(i)]
            d = f['d'+str(i)]
            if not ing: continue
            elif ing in ingredients:
                IngredientRecipe.insert_ingredient_recipe(ing, q,u,d, rid)
            else:
                Ingredient.insert_ingredient(ing)
                IngredientRecipe.insert_ingredient_recipe(ing, q,u,d, rid)

        step_count = int(f['step-count'])
        for s in range(1,step_count+1):
            step = f['step'+str(s)]
            if not step: continue
            else: Step.insert_step(rid, s, step)
        return recipe(recipe_id=rid)
        
    elif request.method == 'GET':
        #print "DIFF: ",set(categories)-set(ingredients)

        return render_template('create_recipe.html', categories=categories, ingredients=ingredients)

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
