from cooking.orm_setup import metadata, db_session, engine
import datetime
import hashlib
from models.recipe import Recipe
from models.rating import Rating
from models.saved import Saved
from models.comment import Comment


class User(object):
    query = db_session.query_property()

    def __init__(self, email=None, first_name=None, last_name=None, icon_code=0, password=None):
        self.id = None
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.icon_code = icon_code
        self.created_at = None
        self.last_login_at = None
        self.hashed_password = User.hash_password(password)

    @classmethod
    def hash_password(cls, password):
        if password:
            sha = hashlib.sha384()
            sha.update(password)
            return sha.digest().encode('base64')[0:-1]
        else:
            return None

    @classmethod
    def load_user(cls, email):
        attributes = ['id','email','first_name','last_name','icon_code','created_at','last_login_at','hashed_password']
        result = engine.execute("SELECT %s FROM users WHERE email=%s;" % (",".join(attributes), '%s'), email)
        
        attrs = None
        for values in result:
            attrs = {attributes[i]:value for i, value in enumerate(values) }
        
        if not attrs:
            return None

        user = cls.create_from_dict(attrs)
        return user

    @classmethod
    def load_user_by_id(cls, id):
        attributes = ['id','email','first_name','last_name','icon_code','created_at','last_login_at','hashed_password']
        result = engine.execute("SELECT %s FROM users WHERE id=%s;" % (",".join(attributes), '%s'), id)
        
        attrs = None
        for values in result:
            attrs = {attributes[i]:value for i, value in enumerate(values) }
        
        if not attrs:
            return None

        user = cls.create_from_dict(attrs)
        return user

    @classmethod
    def check_if_authentic(cls, email, password):
        result = engine.execute("SELECT email FROM users WHERE email=%s \
            AND hashed_password=%s;", (email, cls.hash_password(password)))
        return ([email[0] for email in result] + [None])[0]

    @classmethod
    def create_from_dict(cls, attrs):
        obj = cls()
        for attr, val in attrs.items():
            setattr(obj,attr,val)
        return obj

    @classmethod
    def update(cls, user_id, attrs):
        if 'hashed_password' in attrs:
            engine.execute("UPDATE users SET first_name=%s, last_name=%s, hashed_password=%s WHERE id=%s", 
                (attrs['first_name'], attrs['last_name'], attrs['hashed_password'], user_id))
        else:
            engine.execute("UPDATE users SET first_name=%s, last_name=%s WHERE id=%s", 
                (attrs['first_name'], attrs['last_name'], user_id))

    def name(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return '<User id=%s:email=%r>' % (self.id,self.email)



