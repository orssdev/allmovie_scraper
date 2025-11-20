# For collecting the indexes urls to scrape movie data

import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from protego import Protego

load_dotenv()

user_agent = os.getenv('USER_AGENT')
HEADERS = {'user-agent': user_agent}
url = 'https://www.allmovie.com'
response = requests.get(url + '/robots.txt', headers=HEADERS)
rp = Protego.parse(response.text)
crawl_delay = rp.crawl_delay(user_agent) or 0

if rp.can_fetch('https://www.allmovie.com/genres', user_agent):
     response = requests.get('https://www.allmovie.com/genres', headers=HEADERS)
     soup = BeautifulSoup(response.text, 'html.parser')
     content = soup.select('.content a[href^="https"]')
     # Unix pipe into file `python collect_urls.py > ../data/urls.txt`
     print('[')
     for a in content:
          href = a.get('href')
          print(f'\t"{href}",')
     print(']')