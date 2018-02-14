#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spacy, sys,codecs
from nltk.tree import Tree
sys.path.append('../')
from TagmaniaProcessor import TagmaniaProcessor, ptt
from rules_tree import get_rules 
from pprint import pprint



def spacy_tag(text):
    if 'nlp' not in spacy_tag.__dict__:
        spacy_tag.nlp = spacy.load('en', parser=False, entity=False)
    nested_list = [(w.text, w.tag_) for w in spacy_tag.nlp(text)]
    return nested_list
spacy_tag.nlp = spacy.load('en', parser=False, entity=False)


def apply_rules(rule_set,tagged):
    for rule in get_rules(rule_set,tagged):
        processor = TagmaniaProcessor(rule)
    	valid, mods, tagged  = processor.transform(tagged)		
    return tagged	

def main():
         
    lines = codecs.open('article_test.txt','r',encoding='utf-8').read().splitlines()	    
    
    tag_to_look_for = 'NUMBERY_ENTITIES'
    res = []
    for ln in lines:
        tagged = spacy_tag(ln)
	tmp_res = [thing for thing in apply_rules('rule_set1',tagged) if type(thing) is Tree and thing.label() == tag_to_look_for]	 
        if len(tmp_res) > 0:
           print "line match"
           pprint(tagged)  
           res += tmp_res 
    pprint(res) 

if __name__ == '__main__':
   main() 
