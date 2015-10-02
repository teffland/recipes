
from flask import *
from cooking import app

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


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/logout/')
def logout():
    return ''    

@app.route('/recipes/')
def recipes():
    return ''    

@app.route('/account/')
def account():
    return ''  