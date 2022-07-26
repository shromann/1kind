#____________________ Solution Design ____________________
"""
Scaper.py is designed with an OOP approach; where there exists 
a general web scrapper pattern which will be needed to be 
configured for various web news article sources.

This solution design is the most appropriate for this problem 
every web news source has its own unique layout of its 
unstructured html data, and allows us to scale to more features
and news sources.

In these demonstration, the general web scraper is of class 
name `news` and an implementation of it is called `CNN`, where
the source is from `CNN`.
"""
#_________________________________________________________

######################## Libraries ########################

from bs4 import BeautifulSoup
import pandas as pd
import requests
import sys
import re
import psycopg2
from config import config

################### General Web Scraper ###################
"""
the general web scraper has 6 method:

- title
- date
- author
- desc
are methods that extract and clean the features that we're more 
intrested in studing

- getRelatedNews
is a method to fetch more news links from the given page which 
may be of intrest

- scrape
is a general web scraper to extract, clean and aggregate the
features mentioned above
"""

class news:
    def __init__(self, source):
        self.source = source

    def title(self):
        sys.exit(f'title method not Implemented for {self.source}')

    def date(self):
        sys.exit(f'date method not Implemented {self.source}')

    def author(self):
        sys.exit(f'author method not Implemented {self.source}')

    def desc(self):
        sys.exit(f'desc method not Implemented {self.source}')

    def getRelatedNews(self):
        sys.exit(f'related news method not Implemented {self.source}')

    def scrape(self, seed, visit_limit):
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # args: 
        #   seed: specify the seed url for the webscraper to start
        #   visit_limit: specify the number of articles to scrape
        urls = [seed]
        visited = set()

        news = {'title':[], 'author':[], 'date':[], 'desc':[]}


        while len(visited) < visit_limit:
            if not urls:
                break
            url = urls.pop(0)
            if url not in visited:
                req = requests.get(url)
                soup = BeautifulSoup(req.content, 'html.parser')
                try:
                    title = self.title(soup)
                    date  = self.date(soup)
                    author = self.author(soup)
                    desc = self.desc(soup)

                    news['title'].append(title)
                    news['author'].append(author)
                    news['date'].append(date)
                    news['desc'].append(desc)


                except AttributeError:
                    continue

                visited.add(url)

                print(f'{title[:20]}...',' | ' ,date,' | ', author,' | ',  f'{desc[:10]}...')

                if len(visited) + len(urls) < visit_limit:
                    urls += self.getRelatedNews(soup)

        return pd.DataFrame(news)

######################## CNN Child Class ########################

class CNN(news):

    url_pattern = r'https:\/\/www\.cnn\.com\/\d{4}\/\d{2}\/\d{2}/investing\/(.*)\/index.html'

    def __init__(self):
        super().__init__('CNN')
    
    def title(self, soup):
        # extract
        text = soup.find(class_='pg-headline').get_text()
        # clean
        text = text.strip()
        return text

    def date(self, soup):
        # extract
        text = soup.find(class_ ='update-time').get_text()
        # clean
        text = text[28:]
        return text

    def author(self, soup):
        # extract
        text = soup.find(class_='metadata__byline__author').get_text()
        # clean
        text = text.removeprefix('By ').removesuffix(', CNN Business')
        return text
    
    def desc(self, soup):
        # extract
        desc = [p.get_text() for p in soup.find_all(class_='zn-body__paragraph')]
        return ''.join(desc)

    def getRelatedNews(self, soup):
        # extract and clean
        return [a['href'] for a in soup.find_all('a', href=True) if bool(re.search(self.url_pattern, a['href']))]

    def scrape(self, seed, visit_limit):
        return super().scrape(seed, visit_limit)
        
