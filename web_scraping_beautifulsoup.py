# Scraping data for over 2,000 movies

import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint


url = 'https://www.imdb.com/search/title/?release_date=2017-01-01,2017-12-31&sort=num_votes,desc&ref_=adv_prv'
response_obj = requests.get(url)
source = response_obj.text
html_soup = BeautifulSoup(source, 'lxml')
movies = html_soup.find_all('div', class_='lister-item mode-advanced')
# print(len(movies))
# print(list(movies)[0].prettify())
movie_name = movies[0].find('h3', class_='lister-item-header').a.text
movie_year = movies[0].h3.find('span', class_='lister-item-year text-muted unbold').text
# ======================================================================================================================
ratings = movies[0].find('div', class_='ratings-bar')
imdb_rating = ratings.strong.text
metascore = ratings.find('div', class_='inline-block ratings-metascore').span.text
# ======================================================================================================================
int_votes = movies[0].find('p', class_='sort-num_votes-visible')
votes = int_votes.find('span', attrs={'name': 'nv'}).text
# print(movie_name)
# print(movie_year)
# print(imdb_rating)
# print(metascore)
# print(votes)
# ======================================================================================================================
# Script for a single page
movie_names = list()
movie_years = list()
imdb_ratings = list()
meta_scores = list()
movie_votes = list()
# Extract data for individual movie
for movie in movies:
    # if movie has a metascore extract
    _ratings = movie.find('div', class_='ratings-bar')
    if _ratings.find('div', class_='inline-block ratings-metascore'):
        movie_name = movie.find('h3', class_='lister-item-header').a.text
        movie_names.append(movie_name)
        movie_year = movie.h3.find('span', class_='lister-item-year text-muted unbold').text
        movie_years.append(movie_year)
        imdb_rating = ratings.strong.text
        imdb_ratings.append(imdb_rating)
        meta_score = ratings.find('div', class_='inline-block ratings-metascore').span.text
        meta_scores.append(meta_score)
        int_votes = movie.find('p', class_='sort-num_votes-visible')
        votes = int_votes.find('span', attrs={'name': 'nv'}).text
        movie_votes.append(votes)

df = pd.DataFrame({'movie': movie_names, 'year': movie_years, 'votes': movie_votes,
                   'imdb': imdb_ratings, 'metascore': meta_scores})

'https://www.imdb.com/search/title/?release_date=2017-01-01,2017-12-31&sort=num_votes,desc&start=51&ref_=adv_nxt'

start = [str(i) if i != 0 else '' for i in [0, 51, 101, 151]]
years_url = [str(i) for i in range(2000, 2018)]
