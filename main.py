import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0.2) Gecko/20100101 Firefox/94.0.2',
    'Accept-Language': 'en-US, en;q=0.5'
}
#User Input
search_item = input("Sisestage otsitav ese: ").replace(' ', '+')
pages_to_display = input("Mitut lehekülge kuvada(1-3): ")
pages_to_display = int(pages_to_display) + 1
if pages_to_display > 4 or pages_to_display < 1:
    print('Kasutage vahemikku 1-3')
    exit()
base_url = 'https://www.amazon.com/s?k={0}'.format(search_item)

#Data processing
items = []
for i in range(1, pages_to_display):
    print('Töötlemas {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text

        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find_all('span', {'aria-label': True})[1].text
        except AttributeError:
            continue

        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price = float((price1 + price2).replace(',', ''))
            product_url = 'https://amazon.com' + result.h2.a['href']
            items.append([product_name, rating, rating_count, price, product_url])
        except AttributeError:
            continue
    sleep(1.5)

#Output to csv
df = pd.DataFrame(items, columns=['toode', 'hinnang', 'hinnangute arv', 'hind', 'toote url'])
df.to_csv('{0}.csv'.format(search_item), index=False)
print('Tulemused projektikausta .csv failis')