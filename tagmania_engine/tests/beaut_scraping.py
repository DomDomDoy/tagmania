#!/usr/bin/env python
# -*- coding: utf-8 -*-



import urllib2
from bs4 import BeautifulSoup

# Ask user to enter URL

#guardian_key = "95fc258c-d1ac-4479-9c76-627452c27591"
#url = "https://content.guardianapis.com/search"


# retrieve all of the paragraph tags

def get_paragraphs(url = "https://www.theguardian.com/us-news/2018/jan/22/government-shutdown-republicans-democrats"):
    """
    get paragraphs from an article
    """
    soup = BeautifulSoup(urllib2.urlopen(url),"html5lib")
    paragraphs = soup.find('article').find_all('p')
    return [p.text for p in paragraphs]
if __name__ == '__main__':
    for thing in get_paragraphs():
        print thing
