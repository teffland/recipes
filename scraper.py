
# coding: utf-8

# In[188]:

import requests
from bs4 import BeautifulSoup as bs
import json


# In[183]:

def recipe_link_to_dict(link):
    """ Take in the link to a NYTimes Cooking recipe 
        and extract all of the necessary info in dict form
        This includes:
         * name
         * description
         * prep time
         * yield
         * a url for the photo
         * all of the tags (formerly categories)
         * all of the ingredients, broken down into name, quantity, unit, and comment
         * all of the steps: number and instruction text
         NOTE: We do not pull user comments and names because it doesn't come with the original html, it
         s jscript loaded when the user clicks 'show comments'
    """
    soup = bs(requests.get(link).content, 'html.parser')
    recipe = {}
    recipe['name'] = soup.find('h1', class_='recipe-title').text
    recipe['description'] = soup.find('div', class_='topnote').p.text
    recipe['preparation_time'] = soup.find('ul', class_="recipe-time-yield").li.text.replace('Time','').strip()
    recipe['yield'] = soup.find('span', itemprop="recipeYield").text.strip()
    recipe['photo_url'] = soup.find('img', itemprop='image')['src']

    # get all the tags that work
    recipe['tags'] = []
    for a in soup.find('p', class_="special-diets tag-block").contents:
        try:
            recipe['tags'].append({'name': a.text})
        except:
            pass
        
    # get ingredient info
    recipe['ingredients'] = []
    for li in soup.find_all('li', itemprop="recipeIngredient"):
        ingredient = {'quantity': li.find('span', class_='quantity').text}
        name = li.find('span', itemprop='name').text
        ingredient['name'] = name
        # unit is section of phrase BEFORE name, comment is section AFTER
        split = li.find('span', class_='ingredient-name').text.split(name,1) #maxsplit=1
        ingredient['unit'] = split[0]
        ingredient['comment'] = split[1]
        recipe['ingredients'].append(ingredient)
        
    # get the step info
    recipe['steps'] = []
    for i, li in enumerate(soup.find('ol', itemprop='recipeInstructions').contents):
        try:
            recipe['steps'].append({'number':i, 'instructions':li.text})
        except: # some elements aren't li and break on .text
            pass
    
    return recipe


# In[184]:

def write_json(data, fname='recipe_data.json'):
    with open(fname, 'w') as fp:
        json.dump(data, fp)
    


# In[ ]:

root = 'http://cooking.nytimes.com'
num_searches = 20

search_links = [ root+'/search?q=&page='+str(n+1) for n in range(num_searches)]

print "Getting recipe links"
recipe_links = []
for i, link in enumerate(search_links):
    soup = bs(requests.get(link).content, 'html.parser')
    new_recipe_links = [root+link['href'] for link in soup.find_all('a', class_="card-recipe-info")]
    recipe_links += new_recipe_links
print 'Number of recipes links grabbed: %i' % len(recipe_links)

# load each recipe link and convert it to a dict
recipes = []
for i, link in enumerate(recipe_links):
    print "Downloading recipe #%i" % (i+1)
    # it would appear a lot of these pages aren't as well-formed as I thought
    # or (more likely) my code is buggy, but there's plenty of ones that work
    # so just skip them gracefully
    try:
        recipes.append(recipe_link_to_dict(link))
    except (NameError, TypeError, ValueError, AttributeError) as e:
        print "SKIPPED", e
    
print "Finished, %i total recipes successfully downloaded. Now writing out to file" % len(recipes)
write_json(recipes)
print "All Done!"


# In[ ]:



