from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
from proxies_checker import fetch_proxies

time.sleep(3)

proxies = fetch_proxies()
random_proxy = random.choice(proxies)
target = "https://www.investing.com/etfs/spdr-s-p-500-historical-data?GL_Ad_ID=626070286015&GL_Campaign_ID=18502377045&ISP=1&ppu=1"
# user-agent header in the http request which identifies the client making the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(target, headers=headers, proxies={'http': random_proxy, 'https': random_proxy})

# inicialize BeautifulSoup object and indicate analysis method
# soup = BeautifulSoup(content, 'html.parser')

# getting needed data from url table
# sp500_data = soup.find_all('div', )
