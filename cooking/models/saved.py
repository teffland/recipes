from cooking.orm_setup import metadata, db_session, engine
import datetime
from models.base_model import BaseModel
from psycopg2.extensions import adapt

class Saved(object):
    query = db_session.query_property()

    def __init__(self, user_id=None, recipe_id=None, saved_at=None):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.saved_at = saved_at

    def __repr__(self):
        return '<Saved user_id=%i:recipe_id=%i>' % (self.user_id,self.recipe_id)

    @classmethod
    def favorites(cls, recipe_ids, user_id):
        recipe_ids = [adapt(str(rid)).getquoted() for rid in recipe_ids]
        result = engine.execute("SELECT recipe_id FROM saved WHERE recipe_id IN (%s) AND user_id=%s" % (",".join(recipe_ids), adapt(str(user_id)).getquoted()))
        favorite_ids = set([ int(rid_tuple[0]) for rid_tuple in result ])
        return favorite_ids

    @classmethod
    def mark_as_favorite(cls, current_user, recipe_id):
        test = BaseModel.timestamp_to_db(datetime.datetime.now())

        engine.execute("INSERT INTO saved (user_id, recipe_id, saved_at) VALUES (%s,%s,%s)", (
            current_user.id,
            long(recipe_id),
            BaseModel.timestamp_to_db(datetime.datetime.now())
        ))

    @classmethod
    def unmark_as_favorite(cls, current_user, recipe_id):
        engine.execute("DELETE FROM saved WHERE user_id=%s AND recipe_id=%s", (
            current_user.id,
            long(recipe_id)
        ))

