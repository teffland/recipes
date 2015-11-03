from flask import Flask

# create our application
app = Flask(__name__)
app.config.from_object('cooking.config.DevelopmentConfig')

# Setup connection through ORM
from cooking.orm_setup import db_session, engine
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


import cooking.views