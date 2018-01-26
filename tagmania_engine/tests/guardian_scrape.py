#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module to scrape news articles from the Guardian article search api.
"""

import requests
import json

class Guardian:
  def __init__(self, api_key):
    self.url = "https://content.guardianapis.com/search"
    self.api_key = api_key

  def get_text(self, search_term):
    """
    Get the lead paragraph from the Guardian articles matching this 
    search term. 
    """
    payload = {'q' : search_term, 'format' : 'json', 'show-fields' : 'headline', 'api-key' : self.api_key,'show-blocks':'all'}
    r = requests.get(self.url, payload)

    if (r.status_code != requests.codes.ok):
      r.raise_for_status()
    data = r.json()
    docs = data['response']['results']
    text = []
    for x in docs:
        
        text.append({'url': x['webUrl'] ,'webTitle':x['webTitle']}) 
    return text

if __name__ == '__main__':
   res = Guardian('95fc258c-d1ac-4479-9c76-627452c27591').get_text('US Government Shutdown')
   print res	
