# ORM stants for object relational mapping
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from cooking import app

database_url = 'postgresql://%s:%s@localhost:5432/%s' % (app.config['DB_USER'], app.config['DB_PASSWORD'],app.config['DATABASE'])
engine = create_engine(database_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
metadata = MetaData()

# not necessary. We are creating the tables on our own
# def init_orm():
#     metadata.create_all(bind=engine)