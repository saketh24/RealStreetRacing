from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

base_url = 'http://realstreetperformance.com'
url = 'http://realstreetperformance.com/Products/Honda/'
uh = urlopen(url)
data = uh.read()
data = data.decode()
product_links = open('productlinks.txt', 'w+')
if os.path.getsize('productlinks.txt') == 0:
    soup = BeautifulSoup(data, "html.parser")
    tags = soup('div', {'class': 'itemlist_list_name'})
    for tag in tags:
        product_links.write(base_url + str(tag.next['href']))
        product_links.write('\n')
product_links.close()
