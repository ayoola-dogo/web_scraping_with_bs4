import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import time, sleep
from random import randint
from IPython.core.display import clear_output
from warnings import warn

movie_names = list()
movie_years = list()
imdb_ratings = list()
meta_scores = list()
movie_votes = list()

# Preparing the loop monitor
start_time = time()
request = 0

start = ['&start='+str(i) if i != 0 else '' for i in [0, 51, 101, 151]]
years_url = [str(i) for i in range(2000, 2018)]

# For every year in the interval between 2000 and 2017
for year_url in years_url:
    # For every page in the interval between 1 and 4
    for page in start:
        url = 'https://www.imdb.com/search/title/?release_date={0}-01-01,{0}-12-31&sort=num_votes,desc{1}&ref_=adv_prv'\
            .format(year_url, page)
        # Make a request
        response = requests.get(url)
        # Pause the loop
        sleep(randint(8, 15))
        # Monitor the requests
        request += 1
        elapsed_time = time() - start_time
        print('Requests: {}, Frequency: {} requests/s'.format(request, request/elapsed_time))
        clear_output(wait=True)
        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Requests: {} - Status code: {}'.format(request, response.status_code))
        # Break the loop if the number of requests is greater than expected
        if request > 72:
            warn('Number of requests was greater than expected.')
            break
        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'lxml')
        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_='lister-item mode-advanced')
        # For every movie of these 50
        for mv in mv_containers:
            _ratings = mv.find('div', class_='ratings-bar')
            # Check if movie as metascore if so, then:
            if _ratings.find('div', class_='inline-block ratings-metascore'):
                # Scrape the name and append to list
                movie_name = mv.find('h3', class_='lister-item-header').a.text
                movie_names.append(movie_name)
                # Scrape the year and append to list
                movie_year = mv.h3.find('span', class_='lister-item-year text-muted unbold').text
                movie_years.append(movie_year)
                # Scrape the IMDB rating and append to list
                imdb_rating = _ratings.strong.text
                imdb_ratings.append(imdb_rating)
                # Scrape the Metascore and append to list
                meta_score = _ratings.find('div', class_='inline-block ratings-metascore').span.text
                meta_scores.append(meta_score)
                # Scrape the number of votes and append to list
                int_votes = mv.find('p', class_='sort-num_votes-visible')
                votes = int_votes.find('span', attrs={'name': 'nv'}).text
                movie_votes.append(votes)

df = pd.DataFrame({'movie': movie_names, 'year': movie_years, 'votes': movie_votes,
                   'imdb': imdb_ratings, 'metascore': meta_scores})
print(df.info())
