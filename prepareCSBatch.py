import os
import json
from pprint import pprint

movies = []
csFormatMovies = []

for root, dirs, filenames in os.walk('./data'):
    for f in filenames:
        with open('./data/' + f, 'r') as data_file:    
            data = json.load(data_file)
            movies += data

for movie in movies:
    if('movieTitle' in movie and 'Title' in movie):
        movieId = movie['movieTitle'].strip().replace(' ', '_') + '__' + movie['Title'].strip().replace(' ', '_')
        csFormatMovie = {
            "type": "add",
            "id": movieId,
            "fields": movie
        }
        csFormatMovies.append(csFormatMovie)

with open('./batches/csBatch.json', 'w') as f:
    f.write(json.dumps(csFormatMovies))