from parsimonious.grammar import Grammar
from collections import deque
from itertools import izip, chain

grammar = Grammar(
        r"""
        rule = search_pattern comma space? tags
        search_pattern = group (delimiter group)*
        group = ((open_capture group_pattern '>') / ( caret? '('  group_pattern ')' dollar? operator?) / individual_pattern)
        operator = ex_mark / qu_mark / star / plus
        group_pattern = individual_pattern ( delimiter individual_pattern )*
        individual_pattern = open_paren? caret? (word_pattern lookinside?) dollar? operator?
        word_pattern = ( word ) ( pipe word )*
        lookinside = '{' search_pattern '}'
        word = ~"[\w_0-9-/]+" / '.' / '\\[' / '\\]'
        qu_mark = '?'
        star = '*'
        plus = '+'
        caret = '^'
        dollar = '$'
        delimiter = '^^' / ' '
        comma = ','
        semicolon = ';'
        dash = '-'
        slash = '/'
        space = ' '
        tags = word (space word)*
        pipe = '|'
        ex_mark = '!'
        open_paren = '['
        open_capture = '<'
        """)

def get_tagmania_tree(rule):
    root_node = grammar.parse(rule)
    search_pattern_node = find(root_node, 'search_pattern', give_me='node')
    tags_node = find(root_node, 'tags', give_me='node')
    return {'groups': visit_search_pattern(search_pattern_node),
            'tags': [n.text for n in search(tags_node, 'word')]
            }

def visit_search_pattern(node):
    groups = []
    delim_nodes = search(node, 'delimiter', stop_tags={'group'})
    delimiters = chain([None], (n.text for n in delim_nodes))

    group_nodes = search(node, 'group')
    for delim, group_node in izip(delimiters, group_nodes):
        group = visit_group(group_node)
        group['delimiter'] = delim
        groups.append(group)
    return groups

def visit_group(node):
    st = {'group_pattern'}
    capture = find(node, 'open_capture', stop_tags=st)
    caret = find(node, 'caret', stop_tags=st)
    dollar = find(node, 'dollar', stop_tags=st)
    operator = find(node, 'operator', stop_tags=st, give_me='text')

    delim_nodes = search(node, 'delimiter', stop_tags={'lookinside'})
    delims = chain([None], (n.text for n in delim_nodes))

    ind_patt_nodes = search(node, 'individual_pattern')
    individual_patterns = []
    
    for delim, ind_patt_node in izip(delims, ind_patt_nodes):
        ind_patt = visit_individual_pattern(ind_patt_node)
        ind_patt['delimiter'] = delim
        individual_patterns.append(ind_patt)
    return {'caret': caret,
            'dollar': dollar,
            'capture': capture,
            'operator': operator,
            'individual_patterns': individual_patterns}

def visit_individual_pattern(node):
    st = {'lookinside'}
    open_paren = find(node, 'open_paren', stop_tags=st)
    caret = find(node, 'caret', stop_tags=st)
    dollar = find(node, 'dollar', stop_tags=st)
    operator = find(node, 'operator', stop_tags=st, give_me='text')

    word_nodes = search(node, 'word', stop_tags=st)
    words = [w.text for w in word_nodes]

    lookinside_node = find(node, 'lookinside', give_me='node')
    if lookinside_node:
        lookinside = visit_search_pattern(lookinside_node)
    else:
        lookinside = None

    return {'open_paren': open_paren,
            'caret': caret,
            'dollar': dollar,
            'operator': operator,
            'words': words,
            'lookinside': lookinside}

def find(node, tag, stop_tags=None, give_me='bool'):
    """
    Like search, but with 2 key differences:
    a) only returns one result
    b) returns either the result's text or just a bool saying whether we found it or not
    """
    found_iter = search(node, tag, stop_tags, stop_after_one=True)
    found = next(found_iter, None)
    if give_me == 'bool':
        return bool(found)
    elif give_me == 'text':
        return found.text if found else None
    elif give_me == 'node':
        return found

def search(start_node, tag, stop_tags=None, stop_after_one=False):
    """
    Performs a depth-first search of the tree starting from node, looking for nodes tagged as tag.
    Stop when we reach any of  stop_tags (default: {tag}).
    Stop after (stop_after:int) matched nodes.
    """
    result = []
    if stop_tags is None:
        stop_tags = {tag}
    nodes = deque([start_node])
    while nodes:
        node = nodes.popleft()
        if node.expr_name == tag:
            yield node
            if stop_after_one:
                break
        if node.expr_name not in stop_tags:
            nodes.extend(node.children)
