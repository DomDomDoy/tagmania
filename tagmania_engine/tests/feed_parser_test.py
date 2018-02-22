#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
parse stories from the guardian rss feed
"""
import feedparser,sys,json,urllib2
from bs4 import BeautifulSoup

def get_stories(feed='https://www.theguardian.com/world/rss'):
    d = None
    rss_dump = []
    f_out = open('stuff.json','w')
    try:
   	d = feedparser.parse(feed) 	 
    except:
	sys.exit("feed not valid")
    
    for thing in d['entries']:	
	rss_dump.append({'title':thing['title'],'paragraphs': get_paragraphs(thing['link'])})
    f_out.write(json.dumps(rss_dump, encoding='utf-8'))	 		
	
def get_paragraphs(url):
    """
    get paragraphs from an article
    """
    soup = BeautifulSoup(urllib2.urlopen(url),"html5lib")
    paragraphs = soup.find('article').find_all('p')
    return [p.text for p in paragraphs] 

if __name__ == '__main__':
  get_stories()	
