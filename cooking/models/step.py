from sqlalchemy.types import *
from sqlalchemy import Table, Column, event, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import mapper, relationship, backref
from cooking.orm_setup import metadata, db_session, engine
import datetime

class Step(object):
    query = db_session.query_property()

    def __init__(self, recipe_id=None, number=None, instructions=None):
        self.recipe_id = recipe_id
        self.number = number
        self.instructions = instructions

    def __repr__(self):
        return '<Step recipe_id=%i:number=%i>' % (self.recipe_id,self.number)

    @classmethod
    def load_steps(cls, recipe_id):
        attributes = ['number', 'instructions']
        results = engine.execute("SELECT %s FROM steps WHERE recipe_id=%i ORDER BY number ASC" % (",".join(attributes), long(recipe_id)))
        steps = []
        for result in results:
            step = Step()
            step.number = int(result[0])
            step.instructions = result[1]
            steps.append(step)

        return steps


steps = Table('steps', metadata,
    Column('recipe_id', INTEGER, ForeignKey('recipes.id', ondelete="CASCADE")),
    Column('number', SMALLINT),
    Column('instructions', TEXT),
    PrimaryKeyConstraint('recipe_id', 'number')
)
mapper(Step, steps)

