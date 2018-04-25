from urllib import urlopen
import re
from bs4 import BeautifulSoup
import os
import Queue
import threading, time

product_details = open('details.txt', 'w')
product_details.write("Name|SKU#|Retail Price|Online Price|Today's Price|Description|Specifications\n")
exitflag = 0


class Links():
    def link_gatherer(self):
        base_url = 'http://realstreetperformance.com'
        manufacturer = raw_input('Enter manufacturer')
        url = 'http://realstreetperformance.com/Products/' + str(manufacturer) + '/'
        uh = urlopen(url)
        print('working')
        data = uh.read()
        data = data.decode('UTF-8')
        product_links = open('productlinks.txt', 'w+')
        if os.path.getsize('productlinks.txt') == 0:
            soup = BeautifulSoup(data)
            tags = soup('div', {'class': 'itemlist_list_name'})
            for tag in tags:
                product_links.write(base_url + str(tag.next['href']))
                product_links.write('\n')
        product_links.close()


class MyThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print "Starting " + self.name
        self.product_parser(self.name, self.q)
        print "Exiting " + self.name

    def product_parser(self, thread_name, q):
        while not q.empty():
                queuelock.acquire()
                new_url = q.get()
                queuelock.release()
                flag = 0
                try:
                    product_html = urlopen(new_url)
                except:
                    print 'BAD STATUS LINE, UNABLE TO READ ' + str(new_url)
                    return
                print thread_name + ' now parsing ' + new_url
                newdata = product_html.read()
                newdata = newdata.decode('UTF-8')
                soup1 = BeautifulSoup(newdata)
                name_tag = soup1('div', {'class': 'prod_title'})
                try:
                    product_name = str(name_tag[0].text)
                except:
                    product_name = 'Unknown Name'
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
                time.sleep(1)


scrapy = Links()
scrapy.link_gatherer()
print 'Links populated in productlinks.txt'
threadList = ["Thread-1", "Thread-2", "Thread-3"]
queuelock = threading.Lock()
workQueue = Queue.Queue(100)
threads = []
threadID = 1
f = open('productlinks.txt', 'r')
for link in f:
    workQueue.put(str(link))
for tName in threadList:
    thread = MyThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1


for t in threads:
    t.join()
print 'Main Program Complete'
product_details.close()
