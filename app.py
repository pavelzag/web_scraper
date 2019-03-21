#!/usr/bin/python3
from bs4 import BeautifulSoup
from contextlib import closing
from requests import get

import logging
import sys
import time
import threading
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.FileHandler('webscraper.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

tested_url = sys.argv[1]
print(tested_url)
def is_good_response(response):
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def simple_get(url):
    message = '{} {} {}'.format('Fetching', url, 'content')
    logger.info(message)
    print(message)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    with closing(get(url, headers=headers, stream=True)) as resp:
        if is_good_response(resp):
            return resp.content
        else:
            print('eh')
            return None

def check_alive(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                working_list.append(url)
                return
            else:
                non_working_list.append(url)
                return
    except:
        return


main_page_html = simple_get(url=tested_url)
links_list = []
soup = BeautifulSoup(main_page_html, 'lxml')
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

tested_page_links = []
for url in clean_urls_list:
    if tested_url in url:
        tested_page_links.append(url)


extended_link_list = []
extended_clean_urls_list = []
extended_tested_page_links = []

# Fetching links for all the pages under the domain:
for url in tested_page_links:
    main_page_html = simple_get(url=url)
    links_list = []
    soup = BeautifulSoup(main_page_html, 'lxml')
    for a in soup.find_all('a', href=True):
        extracted_link = a['href']
        extended_link_list.append(extracted_link)
    myset = set(extended_link_list)
    temp_list = list(myset)

    # remove non http links:
    for url in temp_list:
        if 'http' in url:
            extended_clean_urls_list.append(url)

    for url in clean_urls_list:
        if tested_url in url:
            extended_tested_page_links.append(url)

myset = set(extended_tested_page_links)
unique_links = list(myset)

threads = []
working_list = []
non_working_list = []
for x in range (0, len(unique_links)):
    url = unique_links[x]
    t = threading.Thread(target=check_alive, args=(url, ))
    threads.append(t)
    t.start()
    time.sleep(2)

print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
message = '{} {} {} {}'.format(tested_url, 'has', len(working_list), 'working pages')
print(message)
logger.info(message)
for url in working_list:
    message = '{}: {}'.format('This URL is working', url)
    print(message)
    logger.info(message)

print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
message = '{} {} {} {}'.format(tested_url, 'has', len(non_working_list), 'non working pages')
print(message)
logger.info(message)
for url in non_working_list:
    message = '{}: {}'.format('This URL is not working', url)
    print(message)
    logger.info(message)
print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')


