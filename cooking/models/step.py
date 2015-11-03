from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session, engine
import datetime

class Step(object):
    query = db_session.query_property()

    def __init__(self, recipe_id=None, number=None, title=None, instructions=None):
        self.recipe_id = recipe_id
        self.number = number
        self.title = title
        self.instructions = instructions

    def __repr__(self):
        return '<Step recipe_id=%i:number=%i>' % (self.recipe_id,self.number)

    @classmethod
    def load_steps(cls, recipe_id):
        attributes = ['number', 'title', 'instructions']
        results = engine.execute("SELECT %s FROM steps WHERE recipe_id=%i ORDER BY number ASC" % (",".join(attributes), long(recipe_id)))
        steps = []
        for result in results:
            step = Step()
            step.number = int(result[0])
            step.title = result[1]
            step.instructions = result[2]
            steps.append(step)

        return steps


steps = Table('steps', metadata,
    Column('recipe_id', BIGINT, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('number', SmallInteger),
    Column('title', VARCHAR(128)),
    Column('instructions', TEXT),
    PrimaryKeyConstraint('recipe_id', 'number')
)
mapper(Step, steps)

