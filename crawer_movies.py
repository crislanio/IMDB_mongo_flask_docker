from requests import get
from bs4 import BeautifulSoup

from time import sleep
from time import time
from IPython.core.display import clear_output
from random import randint
from warnings import warn
import json

import json
from pymongo import MongoClient
import pymongo

client = MongoClient('mongodb://localhost:27017/') # conecta num cliente do MongoDB rodando na sua máquina
db = client['imdb'] # acessa o banco de dados
collection = db['imdb_oficial'] # acessa a minha coleção dentro desse banco de dados
print("sucesso")


warn("Warning Simulation")
headers = {"Accept-Language": "en-US, en;q=0.5"}

pages = [str(i) for i in range(1,11)]
years_url = [str(i) for i in range(2008,2018)]


# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
durations = []
genders = []
diretors = []
votes = []
gloss_ = []

# Preparing the monitoring of the loop
start_time = time()
requests = 0

dataFilms = {}  
dataFilms['film'] = []  
with open('films.json', 'w+') as outfile:  
    json.dump(dataFilms, outfile)

# For every year in the interval 2008-2018
for year_url in years_url:

    # For every page in the interval 1-11
    for page in pages:

        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url + 
        '&sort=num_votes,desc&page=' + page, headers = headers)

        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 200:
            warn('Number of requests was greater than expected.')  
            break 

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

        # Extract data from individual movie container
        for container in mv_containers:
            # The name
            name = container.h3.a.text
            names.append(name)

            # The year
            year = container.h3.find('span', class_ = 'lister-item-year').text[1:5]
            years.append(year)

            # Duration
            duration = container.find('span', class_ = 'runtime').text[0:3]
            durations.append(int(duration))

            # Diretor
            diretor = container.select_one("p").find_next('p').find_next('p').find_next('a').text 
            diretors.append(diretor)

            # The IMDB rating
            imdb = float(container.strong.text)
            imdb_ratings.append(imdb)
            # Gender
            gender = container.find('span', class_ = 'genre').text
            genders.append(gender)

            # The number of votes
            vote = container.find('span', attrs = {'name':'nv'})['data-value']
            votes.append(int(vote))

            # The number of Gloss
 #           gloss = container.select_one("span").find_next('span').find_next('span').find('span', attrs = {'name':'nv'})['data-value']
 #           gloss_.append(int(gloss))



            collection.insert_one({'name' : name, 'year' :year, 'duration' : int(duration), 'diretor': diretor, 'imdb' : float(imdb), 'votes' : int(vote), 'gender' : gender  })


            dataFilms['film'].append({  
            'name': name,
            'year': year,
            'duration': int(duration),
            'diretor': diretor,
            'imdb': float(imdb),
            'votes': int(vote),
#            'gloss': float(gloss),
            'gender': gender
            })

    
                
with open('films.json', 'w+') as outfile:  
    json.dump(dataFilms, outfile)


'''
import pandas as pd

test_df = pd.DataFrame({'movie': names,
                       'diretor':diretors,
                       'year': years,
                       'duration':durations,
                       'imdb': imdb_ratings,
                       'gender':genders,
                       'votes': votes})
print(test_df.info())
print(len(test_df))
test_df.to_csv("imdb_oficial.csv",index=False)
'''
