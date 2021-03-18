##import libraries
from bs4 import BeautifulSoup
import time, re
import urllib.request as ulb
import numpy as np
import sys



##print html (urllib)
"""
    test website:
    https://www.canadapharmacy.com = 82
    http://news.163.com/ = 759
    total url: 841
"""



site_url = []

##read data from txt file
def read(ms):
    master_website = set()
    file_name = ms
    with open(file_name,'r') as files:
        for line in files:
            for item in  list(line.strip('\n').split(',')):
                master_website.add(item)
    return master_website



## print html doc(bs4)
## spider_deepth control the deepth of spider
def scan_url_list(url_set, spider_deepth):
    for i in range(0, spider_deepth):
        tmp_set = set()
        for web_url in url_set:
            t1 = time.time()
            html = ulb.urlopen(web_url).read()
            soup = BeautifulSoup(html, "lxml")
            for link in soup.find_all('a'):
                temp = link.get('href')
                if temp is not None and len(temp) > 1:
                    if temp.startswith('/'):
                        tmp_set.add(web_url + temp)
                        site_url.append(web_url + temp)
                    if temp.startswith('http'):
                        tmp_set.add(temp)
                        site_url.append(temp)
            t2 = time.time()
            print("time for ", web_url, "is ", t2-t1)
        url_set.update(tmp_set)
    return url_set

def scan_single_url(url, spider_deepth):
    url_tree = set();
    url_tree.add(url);
    have_visted = set();
    for i in  range(0, spider_deepth):
        help_set = set()
        for web_url in url_tree:
            if web_url in have_visted:
                continue
            t1 = time.time()
            html = ulb.urlopen(web_url).read()
            soup = BeautifulSoup(html, "lxml")
            for link in soup.find_all('a'):
                temp = link.get('href')
                if temp is not None and len(temp) > 1:
                    if temp.startswith('/'):
                        help_set.add(web_url + temp)
                    if temp.startswith('http'):
                        help_set.add(temp)
            t2 = time.time()
            print("time for ", web_url, "is ", t2-t1)
        have_visted = url_tree
        url_tree.update(help_set)
    return url_tree
## store data into txt file
def output(filename):
    url = site_url
    f_name = filename
    with open(f_name,'w') as files:
        for u in url:
            files.write(u + '\n')
        files.close()
    print("Output Complete! Total links: ",len(url))



# ##Module start running
# master_website = read('master_website.txt')
# scan_url_list(master_website, 1)
# print(len(scan_single_url("https://www.canadapharmacy.com",1)) + len(scan_single_url("http://news.163.com/",1)))
# output('output.txt')

