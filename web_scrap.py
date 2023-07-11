from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
# from proxies_checker import fetch_proxies

time.sleep(3)

# proxies = fetch_proxies()
# random_proxy = random.choice(proxies)

target = "https://finance.yahoo.com/quote/SPY/history?period1=1577836800&period2=1672531200&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true"
# user-agent header in the http request which identifies the client making the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(target, headers=headers)
#, proxies={'http': random_proxy, 'https': random_proxy}


content = response.text

# inicialize BeautifulSoup object and indicate analysis method
soup = BeautifulSoup(content, 'html.parser')

# getting needed data from url table
scrapped_data = []

table = soup.find('table', class_='W(100%) M(0)')
if table:
    rows = table.find_all('tr')
    for row in rows[1:]:
        columns = row.find_all('td')
        date = columns[0].text.strip()
        close = columns[-1].text.strip()
        if close == '':
            proxy = close(skiprows=[2])       

        # scrapped_data.append((date, close))
        print(close)

# df = pd.DataFrame(scrapped_data)
# print(df)

    