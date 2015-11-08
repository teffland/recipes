from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session, engine
from collections import defaultdict
from psycopg2.extensions import adapt

class Rating(object):
    query = db_session.query_property()

    def __init__(self, user_id=None, recipe_id=None, rating=None):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.rating = rating

    def __repr__(self):
        return '<Rating user_id=%i:recipe_id=%i:rating=%i>' % (self.user_id,self.recipe_id,self.rating)

    @classmethod
    def avg_rating_by_recipe(cls, recipe_ids):
        recipe_ids = [adapt(str(rid)).getquoted() for rid in recipe_ids]
        result = engine.execute("SELECT recipe_id, AVG(rating) FROM ratings WHERE recipe_id IN (%s) GROUP BY recipe_id" % (",".join(recipe_ids)))
        ratings = defaultdict(int)
        for result_tuple in result:
            ratings[int(result_tuple[0])] = float(result_tuple[1])
        return ratings

    @classmethod
    def rate(cls, user, recipe_id, rating):
        user_id = long(user.id)
        recipe_id = long(recipe_id)
        results = engine.execute("SELECT COUNT(*) FROM ratings WHERE user_id=%s AND recipe_id=%s", (user_id,recipe_id))
        exists = False
        for result in results:
            if result[0] > 0:
                exists = True

        if exists:
            engine.execute("UPDATE ratings SET rating=%s WHERE user_id=%s AND recipe_id=%s", (int(rating), user_id, recipe_id))
        else:
            engine.execute("INSERT INTO ratings (user_id, recipe_id, rating) VALUES (%s,%s,%s)", (user_id, recipe_id, int(rating)))


ratings = Table('ratings', metadata,
    Column('user_id', BIGINT, ForeignKey('users.id', ondelete="CASCADE")),
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('rating', SmallInteger),
    PrimaryKeyConstraint('user_id', 'recipe_id')
)
mapper(Rating, ratings)
