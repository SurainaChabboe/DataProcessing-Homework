#!/usr/bin/env python
# Name:
# Student number:
'''
This script scrapes IMDB and outputs a CSV file with highest rated tv series.
'''
import csv

from pattern.web import URL, DOM

TARGET_URL = "http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series"
BACKUP_HTML = 'tvseries.html'
OUTPUT_CSV = 'tvseries.csv'


def extract_tvseries(dom):
    '''
    Extract a list of highest rated TV series from DOM (of IMDB page).

    Each TV series entry should contain the following fields:
    - TV Title
    - Rating
    - Genres (comma separated if more than one)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    '''

    url = URL("http://www.imdb.com/search/title?num_votes=5000,&sort=user_rating,desc&start=1&title_type=tv_series") 
    dom = DOM(url.download(cached=True))   
    for a in dom('div[class="lister-item-content"]'):
        actors = []
        title = a('a')[0].content
        rating = a('strong')[0].content 
        runtime = a('span[class="runtime"]')[0].content
        genres = a('span[class="genre"]')[0].content
        for e in range(12, 16):
            actors.append(a('a')[e].content)
    return (title, rating, runtime, genres, actors)

def save_csv(f, tvseries):
    '''
    Output a CSV file containing highest rated TV-series.
    '''
    x = extract_tvseries(dom)

    with open(OUTPUT_CSV, "wb") as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Rating', 'Genre', 'Actors', 'Runtime'])
        for i in range(50):
            writer.writerow(x)

if __name__ == '__main__':
    # Download the HTML file
    url = URL(TARGET_URL)
    html = url.download()

    # Save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # Parse the HTML file into a DOM representation
    dom = DOM(html)

    # Extract the tv series (using the function you implemented)
    tvseries = extract_tvseries(dom)

    # Write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'wb') as output_file:
        save_csv(output_file, tvseries)