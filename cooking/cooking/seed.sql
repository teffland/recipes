INSERT INTO 
    users (email, first_name, last_name, hashed_password, icon_code, created_at, last_login_at) 
VALUES
    ('abc@abc.com', 'Abc', 'Xyz', 'GrYOEQ1BqarF4w0IbEkIGb/jRhs4x2uWAv6WhqoKo9KMY8lqEBnjeIxAoU9CkuUP', 0, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
    ('frank@whitehouse.fake', 'Franklin', 'Roosevelt', '36f104ac393b8431b57e78670c350359059f5bac353ef3ce620ee7c8ccf38928', 1, '2015-10-09 12:00:00', '2015-10-09 12:00:00'),
    ('george@whitehouse.fake', 'George', 'Washington', '1bd918318467b5edf3243b90633427d2facaf630747d2d33bce137638a8719d4', 2, '2015-10-10 12:00:00', '2015-10-10 12:00:00'),
    ('bush@whitehouse.fake', 'George', 'Bush', '1bd918318467b5edf3243b90633427d2facaf630747d2d33bce137638a8719d4', 0, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
    ('bill@whitehouse.fake', 'Bill', 'Clinton', '237cef09c18de58503d79d9dd966c73c9736a8a9b8def484ba08f4d97bd2d3aa', 1, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
    ('teo@whitehouse.fake', 'Theodore', 'Roosevelt', 'a8979eec0be4e79b40e969c701e012c56dc3dbec3ba63611e597f605fe26eac8', 2, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
    ('rick@whitehouse.fake', 'Richard', 'Nixon', '5f872912d9b2b6f312711902991ac83fd854c746a8922e36715ff3aff18574b1', 3, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
    ('tom@whitehouse.fake', 'Thomas', 'Jefferson', '62660e10f69dcf92334c3bcae6330673947c2863982a9e8af92f141ad9587ce2', 0, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
    ('john@whitehouse.fake', 'John', 'Kennedy', '9c4b7a6b4af91b44be8d9bb66d41e82589f01974702d3bf1d9b4407a55593c3c', 1, '2015-10-08 12:00:00', '2015-10-08 12:00:00'),
    ('harry@whitehouse.fake', 'Harry', 'Truman', '79ff9c4d2fe456cc3015d157cf941fa51a4b2c51629d73b057629cdbb9801416', 2, '2015-10-08 12:00:00', '2015-10-08 12:00:00');

INSERT INTO 
    categories (id, name, description)
VALUES
    (1, 'Mexican', 'Corn, chilli and beans, the best that''s ever beans.'),
    (2, 'Burger', 'The most traditional sandwich of them all.'),
    (3, 'Microwave treats', 'Things you can do easily at home with your microwave.'),
    (4, 'Veggie', 'No meat for you today.'),
    (5, 'Noodles', NULL),
    (6, 'Pizza', 'The most famous italian treat!'),
    (7, 'Dessert', 'Sweet!'),
    (8, 'Salad', 'What you eat when there''s no meat.'),
    (9, 'Japanese', 'Sushi for all.'),
    (10, 'Appetizers', NULL);

INSERT INTO 
    ingredients (id, name)
VALUES
    (1, 'Haas avocato'),
    (2, 'lime'),
    (3, 'salt'),
    (4, 'onion'),
    (5, 'Roma tomato'),
    (6, 'ground beef'),
    (7, 'american cheese'),
    (8, 'burger bun'),
    (9, 'soy protein'),
    (10, 'egg'),
    (11, 'salmon'),
    (12, 'condensed milk'),
    (13, 'cocoa powder'),
    (14, 'cream'),
    (15, 'strawberry quik');

INSERT INTO 
    recipes (id, name, servings, preparation_time, nutritional_info, photo_path, creator_id, created_at)
VALUES 
    (1, 'Guacamole', '1 batch', '1h20m', NULL, '/fakepath/guacaphoto.png', 1, '2015-10-08 12:00:00'),
    (2, 'Cheeseburger', '1 burger', '20m', NULL, '/fakepath/chezburgerphoto.png', 2, '2015-10-08 12:00:00'),
    (3, 'Burger', '1 burger', '20m', NULL, '/fakepath/burgerphoto.png', 2, '2015-10-08 12:00:00'),
    (4, 'Veggie Burger', '1 burger', '20m', NULL, '/fakepath/turkburgerphoto.png', 2, '2015-10-08 12:00:00'),
    (5, 'Microwave Egg', '1 egg serving', '5m', NULL, '/fakepath/eggphoto.png', 3, '2015-10-08 12:00:00'),
    (6, 'Microwave Tomato', '1 tomato serving', '12m', NULL, '/fakepath/tomatophoto.png', 3, '2015-10-08 12:00:00'),
    (7, 'Microwave Onion', '1 onion serving', '12m', NULL, '/fakepath/onionphoto.png', 3, '2015-10-08 12:00:00'),
    (8, 'Sashimi', '1 serving', '10m', NULL, '/fakepath/sashimiphoto.png', 1, '2015-10-08 12:00:00'),
    (9, 'Brigadeiro', '6 servings', '30m', NULL, '/fakepath/brigadeirophoto.png', 4, '2015-10-08 12:00:00'),
    (10, 'Fake Strawberry Mousse', '4 servings', '5m', NULL, '/fakepath/fsmphoto.png', 4, '2015-10-08 12:00:00');

UPDATE recipes SET nutritional_info='Nutritional analysis per serving: 201 calories; 9 grams fat; 1 gram saturated fat; 6 grams monounsaturated fat; 1 gram polyunsaturated fat; 27 grams carbohydrates; 3 grams dietary fiber; 1 gram sugars; 3 grams protein; 9 milligrams sodium';

INSERT INTO 
    categories_recipes (recipe_id, category_id)
VALUES
    (1,1), (1,4),
    (2,2),
    (3,2),
    (4,2), (4,4),
    (5,3),
    (6,3), (6,4),
    (7,3), (7,4),
    (8,9),
    (9,3), (9,7),
    (10,7);


INSERT INTO 
    ingredients_recipes (recipe_id, ingredient_id, quantity, unit, comment)
VALUES
    (1,1,'3',NULL,'halved, seeded and peeled'), (1,2,'1',NULL,'juiced'), (1,3,'1/2','teaspoon',NULL), (1,4,'1','medium',NULL),(1,5,'2',NULL,'seeded and diced'),
    (2,6,'6','ounces','chuck'), (2,3,'1','pinch',NULL), (2,7,'2','slices',NULL), (2,8,'1',NULL,NULL),
    (3,6,'6','ounces','chuck'), (3,3,'1','pinch',NULL), (3,8,'1',NULL,NULL),
    (4,9,'6','ounces',NULL), (4,3,'1','pinch',NULL), (4,8,'1',NULL,NULL),
    (5,10,'1',NULL,NULL), (5,3,'1','pinch',NULL),
    (6,5,'1',NULL,NULL), (6,3,'1','pinch',NULL),
    (7,4,'1',NULL,NULL), (7,3,'1','pinch',NULL),
    (8,11,'12','ounces','raw, unfilleted and skinned'),
    (9,12,'1','can',NULL), (9,13,'3','full spoons',NULL),
    (10,14,'1','pound',NULL), (10,15,'6','full spoons',NULL);


INSERT INTO 
    steps (recipe_id, number, title, instructions)
VALUES
    (1, 1, 'Mix everything', 'In a large bowl place the scooped avocado pulp and lime juice, toss to coat. Drain, and reserve the lime juice, after all of the avocados have been coated. Using a potato masher add the salt, cumin, and cayenne and mash. Then, fold in the onions, jalapeno, tomatoes, cilantro, and garlic. Add 1 tablespoon of the reserved lime juice. Let sit at room temperature for 1 hour and then serve.'),
    (2,1, 'Prepare the patties', 'Lightly mix 6 ounces ground beef chuck with a big pinch of kosher salt. Form into two equal balls, and then shape into two flat patties. Lay two slices American cheese between them and form the meat around the cheese; make an indentation in the center of the patty.'), (2,2, 'Cook the patties', 'Heat a cast-iron skillet over medium-high heat; sprinkle the skillet with salt. Cook the burger 4 to 5 minutes per side.'), (2,3, 'Serve', 'Serve on a soft bun.'),
    (3,1, 'Prepare the patties', 'Lightly mix 6 ounces ground beef chuck with a big pinch of kosher salt. Form into two equal balls, and then shape into two flat patties.'), (3,2, 'Cook the patties', 'Heat a cast-iron skillet over medium-high heat; sprinkle the skillet with salt. Cook the burger 4 to 5 minutes per side.'), (3,3, 'Serve', 'Serve on a soft bun.'),
    (4,1, 'Prepare the patties', 'Lightly mix 6 ounces soy protein with a big pinch of kosher salt. Form into two equal balls, and then shape into two flat patties.'), (4,2, 'Cook the patties', 'Heat a cast-iron skillet over medium-high heat; sprinkle the skillet with salt. Cook the burger 4 to 5 minutes per side.'), (4,3, 'Serve', 'Serve on a soft bun.'),
    (5,1, 'Break the egg', 'Break the egg in a small deep contained. Burst the yolk and drop the pinch of salt.'), (5,2, 'Cook', 'Put the container in the microwave with medium power for 2 minutes'),
    (6,1, 'Prepare', 'Cut the tomato in half and put it in a plate. Pour salt over the two halves.'), (6,2, 'Cook', 'Put the plate into the microwave with medium power for 10 minutes'),
    (7,1, 'Prepare', 'Cut the onion in half and put it in a plate. Pour salt over the two halves.'), (7,2, 'Cook', 'Put the plate into the microwave with medium power for 10 minutes'),
    (8,1, 'Clean', 'Clean the salmon with tap water and then leave it to rest in water for 15 minutes'), (8,2, 'Cut', 'Cut the salmon in thick 1 inch fillets and then cut those fillets again in the other direction to get small pieces of raw salmon'), (8,3, 'Put it in a plate', 'Put the small pieces interleaved in a plate and eat.'),
    (9,1, 'Mix ingredients', 'Pour the condensed milk in a large bowl. Add the 3 spoons of cocoa, one at a time, and mix it until it is practically dissolved.'), (9,2, 'Cook', 'Put the bowl in the microwave oven and cook for 12 minutes with low power. Remove the bowl and mix again the ingredients. Cook 12 more minutes with the same settings and done!'),
    (10,1, 'Mix ingredients', 'Pour the cream in a bowl. Add the 6 spoons of strawberry quik, one at a time, and mix it until it is dissolved.'), (10,2, 'Refrigerate', 'Put the bowl in fridge and wait until you are hungry.');


INSERT INTO 
    ratings (user_id, recipe_id, rating)
VALUES
    (1,1,5), (1,2,3), (1,3,5), (1,4,4),
    (2,5,1), 
    (3,5,4),
    (4,2,1),
    (5,8,5), (5,10,5),
    (6,6,1);

INSERT INTO 
    saved (user_id, recipe_id, saved_at)
VALUES
    (1,1,'2015-10-08 14:43:23'), (1,3,'2015-10-08 14:41:21'), (1,4,'2015-10-08 15:13:02'),
    (3,5,'2015-10-09 07:32:47'),
    (5,8,'2015-10-08 14:43:23'), (5,10,'2015-10-09 15:43:23'),
    (7,1,'2015-10-10 22:05:55'), (7,3,'2015-10-10 22:10:55'), (7,9,'2015-10-10 22:15:55'), (7,10,'2015-10-10 22:18:55');

INSERT INTO 
    comments (user_id, recipe_id, text, created_at, updated_at)
VALUES
    (1,1,'This guacamole is great! I created the recipe =D', '2015-10-10 22:10:55', '2015-10-10 22:10:55'),
    (2,1,'This guacamole horrible! You should be ashamed of yourself', '2015-10-10 23:10:55', '2015-10-10 23:10:55'),
    (3,1,'As a mexican descendent I agree with the last comment', '2015-10-11 23:10:55', '2015-10-11 23:10:55'),
    (1,1,'That is because you can''t follow instructions', '2015-10-12 22:10:55', '2015-10-12 22:10:55'),
    (4,1,'Keep it classy fellow presidents...', '2015-10-13 21:11:55', '2015-10-13 22:11:55'),
    (1,3,'I like big burgers and I cannot lie', '2015-10-10 21:13:55', '2015-10-11 22:13:55'),
    (1,4,'And I don''t like veggie burgers, it should not be called a burger', '2015-10-10 21:12:55', '2015-10-10 22:12:55'),
    (8,4,'+1', '2015-10-10 21:12:55', '2015-10-10 22:12:55'),
    (9,4,'up', '2015-10-10 21:12:55', '2015-10-10 22:12:55'),
    (10,4,'uuuuuup', '2015-10-10 21:12:55', '2015-10-10 22:12:55');
