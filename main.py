"""
main.py is where we call and use our implemented web scrapers 
and post to `postgres`. We do this by using two UDF.
1. scrape: scrape and aggregate the data to a singular pandas data frame
2. post: update the postgres database from the scraped data.
"""

from scraper import CNN
from sqlalchemy import create_engine
import psycopg2


def scrape():
    """
    `scrape` is a UDF that developers can use to specify and 
    configure to scrape from their chosen news sources.
    """

    cnn = CNN()
    seed = 'https://edition.cnn.com/2021/05/06/investing/bitcoin-cash-explainer/index.html'

    df = cnn.scrape(seed, 150)
    return df
    

def post():
    engine = create_engine('postgresql+psycopg2://postgres:1kind@localhost:5432/news')


if __name__ == '__main__':
    result = scrape()
    print(result)
    # post()
