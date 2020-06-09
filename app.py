import requests
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, 'html.parser')

def get_url(query, loc):
    url = 'https://ca.indeed.com/jobs?'
    query = 'q=' + urllib.parse.quote_plus(query)
    loc = '&l=' + urllib.parse.quote_plus(loc)
    url += query + loc
    return url

query = 'carpenter'
loc = 'Vancouver, BC'

for start in np.arange(0, 31, 10):
    url = get_url(query, loc) + '&start='+str(start)
    soup = get_soup(url)
    
    regex = re.compile('.*jobsearch-SerpJobCard unifiedRow.*')
    cards = soup.find_all(class_=regex)
    
    if start == 0:
        title, company, salary,  location, post_url = [], [], [], [], []

    for card in cards:
        if str(card.find(class_='title')) != 'None':
            title.append(card.find('h2', class_='title').find('a')['title'])
            company.append(card.find(class_='company').text.strip())

            if str(card.find(class_='salaryText')) != 'None':
                salary.append(card.find(class_='salaryText').text.strip())
            else:
                salary.append('None')

            location.append(card.find(class_='location accessible-contrast-color-location').text)
            post_url.append(card.find(class_='title').find('a')['href'])

# define the dataframe df
df = pd.DataFrame(title, columns=['title'])
df['company'], df['salary'], = company, salary
df['location'], df['post_url'] = location, post_url

# save the dataframe to disk
df.to_csv('jobs.csv', index=False, sep=';')