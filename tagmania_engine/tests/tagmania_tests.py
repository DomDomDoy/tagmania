#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" 
for each class, test of individual pattern level as well as group level

"""
import spacy, sys,pytest 
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
                 (u'.', u'.')] 

tagged_text2 = [(u'he',u'PRP'),Tree('VP',[(u'was',u'VBZ'),(u'going','VBZ')])]

@pytest.mark.parametrize('test_rule,tagged,expected', [
       	 
    pytest.param(u'<DT NN>,Nope',
                 tagged_text1,
                 [(2, (u'a', u'DT')),
		  (3, (u'reason', u'NN')),
		  (8, (u'a', u'DT')),
		  (9, (u'test', u'NN'))],
                 marks=pytest.mark.basic,
		 id='<DT NN>' ),
     
    
    pytest.param(u'<^VB PRP>,Nope',
                 tagged_text1,
                 [(0, (u'Give', u'VB')), 
	 	  (1, (u'me', u'PRP'))],
                 marks=pytest.mark.basic,
		 id='<^VB PRP>' ),
    
    pytest.param(u'<PERIOD$>,Nope',
                 tagged_text1,
                 [(10, (u'.', u'.'))],
                 marks=pytest.mark.basic,
		 id='<PERIOD$>' ),
    
    pytest.param(u'<VB|VBZ> PRP|DT,Nope',
                 tagged_text1,
                 [(0, (u'Give', u'VB')), (7, (u'is', u'VBZ'))],
                 marks=pytest.mark.basic,
		 id='<VB|VBZ> PRP|DT' ),
    
    pytest.param(u'<VB> DT!,Nope',
                 tagged_text1,
                 [(0, (u'Give', u'VB'))],
                 marks=[pytest.mark.basic],
		 id='<VB> DT!' ),
    	
    pytest.param(u'<VB> PRP!,Nope',
                 tagged_text1,
                 [],
                 marks=[pytest.mark.basic,pytest.mark.xfail(reason="no matching pattern")],
		 id='<VB> PRP!' ),
   ])
def test_tag_rule(test_rule,tagged,expected):
    
    processor = TagmaniaProcessor(test_rule)
    valid, mods, transformed_input = processor.transform(tagged)	 
    
	    
 
    assert valid, mods['to_delete'] == expected


"""
def check_patterns(tag_seq, patterns):
    processors = [TagmaniaProcessor(patt + ', None') for patt in patterns]
    return any(processor.validate(tag_seq) for processor in processors)


def run_tagmania_rule(text_tagged,patt):
     
    processor = TagmaniaProcessor(patt)
    valid, modifications, text_tagged = processor.transform(text_tagged)
    print u"pattern:{0}, valid:{1}".format(patt, valid)
    pprint.pprint(modifications)

if __name__ == '__main__':
   import pprint
   text =  u"Give me a reason, why this is a test."
   patts = [u'<DT NN>, Nope',
            u'<^VB PRP>, Nope',
            u'<PERIOD$>, Nope',
            u'<PRP>, Nope',
            u'<VB> PRP!, Nope',
            u'<VBZ> PRP!, Nope',
            #u'<VB|VBZ> PRP!, Nope',  
            u'<VB> DT!, Nope',
            #u'<DT NN>^^<DT NN>,Nope Nope2',
            #u'<.{test}>, Nope',
            u'<VB|VBZ> PRP|DT, Nope',
            u'VB{<Give>} PRP, VERB',
            u'<VB{<Give>}> <PRP>, COMMAND VERB NOUN',
            u'<DT? NNP|of*>, NERS'] 
            
   text_tagged = tag_string(text)
   pprint.pprint(text_tagged)
   
   for patt in patts[:8]: 
       
       run_tagmania_rule(text_tagged,patt) 
"""   
