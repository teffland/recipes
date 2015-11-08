# Question:
I noticed you were using ```sha384("password").digest().encode('base64')[0:-1]``` for password hashing
Why not just use ```sha384("password").hexdigest()``` ?
# Todo List
- []Sanizize SQL queries
- []Create the account page (with the option to edit password)
- []Add comments to the recipe pages
- []Create recipe page
- [X]Load the data 
- [X]Store recipe images

# Cooking Web App

Flask web app of the recipe sharing website, being developed as Project 1 for the Databases class at Columbia.

## Environment Setup Instructions (Linux)

1. Install git
`sudo apt-get install git`

2. Clone repo and enter app dir
  ```
  git clone git@github.com:teffland/recipes.git
  cd recipes/cooking
  ```

3. Install python/flask/postgres etc.
  `sudo apt-get install python2.7 python-pip postgresql-9.3 postgresql-client-9.3 postgresql-server-dev-9.3 libpq-dev python-dev sqlite3`

4. Setup virtualenv
  `sudo pip install virtualenv virtualenvwrapper`
  Add this to ~/.bashrc and also issue the command once so you don't have to reopen the terminal
  `source /usr/local/bin/virtualenvwrapper.sh`
  Creat virtualenv and use it
  `mkvirtualenv cooking`
  `workon cooking`

5. Install python libs
  pip install flask psycopg2 sqlalchemy click

6. Setup PostgreSQL
  Set password to db user 'postgres'
  ```
  sudo -u postgres psql postgres
  \password postgres
  \q
  ```
  Create db user with the same name as your linux user
  `sudo -u postgres createuser --interactive $USER`
  
  Open the client in database "postgres" and set a password for your user
  ```
  psql -d postgres
  \password my_user
  \q
  ```

  Create the databases for our application
  `createdb cooking_development`
  `createdb cooking_production`

7. Config application
  Open file `APP_HOME/cooking/config.py` and change you `DB_USER` and `DB_PASSWORD`.
  For your `SECRET_KEY`, open a python shell and type:
  `>> os.urandom(24).encode('hex')`

8. Populate DB
  on the app home folder run:
  `python reset_db.py`

  You can check the status of your database by entering psql and doing some queries:
  `psql -d cooking_development`
  `SELECT * FROM users;`

9. Run the app
  on the app folder run:
  `python runserver.py`

