import requests
from bs4 import BeautifulSoup


def fetch_proxies():
    url = "https://free-proxy-list.net"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    proxies = []

    table = soup.find('table', class_='table-striped')
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            ip = columns[0].text.strip()
            port = columns[1].text.strip()
            protocol = columns[6].text.strip().lower()
            if protocol == 'no':
                proxy = f'http://{ip}:{port}'
            elif protocol == '':
                proxy = f'{ip}:{port}'
            else:
                proxy = f'https://{ip}:{port}'
                proxies.append(proxy)
    return proxies


print(fetch_proxies())
