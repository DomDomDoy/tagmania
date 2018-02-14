import re
import itertools
from rules import rule_dict
from tagmania_constants import PUNCT, constant_varnames

class RulesTree:
    def __init__(self, data=None, children=None):
        self.data = data if data else set()
        self.children = children if children else dict()

    def add_child(self, edge_label, node):
        self.children[edge_label] = node

punctuation = {v:k for k,v in PUNCT.iteritems()}

def remove_look_insides(rule):
    while True:
        index = rule.rfind('{')
        if index == -1:
            return rule
        end = rule.find('}', index) + 1
        if end == -1:
            raise Exception('Badly nested brackets')
        rule = rule[:index] + rule[end:]

def cond_lower_case(thing):
    upper_words = set(punctuation.values())
    upper_words.add('PUNCT')
    if isinstance(thing, basestring):
        return thing if thing in upper_words else thing.lower()
    else:
        return map(cond_lower_case, thing)

def get_paths(rule, variables):
    if 'regex' not in get_paths.__dict__:
        get_paths.regex = re.compile(r' |\^\^')

    if any(vari in rule for vari in variables):
        return [[]]

    rule = rule.split(',', 1)[0]
    rule = rule.replace('<', '').replace('>', '').replace('[', '').replace(']', '').strip('^$')
    rule = remove_look_insides(rule)
    first_path = [x for x in get_paths.regex.split(rule) if all(char.isalpha() or char in ['|', '_'] for char in x)]
    paths = [first_path[:]]

    for i, word in enumerate(first_path):
        if '|' in word:
            new_paths = []
            parts = word.split('|')
            for path in paths:
                new_paths += [path[:i] + [part] + path[i+1:] for part in parts]
            paths = new_paths
    paths = [set(path) for path in paths]
    new_paths = []
    for path in paths:
        if not any(other < path for other in paths):
            to_append = sorted(list(path))
            new_paths.append(to_append)
    return new_paths

def add_stuff(path, index, node):
    if not path:
        node.data.add(index)
        return
    word = path.pop()
    if word not in node.children:
        node.add_child(word, RulesTree())
    child = node.children[word]
    add_stuff(path, index, child)

def tuple_list_to_tree(rule_list, variables):
    tree_list = [get_paths(rule, variables) for rule in rule_list]
    tree_list = cond_lower_case(tree_list)

    node = RulesTree()
    for index, pathlist in enumerate(tree_list):
        for path in pathlist:
            add_stuff(path, index, node)
    return node

def get_words(input_thing):
    if type(input_thing) in (str, unicode):
        if input_thing in punctuation:
            return {input_thing, punctuation[input_thing], 'PUNCT'}
        return {input_thing.lower()}
    if type(input_thing) is tuple:
        iterate_get_words = (get_words(thing) for thing in input_thing)
        return set(itertools.chain(*iterate_get_words))
    if type(input_thing) is list:
        return set().union(*map(get_words, input_thing))
    if 'label' in dir(input_thing):
        result = get_words(input_thing[:])
        result.add(input_thing.label().lower())
        return result
    raise Exception('Not string, list, nltk.Tree or tuple')

def traverse_tree(node, word_set):
    indices = set()
    indices.update(node.data)
    relevant_edge_labels = set(node.children.keys()) & word_set
    for edge_label in relevant_edge_labels:
        child = node.children[edge_label]
        indices.update(traverse_tree(child, word_set))
    return indices

def get_new_tags(rule):
    tags = rule.lower().split(',',1)[1]
    return tags.split()

def item_zip(dict1, dict2):
    for key in dict1:
        yield (key, dict1[key], dict2[key])

def get_rules(name, input_list):
    if 'trees' not in get_rules.__dict__:
        get_rules.trees = {k:tuple_list_to_tree(r, c) for k,r,c in item_zip(rule_dict, constant_varnames)}
    if 'tags_dict' not in get_rules.__dict__:
        get_rules.tags_dict = {k: map(get_new_tags, r) for k,r in rule_dict.iteritems()}
    
    
    
    rule_list = rule_dict[name]
    root = get_rules.trees[name]
    tags = get_rules.tags_dict[name]
    input_words = get_words(input_list)

    indices = {0} # Since the first rule always changes a Tree to a list (where applicable), the safest thing to do is to include it
    while True:
        new_indices = traverse_tree(root, input_words)
        extra_indices = new_indices - indices
        indices = new_indices
        if not extra_indices:
            break
        input_words.update(*(tags[i] for i in extra_indices))

    indices = list(indices)
    indices.sort()
    return [rule_list[i] for i in indices]
