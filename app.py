#!/usr/bin/python3
from bs4 import BeautifulSoup
from contextlib import closing
from requests import get

import logging
import time
import threading
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('webscraper.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def is_good_response(response):
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def simple_get(url):
    message = '{} {} {}'.format('Testing if', url, 'is working')
    logger.info(message)
    print(message)
    with closing(get(url, stream=True)) as resp:
        if is_good_response(resp):
            return resp.content
        else:
            print('eh')
            return None

def check_alive(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                print('{} {}'.format(url, 'is working'))
                working_list.append(url)
                return
            else:
                print('{} {}'.format(url, 'is not working'))
                non_working_list.append(url)
                return
    except:
        return




main_page_html = simple_get(url='http://www.guardicore.com')
links_list = []
soup = BeautifulSoup(main_page_html)
for a in soup.find_all('a', href=True):
    extracted_link = a['href']
    links_list.append(extracted_link)
myset = set(links_list)
temp_list = list(myset)
clean_urls_list = []

# remove non http links:
for url in temp_list:
    if 'http' in url:
        clean_urls_list.append(url)

guardicore_links = []
for url in clean_urls_list:
    if "www.guardicore" in url:
        guardicore_links.append(url)

threads = []
working_list = []
non_working_list = []
for x in range (0, len(clean_urls_list)):
    url = clean_urls_list[x]
    t = threading.Thread(target=check_alive, args=(url, ))
    threads.append(t)
    t.start()
    time.sleep(1)
print(working_list)
print(non_working_list)


