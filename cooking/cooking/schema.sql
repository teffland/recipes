

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
    id              bigserial PRIMARY KEY ,
    email           varchar(128) NOT NULL UNIQUE,
    first_name      varchar(128) NOT NULL,
    last_name       varchar(128) NOT NULL,
    hashed_password varchar(128) NOT NULL,
    icon_code       smallint NOT NULL DEFAULT 0,
    created_at      timestamp NOT NULL,
    last_login_at   timestamp NOT NULL
);

CREATE TABLE recipes (
    id                  bigserial PRIMARY KEY,
    name                varchar(128) NOT NULL,
    servings            varchar(32),
    preparation_time    varchar(32),
    nutritional_info    text,
    photo_path          text NOT NULL,
    creator_id          bigint NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at          timestamp NOT NULL
);

CREATE TABLE ratings (
    user_id             bigint REFERENCES users(id) ON DELETE CASCADE,
    recipe_id           bigint REFERENCES recipes(id) ON DELETE CASCADE,
    rating              smallint NOT NULL CHECK (rating IN (1,2,3,4,5)),
    PRIMARY KEY (user_id, recipe_id)
);

CREATE TABLE saved (
    user_id             bigint REFERENCES users(id) ON DELETE CASCADE,
    recipe_id           bigint REFERENCES recipes(id) ON DELETE CASCADE,
    saved_at            timestamp NOT NULL,
    PRIMARY KEY (user_id, recipe_id)
);

CREATE TABLE categories (
    id                  bigserial PRIMARY KEY,
    name                varchar(128) NOT NULL,
    description         text
);

CREATE TABLE categories_recipes (
    recipe_id           bigint REFERENCES recipes(id) ON DELETE CASCADE,
    category_id         bigint REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (recipe_id, category_id)
);

CREATE TABLE ingredients (
    id                  bigserial PRIMARY KEY,
    name                varchar(128) NOT NULL
);

CREATE TABLE ingredients_recipes (
    ingredient_id       bigint REFERENCES ingredients(id) ON DELETE CASCADE,
    recipe_id           bigint REFERENCES recipes(id) ON DELETE CASCADE,
    quantity            varchar(32),
    unit                varchar(32),
    comment             varchar(128),
    PRIMARY KEY (ingredient_id, recipe_id)
);

CREATE TABLE steps (
    recipe_id           bigint REFERENCES recipes(id) ON DELETE CASCADE,
    number              smallint NOT NULL CHECK(number > 0),
    title               varchar(128) NOT NULL,
    instructions        text NOT NULL,
    PRIMARY KEY (recipe_id, number)  
);

CREATE TABLE comments (
    id                  bigserial PRIMARY KEY,
    user_id             bigint REFERENCES users(id) ON DELETE CASCADE,
    recipe_id           bigint REFERENCES recipes(id) ON DELETE CASCADE,
    text                text NOT NULL,
    created_at          timestamp NOT NULL,
    updated_at          timestamp NOT NULL  
);