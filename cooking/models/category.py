from cooking.orm_setup import metadata, db_session, engine
import datetime


class Category(object):
    query = db_session.query_property()

    def __init__(self, name=None, description=None):
        self.id = None
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Category name=%r>' % (self.name)

    @classmethod
    def load_categories(cls, recipe_id):
        attributes = ['name', 'description']
        results = engine.execute("SELECT %s FROM categories_recipes JOIN categories ON categories_recipes.category_name=categories.name WHERE recipe_id=%i ORDER BY name ASC" % (",".join(attributes), long(recipe_id)))
        categories = []
        for result in results:
            category = Category()
            category.name = result[0]
            category.description = result[1]
            categories.append(category)

        return categories

    @classmethod
    def load_unique_categories(cls):
        results = engine.execute("SELECT name, description FROM categories;")
        categories = []
        for result in results:
            categories.append(Category(name=result[0], description=result[1]))
        return categories

    @classmethod
    def insert_category(cls, name):
        d = {'name':name}
        engine.execute("INSERT INTO categories (name) VALUES %(name)s", d)



