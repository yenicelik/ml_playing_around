import pandas as pd
import numpy as np
import urllib2
import requests
import lxml
import re
from unidecode import unidecode

import time

try:
    import scrapy
except ImportError:
    import pip
    pip.main(['install', 'scrapy'])
    import scrapy
    
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup

#try:
#    import newspaper
#except ImportError:
#    import pip
#    pip.main(['install', 'newspaper'])
#    import newspaper

fb_data = pd.read_csv('DailyMail_facebook_statuses.csv')

fb_data = fb_data[fb_data['status_link'].str.contains("http://dailym.ai/")]

links = fb_data['status_link']

links.to_csv('DailyMail_facebook_statuses_links.csv')

def get_body(url):
    page = urllib2.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(page)
    html = soup.prettify()
    #text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    #return soup.title.text, text
    return soup.title.text, soup.content

def get_text(url):
    """ return title, description and text from the body of a given html """
    try:
        response = requests.get(url, timeout=20)
        response.encoding = 'ISO-88959-1'

        #Create a bs-parser class
        soup = BeautifulSoup(response.content, 'lxml')


        #Try to catch title and description tag
        title = re.sub(' \| Daily Mail Online', '', unidecode(soup.title.string))

        tmpall = soup.findAll('meta')
        for meta in tmpall:
            if 'description' == meta.get('name', '').lower():
                description = meta['content']
                break

        #Remove certain tags from html
        for script in soup(["script", "style", "img", "video"]):
            script.extract()

        tmpall = soup.findAll("div", {"itemprop" : "articleBody"})

        text = unidecode(' '.join(map( lambda p: p.text, soup.find_all("p", {"class" : "mol-para-with-font"}))))

        return title, description, text
    except Exception as err:
        print(err)
        return '', '', ''

title, descr, text = get_text(links[0])

print("Title")
print(title)
print
print("Description")
print(descr)
print
print("Text")
print(text)

for url in links[::2]:
    title, descr, text = get_text(url)
    with open("DailyMail_titles.txt", "a") as myfile:
        myfile.write(title.encode('utf-8') + '. ')
    with open("DailyMail_descriptions.txt", "a") as myfile:
        myfile.write(descr.encode('utf-8') + ' <br /> ')
    with open("DailyMail_content.txt", "a") as myfile:
        myfile.write(text.encode('utf-8') + '<br /> ')
    #time.sleep(0.2)
    print(url)