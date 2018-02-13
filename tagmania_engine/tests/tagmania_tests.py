#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 
for each class, test of individual pattern level as well as group level

"""
import spacy, sys,pytest 
from beaut_scraping import get_paragraphs
from nltk.tree import Tree
sys.path.append('../')
from TagmaniaProcessor import TagmaniaProcessor, ptt


tagged_text1 = [(u'Give', u'VB'),
                 (u'me', u'PRP'),
                 (u'a', u'DT'),
                 (u'reason', u'NN'),
                 (u',', u','),
                 (u'why', u'WRB'),
                 (u'this', u'DT'),
                 (u'is', u'VBZ'),
                 (u'a', u'DT'),
                 (u'test', u'NN'),
                 (u'of', u'of'),
                 (u'grandeur', u'NN'),
                 (u'.', u'.')] 

tagged_text2 = [(u'he',u'PRP'),
                Tree('VP',[(u'was',u'VBZ'),(u'going','VBZ')]), 
                (u'there',u'PLACE')]

@pytest.mark.parametrize('test_rule,tagged,expected_del,expected_add', [

       	 
    pytest.param(u'<DT NN>,Nope',
               tagged_text1,
               [(2, (u'a', u'DT')), (3, (u'reason', u'NN')), (8, (u'a', u'DT')), (9, (u'test', u'NN'))],
               [(2, Tree('Nope', [(u'a', u'DT'), (u'reason', u'NN')])), (8, Tree('Nope', [(u'a', u'DT'), (u'test', u'NN')]))],
               marks=[pytest.mark.basic],
	       id='<DT NN>,Nope' ),

    pytest.param(u'<^VB PRP>,Nope',
                   tagged_text1,
                   [(0, (u'Give', u'VB')), (1, (u'me', u'PRP'))],
                   [(0, Tree('Nope', [(u'Give', u'VB'), (u'me', u'PRP')]))],
                   marks=[pytest.mark.basic],
                   id='<^VB PRP>,Nope' ),

    pytest.param(u'<PERIOD$>,Nope',
                   tagged_text1,
                   [(12, (u'.', u'.'))],
                   [(12, Tree('Nope', [(u'.', u'.')]))],
                   marks=[pytest.mark.basic],
                   id='<PERIOD$>,Nope' ),

    pytest.param(u'<VB|VBZ> PRP|DT,Nope',
                   tagged_text1,
                   [(0, (u'Give', u'VB')), (7, (u'is', u'VBZ'))],
                   [(0, Tree('Nope', [(u'Give', u'VB')])), (7, Tree('Nope', [(u'is', u'VBZ')]))],
                   marks=[pytest.mark.basic],
                   id='<VB|VBZ> PRP|DT,Nope' ),

    pytest.param(u'<VB> DT!,Nope',
                   tagged_text1,
                   [(0, (u'Give', u'VB'))],
                   [(0, Tree('Nope', [(u'Give', u'VB')]))],
                   marks=[pytest.mark.basic],
                   id='<VB> DT!,Nope' ),

    pytest.param(u'<VP{was}>,Nope',
                   tagged_text2,
                   [(1, Tree('VP', [(u'was', u'VBZ'), (u'going', 'VBZ')]))],
                   [(1, Tree('Nope', [Tree('VP', [(u'was', u'VBZ'), (u'going', 'VBZ')])]))],
                   marks=[pytest.mark.basic],
                   id='<VP{was}>,Nope' ),

    pytest.param(u'VP{was} <PLACE$>,Tag1',
                   tagged_text2,
                   [(2, (u'there', u'PLACE'))],
                   [(2, Tree('Tag1', [(u'there', u'PLACE')]))],
                   marks=[pytest.mark.basic],
                   id='VP{was} <PLACE$>,Tag1' ),

    pytest.param(u'<VB> PRP!,Nope',
                   tagged_text1,
                   [],
                   [],
                   marks=[pytest.mark.basic,pytest.mark.xfail(reason='no matching pattern')],
                   id='<VB> PRP!,Nope' ),

    pytest.param(u'<a NN|of*>, NER',
                   tagged_text1,
                   [(2, (u'a', u'DT')), (3, (u'reason', u'NN')), (8, (u'a', u'DT')), (9, (u'test', u'NN')), (10, (u'of', u'of')), (11, (u'grandeur', u'NN'))],
                   [(2, Tree('NER', [(u'a', u'DT'), (u'reason', u'NN')])), (8, Tree('NER', [(u'a', u'DT'), (u'test', u'NN'), (u'of', u'of'), (u'grandeur', u'NN')]))],
                   marks=[pytest.mark.basic],
                   id='<a NN|of*>, NER' ),
    ]) 
   
def test_search_engine(test_rule,tagged,expected_del,expected_add):
    
    processor = TagmaniaProcessor(test_rule)
    valid, mods, transformed_input = processor.transform(tagged)	  
    assert valid, mods['to_delete'] == expected_del
    assert mods['to_add'] == expected_add


def run_tagmania_rule(tagged_text,patt,sample,marx=[pytest.mark.basic]):
    """ 
    run tagmania rule , generate parametrized version of 


    """
    processor = TagmaniaProcessor(patt)
    valid, modifications, tagged_text_mod = processor.transform(tagged_text)
        
    print u"""pytest.param(u\'{patt}\',
               {name_of_tagged},
               {expected_del},
               {expected_add},
               marks={marker},
	       id=\'{patt}\' ),\n""".format(patt=patt, 
                                        name_of_tagged=sample,
                                        expected_del=modifications['to_delete'],
                                        expected_add=modifications['to_add'],
                                        marker=marx )



