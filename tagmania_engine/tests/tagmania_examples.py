#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs,sys,spacy
sys.path.append('../')

from TagmaniaProcessor import TagmaniaProcessor, ptt
from rules_tree import get_rules
from tagmania_helper import replace_contractions
from pprint import pprint



def spacy_tag(text):
    if 'nlp' not in spacy_tag.__dict__:
        spacy_tag.nlp = spacy.load('en')
    nested_list = [(w.text, w.tag_) for w in spacy_tag.nlp(text)]
    ents  = spacy_tag.nlp(text).ents
    return nested_list, ents
spacy_tag.nlp = spacy.load('en')


def apply_rules(rule_set,tagged, rule_file=False):
    applied,rules = [], []
    
    if rule_file:
       rules = get_rules(rule_set,tagged)
    else:
       rules = rule_set 
    for rule in rules:
        
        processor = TagmaniaProcessor(rule)
    	valid, mods, tagged  = processor.transform(tagged)		
        if valid:
           applied.append(rule)
        
    return tagged, applied







def ex2():
             
    text = u"The bill passed 81-18. Sixteen Democrats and two libertarian-minded Republicans voted against it. Among them were a number of potential Democratic presidential candidates in 2020 including Cory Booker, Kirsten Gillibrand, Kamala Harris, Bernie Sanders and Elizabeth Warren" 
    
    #disambiguate NNP
    
    rule_set = [u'<CD SYM CD>,CD', 
                u'PERSON PERSON|COMMA+ <NNP+> and PERSON,PERSON',        
                u'<PERSON COMMA|PERSON+ and PERSON>,PERSON_LISTING',]
    
     
    
    text = replace_contractions(text)
    tagged,ents = spacy_tag(text)	
    pprint(tagged) 
    people  = [(ent.text,ent.label_) for ent in ents if ent.label_== u'PERSON']
            
     
    #add dynamic rules 
    if len(people) > 0:
       rule_set = [u'<{0}>,PERSON'.format(name) for name,_ in people] + rule_set 
    
    tagged, applied_rules = apply_rules(rule_set,tagged) 
    print "Out:\n",
    pprint(tagged)
    
    print "applied rules\n",
    pprint(applied_rules)
    print "----------------------------------------------------\n"





def ex1():
             
    lines = codecs.open('relative_clauses.txt','r',encoding='utf-8').read().splitlines()
    
    
    #identify Action in a sentence with a relative clause
    rule_set = [u'<I|she|he|we|you|they>,Pronoun',
		u'<DT JJ? NN|NNP|NNS>,Object',
		u'<^Pronoun|Object>,Subject',
		u'<is|was|were|are|am VBG>,Gerund',
		u'Subject that|who|which <Gerund|VBZ|VBP|VBD>^^<VBZ|VBP|VBD>,VP ACTION',  
		u'Subject <Gerund|VBZ|VBP|VBD>, ACTION']
    
    for ln in lines:
        
        ln = replace_contractions(ln)
        tagged,ents = spacy_tag(ln)	
        pprint(tagged) 
        
        tagged, applied_rules = apply_rules(rule_set,tagged) 
        print "Out:\n",
        pprint(tagged)
        
        print "applied rules\n",
        pprint(applied_rules)
        print "----------------------------------------------------\n"

if __name__ == '__main__':
   #ex1()
   ex2()
