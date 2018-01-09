#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys
sys.path.append('../../')
from utils import load
from functools import partial
directory = 'tagmania/tagmania_engine/tagmania_constants'
load_const =  partial(load, directory)

PUNCT = {'PERIOD':'.', 
    'QUESTIONMARK':'?', 
    'EXCLAMATIONMARK':'!', 
    'ELLIPSIS':'...', 
    'COLON':':', 
    'COMMA':',', 
    'DASH':'-', 
    'SEMICOLON':';', 
    'HYPHEN':'--', 
    'SLASH':'/', 
    'QUOTATION':'\"', 
    'APOSTROPHE':'\'', 
    'LEFTPARENTHESES':'(', 
    'RIGHTPARENTHESES':')',
    'AMPERSAND':'&'}

PARTICLE_MAPPINGS = {
    'ObjectS_clause': 'OBJECT', 
    'OC': 'OBJECT', 
    'PrepositionS_clause': 'OBJECT', 
    'RelativeS_clause': 'MODIFIER',
    'RC': 'MODIFIER', 
    'CausalS_clause': 'CAUSE', 
    'TemporalS_clause': 'TIME', 
    'ConcessiveS_clause': 'CONCESSION',
    'ConsecutiveS_clause': 'CONSECUTIVE', 
    'FinalS_clause': 'GOAL', 
    'ConditionalS_clause': 'CONDITION',
    'LocativeS_clause': 'PLACE', 
    'QuantityS_clause': 'QUANTITY', 
    'MannerS_clause': 'MANNER', 
    'ADVERBIAL': 'ADVERBIAL'}

#ALLOWED_CHUNK_TAGS = load_const('ALLOWED_CHUNK_TAGS')
#ALLOWED_POS_TAGS = load_const('ALLOWED_POS_TAGS')
WORDS_TO_BREAK = load_const('WORDS_TO_BREAK')


# constant loading functions

constant_varnames = defaultdict(list)
constant_varnames['geo_toks'] = ['GENERIC_MEET_VERBS', 'LOCATIVE_ADVERBS', 'LOCATIVE_PREPOSITIONS', 'LOCATIVE_PREPOSITIONS_WITHOUT_TO',
        'MEET_NOUNS', 'MEET_VERBS', 'NP_LOCATIVE_VERBS', 'PLACE_NAMES', 'PLACES']
constant_varnames['clause_opening'] = ['V1', 'V2', 'V3']
constant_varnames['date_time'] = ['NUM']
def load_geo_constants():
    return {var_name: load_const(var_name) for var_name in constant_varnames['geo_toks']}

def load_clause_constants():
    return {var_name: load_const(var_name) for var_name in constant_varnames['clause_opening']}

def load_date_time_constants():
    return {var_name: load_const(var_name) for var_name in constant_varnames['date_time']}

constant_factory_dict = defaultdict(lambda: dict)
constant_factory_dict['clause_opening'] = load_clause_constants
constant_factory_dict['geo_toks'] = load_geo_constants
constant_factory_dict['date_time'] = load_date_time_constants
