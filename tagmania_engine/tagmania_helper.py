#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.tree import Tree
import re
from tagmania_constants import PUNCT
from tagmania_constants import WORDS_TO_BREAK

"""
Helper functions for tagmania 
"""

def check_syntax(rule):
    """
    check balanced parens, return false if not valid
    """
    ls = {'<', '(', '{'}
    rs = {'>', ')', '}'}
    rs_to_ls = {'>': '<', ')': '(', '}': '{'}
    delim_stack = []
    for char in rule:
        if char in ls:
            delim_stack.append(char)
        if char in rs:
            if not delim_stack or rs_to_ls[char] != delim_stack.pop():
                return False
    return not delim_stack

def package(index_matched, new_tag, to_tree):
    starting_index = index_matched[0][0]
    tups = [x for i,x in index_matched]

    if to_tree:
        new_tree = Tree(new_tag, tups)
        return (starting_index, new_tree)
    else:
        new_tuple = (starting_index,(u" ".join([tup[0] for tup in tups]),new_tag))
        return new_tuple

def reverse_punct(string):
    for new, old in PUNCT.items():
        string = string.replace(old, new)
    return string

def replace_contractions(string):
    if 'regexes' not in replace_contractions.__dict__:
        regexes = []
        for thing in WORDS_TO_BREAK:
            old, new = thing.split(',')
            replace_regex = re.compile(r'(?<!\w){}(?!\w)'.format(old))
            regexes.append((replace_regex, new))
        replace_contractions.regexes = regexes

    for replace_regex, new in replace_contractions.regexes:
        string = replace_regex.sub(new, string)

    return string
