from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


product_details = open('details.txt', 'w')
product_details.write("Name|SKU#|Retail Price|Online Price|Today's Price|Description|Specifications\n")


def product_parser(new_url):
    flag = 0
    product_html = urlopen(new_url)
    newdata = product_html.read()
    newdata = newdata.decode()
    soup1 = BeautifulSoup(newdata, "html.parser")
    name_tag = soup1('div', {'class': 'prod_title'})
    product_name = str(name_tag[0].text)
    sku_tag = soup1('div', {'class': 'prod_sku'})
    x = re.findall('#: (.*)<!', str(sku_tag))
    product_sku_number = str(x[0])
    prices_tags = soup1('div', {'class': 'retail_price'})
    prices = list()
    for prices_tag in prices_tags:
        x = re.findall('">(.+)</', str(prices_tag))
        if len(x) == 0:
            continue
        prices.append(x[0])
    y = re.findall(': (.+)', str(prices[0]))
    product_retail_price = str(y[0])
    y = re.findall(': (.+)', str(prices[1]))
    product_online_price = str(y[0])
    y = re.findall(': (.+)', str(prices[2]))
    product_today_price = str(y[0])
    desc_exists_tag = soup1('div', {'class': 'title_item'})
    if desc_exists_tag[0].text.strip() == 'Description':
        desc_tag = soup1('div', {'class': 'iteminfo-box'})
        x = re.findall('">([a-z A-Z].+?)</[a-z A-Z]?', str(desc_tag[0]))
        if len(x) == 0:
            product_description = 'No Description'
        else:
            product_description = str(x[0])
    else:
        product_description = 'No Description'
    product_details.write(product_name + '|')
    product_details.write(product_sku_number + '|')
    product_details.write(product_retail_price + '|')
    product_details.write(product_online_price + '|')
    product_details.write(product_today_price + '|')
    product_details.write(product_description + '|')
    specs_exists_tag = soup1('div', {'id': 'title-spec'})
    if specs_exists_tag[0].text.strip() == 'Specifications':
        title_spec_tags = soup1('div', {'class': 'title_item spec'})
        answer_spec_tags = soup1('div', {'class': 'iteminfo-box spec'})
        del title_spec_tags[0]
        for (title_spec_tag, answer_spec_tag) in zip(title_spec_tags, answer_spec_tags):
            if answer_spec_tag.text.strip() == '':
                continue
            else:
                flag = 1
                product_details.write(
                    str(title_spec_tag.text.strip()) + ': ' + str(answer_spec_tag.text.strip()) + '\t')
    else:
        product_specifications = 'No Specifications'
        product_details.write(product_specifications + '\n')
    if flag is not 1:
        product_specifications = 'No Specifications'
        product_details.write(product_specifications + '\n')
    else:
        product_details.write('\n')


f = open('productlinks.txt', 'r')
for link in f:
    print('Now parsing ' + str(link))
    product_parser(link)


product_details.close()