if __name__ == '__main__':
   import pprint
   #text =  u"Give me a reason, why this is a test."
   """
   patts = [u'<DT NN>, DT_TITLE',
            u'<^VB PRP>, STARTING_VB',
            u'<PERIOD$>, FULL_STOP',
            u'<VB|VBZ> PRP|DT, Nope',
            u'<VB> DT!, Nope',
            u'<PRP>, PRONOUN',
            u'<VB> PRP!, Nope',
            u'<VBZ> PRP!, Nope',
            #u'<VB|VBZ> PRP!, Nope',  
            
            #u'<DT NN>^^<DT NN>,Nope Nope2',
            #u'<.{test}>, Nope',
            
            u'VB{<Give>} PRP, VERB',
            u'<VB{<Give>}> <PRP>, COMMAND VERB NOUN',
            u'<a NN|of*>, NER_MAN'] 
            
   """ 
   
   #generate parameterized pytest params from dictionaries 
   patt_dicts = [{'patt':u'<DT NN>,Nope','sample':'tagged_text1','marx':'[pytest.mark.basic]'},
            {'patt':u'<^VB PRP>,Nope','sample':'tagged_text1','marx':'[pytest.mark.basic]'},
            {'patt':u'<PERIOD$>,Nope','sample':'tagged_text1','marx':'[pytest.mark.basic]'},
            {'patt':u'<VB|VBZ> PRP|DT,Nope','sample':'tagged_text1','marx':'[pytest.mark.basic]'},
            {'patt':u'<VB> DT!,Nope','sample':'tagged_text1','marx':'[pytest.mark.basic]'},
            {'patt':u'<VP{was}>,Nope','sample':'tagged_text2','marx':'[pytest.mark.basic]'},    
            {'patt':u'VP{was} <PLACE$>,Tag1','sample':'tagged_text2','marx':'[pytest.mark.basic]'},    
            {'patt':u'<VB> PRP!,Nope','marx':"[pytest.mark.basic,pytest.mark.xfail(reason='no matching pattern')]",'sample':'tagged_text1'},
            {'patt':u'<a NN|of*>, NER','sample':'tagged_text1','marx':'[pytest.mark.basic]'},] 

   #pprint.pprint(tagged_text1)
   
   for patt_dict in patt_dicts:        
       tagged_text = None 
       if patt_dict['sample'] == 'tagged_text1':
           tagged_text = tagged_text1
       elif patt_dict['sample'] == 'tagged_text2':
           tagged_text = tagged_text2   

       run_tagmania_rule(tagged_text,**patt_dict)
       
   
