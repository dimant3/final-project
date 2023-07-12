import psycopg2
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
from postgres import db_con, create_table
# from proxies_checker import fetch_proxies

time.sleep(3)

# proxies = fetch_proxies()
# random_proxy = random.choice(proxies)

target = "https://finance.yahoo.com/quote/SPY/history?period1=1577836800&period2=1672531200&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=false"
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

table = soup.find('table', class_='W(100%)')
if table:
    rows = table.find_all('tr')
    for row in rows[1:]:
        if 'Dividend' in row.text:
            continue
        columns = row.find_all('td')

        try:
            date = columns[0].text.strip()
        except IndexError:
            date = ""

        try:
            open_price = columns[1].text.strip()
        except IndexError:
            open_price = ""

        try:
            high_price = columns[2].text.strip()
        except IndexError:
            high_price = ""

        try:
            low_price = columns[3].text.strip()
        except IndexError:
            low_price = ""

        try:
            close_price = columns[4].text.strip()
        except IndexError:
            close_price = ""

        try:
            adj_close_price = columns[5].text.strip()
        except IndexError:
            adj_close_price = ""

        try:
            volume = columns[6].text.strip()
        except IndexError:
            volume = ""

        #inserting all table values from url to the list scrapped_data
        scrapped_data.append({
            'Date': date,
            # 'Open': open_price,
            # 'High': high_price,
            # 'Low': low_price,
            'Close': close_price,
            # 'Adj Close': adj_close_price,
            # 'Volume': volume
            })
db_con()
create_table()
# taking data from our scrapped_data list and inserting into database
for entry in scrapped_data:
    date = entry['Date']
    close_price = entry['Close']

    connection = psycopg2.connect(**db_con())
    cursor = connection.cursor()

    insert_data_into_table = """
            INSERT INTO sp500 (date, close)
            VALUES (%s, %s)
        """
    values = (date, close_price)

    cursor.execute(insert_data_into_table, values)

    connection.commit()
    cursor.close()
    connection.close()
    