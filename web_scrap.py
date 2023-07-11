from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

delay = 3

url = 'https://finance.yahoo.com/quote/SPY/history?p=SPY'
time.sleep(delay)


target = "https://finance.yahoo.com/quote/SPY/history?p=SPY"
# user-agent header in the http request which identifies the client making the request
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(target, headers=headers)

print(response.status_code)

# inicialize BeautifulSoup object and indicate analysis method
# soup = BeautifulSoup(content, 'html.parser')

# getting needed data from url table
# sp500_data = soup.find_all('div', )