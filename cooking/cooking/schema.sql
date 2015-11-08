

DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS steps;
DROP TABLE IF EXISTS ingredients_recipes;
DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS categories_recipes;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS saved;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS users;


CREATE TABLE users (
    id              serial PRIMARY KEY ,
    email           varchar(128) NOT NULL UNIQUE,
    first_name      varchar(128) NOT NULL,
    last_name       varchar(128) NOT NULL,
    hashed_password varchar(128) NOT NULL,
    icon_code       smallint NOT NULL DEFAULT 0,
    created_at      timestamp NOT NULL,
    last_login_at   timestamp NOT NULL
);

CREATE TABLE recipes (
    id                  serial PRIMARY KEY,
    name                varchar(128) NOT NULL,
    servings            varchar(128),
    preparation_time    varchar(128),
    nutritional_info    text,
    photo_file          text NOT NULL,
    creator_id          integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at          timestamp NOT NULL
);

CREATE TABLE ratings (
    user_id             integer REFERENCES users(id) ON DELETE CASCADE,
    recipe_id           integer REFERENCES recipes(id) ON DELETE CASCADE,
    rating              smallint NOT NULL CHECK (rating IN (1,2,3,4,5)),
    PRIMARY KEY (user_id, recipe_id)
);

CREATE TABLE saved (
    user_id             integer REFERENCES users(id) ON DELETE CASCADE,
    recipe_id           integer REFERENCES recipes(id) ON DELETE CASCADE,
    saved_at            timestamp NOT NULL,
    PRIMARY KEY (user_id, recipe_id)
);

CREATE TABLE categories (
    name                varchar(128) PRIMARY KEY,
    description         text
);

CREATE TABLE categories_recipes (
    recipe_id           integer REFERENCES recipes(id) ON DELETE CASCADE,
    category_name       varchar(128) REFERENCES categories(name) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, category_name)
);

CREATE TABLE ingredients (
    name                varchar(128) PRIMARY KEY
);

CREATE TABLE ingredients_recipes (
    id                  serial PRIMARY KEY,
    ingredient          varchar(128) REFERENCES ingredients(name) ON DELETE CASCADE,
    recipe_id           integer REFERENCES recipes(id) ON DELETE CASCADE,
    quantity            varchar(256),
    unit                varchar(256),
    comment             varchar(256)
);

CREATE TABLE steps (
    recipe_id           integer REFERENCES recipes(id) ON DELETE CASCADE,
    number              smallint NOT NULL CHECK(number > 0),
    instructions        text NOT NULL,
    PRIMARY KEY (recipe_id, number)  
);

CREATE TABLE comments (
    id                  serial PRIMARY KEY,
    user_id             integer REFERENCES users(id) ON DELETE CASCADE,
    recipe_id           integer REFERENCES recipes(id) ON DELETE CASCADE,
    text                text NOT NULL,
    created_at          timestamp NOT NULL,
    updated_at          timestamp NOT NULL  
);
