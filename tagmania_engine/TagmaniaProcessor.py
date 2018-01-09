#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import defaultdict
from operator import itemgetter

from itertools import chain
from nltk.tree import Tree

from tagmania_tree import get_tagmania_tree
from tagmania_constants import PUNCT
from tagmania_constants import constant_factory_dict
from tagmania_helper import check_syntax, package

# For debug
from pprint import pprint, pformat
def convert(t):
    if isinstance(t, Tree):
        return Tree(t.label(), convert(t[:]))
    if isinstance(t, list):
        return map(convert, t)
    if isinstance(t, tuple):
        return Tree(t[1], [t[0]])
    return t
def ptt(l):
    Tree('Sentence', convert(l)).pretty_print()

class TagmaniaProcessor:
    constant_dicts = {}
    trees = {}

    def __init__(self, rule=None, tree=None, rule_class='', verbose=False):
        """
        Parse the rule and get its tree (if tree=None), check its syntax, fetch any constants used in this rule class
            rule: str, the tagmania rule
            tree: dict, parsed tagmania rule
            rule_class: str, which type of rule this is (e.g. pos-tagging, post-np-pp-chunking, etc.)
        """
        self.verbose = verbose
        self.rule_class = rule_class

        assert rule or tree
        self.rule = rule
        if rule:
            if not check_syntax(rule):
                self.rule_class = 'BAD SYNTAX'
                return self
            if self.rule not in TagmaniaProcessor.trees:
                TagmaniaProcessor.trees[self.rule] = get_tagmania_tree(self.rule)
            self.tree = TagmaniaProcessor.trees[self.rule]
        elif tree:
            self.tree = tree

        if self.rule_class not in TagmaniaProcessor.constant_dicts:
            TagmaniaProcessor.constant_dicts[self.rule_class] = constant_factory_dict[self.rule_class]()
        self.constants = TagmaniaProcessor.constant_dicts[self.rule_class]
    
    def set_tuples(self, tuple_list):
        self.tuple_list = tuple_list[:]    
    def validate(self, tuple_list):
        """
        Try and match the rule once against input tuple list. Return bool.
        """
        if self.verbose:
            print 'Rule:',self.rule if self.rule else 'Lookinside'
        if self.rule_class == 'BAD SYNTAX':
            print 'BAD SYNTAX'
            return False
        self.tuple_list = tuple_list[:]
        valid = self.process_rule()[0]
        return valid 
    def transform(self, tuple_list):
        """
        Repeatedly match the rule against the tuple list until no more matches are found, then make replacements.
        """
        if self.verbose:
            print 'Rule:', self.rule if self.rule else 'Lookinside'
        if self.rule_class == 'BAD SYNTAX':
            print 'BAD SYNTAX'
            return False, tuple_list
        self.tuple_list = tuple_list[:]
        tup_index = 0
        self.modifications = {'to_add': [], 'to_delete': []}
        self.priority_mods = {'to_add': [], 'to_delete': []}
        self.valid = False
        while True:
            valid, modifications, priority_mods = self.process_rule(tup_index)
            self.valid |= valid
            if not valid:
                break
            self.add_to_mods(modifications, priority_mods)
            all_mods = list(chain(modifications['to_add'], modifications['to_delete'], priority_mods['to_add'], priority_mods['to_delete']))
            if not all_mods:
                break
            tup_index = max(i for i,x in all_mods)
            tup_index = int(round(tup_index)) + 1
        if self.valid:
            self.new_tuple_list = self.generate_new_tuple_list()
            if self.verbose and self.rule:
                print 'Rule:', self.rule
                print 'Original tuple list:'
                ptt(self.tuple_list)
                print 'Modifications:'
                pprint(self.modifications)
                print 'Priority (lookinside) modifications:'
                pprint(self.priority_mods)
                print 'New tuple list:'
                ptt(self.new_tuple_list)
        else:
            self.new_tuple_list = self.tuple_list
        return self.valid, self.modifications ,self.new_tuple_list

    def add_to_mods(self, modifications, priority_mods):
        self.modifications['to_add'] += modifications['to_add']
        self.modifications['to_delete'] += modifications['to_delete']
        self.priority_mods['to_add'] += priority_mods['to_add']
        self.priority_mods['to_delete'] += priority_mods['to_delete']

    def process_rule(self, tup_index=0):
        """
        Match rule once against the tuple list. tup_index specifies where to start from in the tuple_list
        """
        groups = self.tree['groups']

        self.tags = self.tree['tags'][:]
        grp_index = 0
        to_tree = self.rule_class != 'pos_tagging'
        modifications = {'to_add': [], 'to_delete': []}
        priority_mods = {'to_add': [], 'to_delete': []}
        valid = True
        while grp_index < len(groups) and tup_index < len(self.tuple_list):
            start = (tup_index == 0)
            end = (tup_index + 1 == len(self.tuple_list))
            group = groups[grp_index]
            if self.verbose:
                print 'Looking at grp_index: {}, tup_index: {}'.format(grp_index, tup_index)
                print 'Group: {}'.format(group)
            results = self.validate_group(group, tup_index)
            if self.verbose:
                print 'Results from validate_group for grp_index {}: {}'.format(grp_index, bool(results['matches']))
            matches = results['matches']
            open_paren_matches = results['open_paren_matches']
            lookinside_matches = results['lookinside_matches']
            new_tup_index = results['new_tup_index']
            if matches:
                for lookinside_match in lookinside_matches:
                    # lookinside matches must be applied first
                    priority_mods['to_delete'].append(lookinside_match['old'])
                    priority_mods['to_add'].append(lookinside_match['new'])
                if group['capture']:
                    tag = self.get_next_tag(matches)
                    packaged = package(matches, tag, to_tree)
                    modifications['to_add'].append(packaged)
                    modifications['to_delete'] += matches
                elif open_paren_matches:
                    to_add = [(i-0.2, ('[', tag)) for i,tag in zip(open_paren_matches, self.tags)]
                    self.tags = self.tags[len(open_paren_matches):]
                    modifications['to_add'] += to_add
                if group['operator'] != '*':
                    grp_index += 1
                tup_index = new_tup_index
            elif group['operator'] in ('?', '*'):
                grp_index += 1
            else:
                # If we get here, we have failed to match this group anywhere.
                modifications = {'to_add': [], 'to_delete': []}
                priority_mods = {'to_add': [], 'to_delete': []}
                valid = False
                break

        # If we hit the end of the tuple list before running out of groups,
        # check to see if every remaining group is either optional or consists
        # entirely of optional/negated individual patterns.
        if grp_index < len(groups):
            remaining_groups = groups[grp_index:]
            for group in remaining_groups:
                if group['operator'] == '?':
                    continue
                elif all(ind_patt['operator'] for ind_patt in group['individual_patterns']):
                    continue
                else:
                    modifications = {'to_add': [], 'to_delete': []}
                    priority_mods = {'to_add': [], 'to_delete': []}
                    valid = False
        return valid, modifications, priority_mods

    def get_next_tag(self, matches):
        tag = self.tags.pop(0)
        ref_tuple = None
        if tag == 'GET_FIRST_TAG':
            ref_tuple = matches[-1][1]
        """
        elif tag == 'GET_LAST_TAG':    
            ref_tuple = matches[-1][0]
        
            if hasattr(first, 'label'):
                tag = first.label()
            else:
                tag = first[1]
        """
        return tag

    def validate_group(self, group, tup_index):
        """
        Inputs: group: dict,
                tup_index, integer between 0 and len(tuple_list)-1
        Returns: dictionary, with keys:
            matches: list of indices corresponding to the elements of tup_index
                that match this group. Empty list if no match found.
            open_paren_matches: same as matches but for open clauses
            lookinside_matches: list of dicts {'old':..., 'new':...}
                corresponding to any chunks recursively transformed during the
                course of validating this group.
            new_tup_index: int, last index of tuple_list that produced a match
        """
        matches = []
        open_paren_matches = []
        lookinside_matches = []
        starting_tup_index = tup_index
        ip_index = 0
        while ip_index < len(group['individual_patterns']) and tup_index < len(self.tuple_list):
            start = (tup_index == 0)
            end = (tup_index + 1 == len(self.tuple_list))
            ind_patt, tup = group['individual_patterns'][ip_index], self.tuple_list[tup_index]
            valid, new_tup = self.validate_individual_pattern(ind_patt, tup, start=start, end=end, grp_capture=group['capture'])
            # Evaluate operator
            if not valid and ind_patt['operator'] in ('?', '*'):
                ip_index += 1
                continue
            if ind_patt['operator'] == '!':
                valid = not valid
            if valid:
                if new_tup != tup:
                    lookinside_matches.append({'old': (tup_index, tup), 'new': (tup_index, new_tup)})
                    matches.append((tup_index, new_tup))
                else:
                    matches.append((tup_index, tup))
                if ind_patt['open_paren']:
                    open_paren_matches.append(tup_index)
                if ind_patt['operator'] != '*':
                    ip_index += 1
                tup_index += 1
            else:
                if ind_patt['delimiter'] == '^^':
                    matches.append((tup_index, tup))
                    tup_index += 1
                    continue
                else:
                    # We have failed to find a group match at this starting index.
                    if group['delimiter'] == ' ':
                        return {'matches': [], 'open_paren_matches': [], 'lookinside_matches': [], 'new_tup_index': starting_tup_index}
                    matches = []
                    open_paren_matches = []
                    starting_tup_index += 1
                    tup_index = starting_tup_index
                    ip_index = 0

        fail = {'matches': [],
                'open_paren_matches': [],
                'lookinside_matches': [],
                'new_tup_index': starting_tup_index}

        if matches == [] or ip_index != len(group['individual_patterns']):
            return fail
        if group['caret'] and matches[0][0] != 0:
            return fail
        if group['dollar'] and matches[-1][0] != len(self.tuple_list) - 1:
            return fail

        return {'matches': matches,
                'open_paren_matches': open_paren_matches,
                'lookinside_matches': lookinside_matches,
                'new_tup_index': tup_index}

    def validate_individual_pattern(self, ind_patt, tup, start, end, grp_capture):
        """
        Matches individual pattern against given tup. If found lookinside, processes it.
        """
        if ind_patt['caret'] and not start:
            return False, tup
        if ind_patt['dollar'] and not end:
            return False, tup

        valid = self.check_words(ind_patt['words'], tup)
        if ind_patt['lookinside'] and valid:
            valid, new_tup = self.transform_lookinside(ind_patt['lookinside'], tup, grp_capture)
        else:
            new_tup = tup

        return valid, new_tup

    def transform_lookinside(self, lookinside, tup, grp_capture):
        """
        Recursively applies TagmaniaProcessor.transform to lookinside
        """
        is_tree = hasattr(tup, 'label')
        if is_tree:
            tuple_list = tup[:]
        else:
            tuple_list = [tup]

        if grp_capture:
            first_tag = self.tags.pop(0)

        sub_tree = {'groups': lookinside, 'tags': self.tags}
        sub_processor = TagmaniaProcessor(tree=sub_tree, rule_class=self.rule_class)
        valid, new_tuple_list = sub_processor.transform(tuple_list)
        if valid:
            num_tags = sub_processor.count_capture_groups()
            self.tags = self.tags[num_tags:]

        if grp_capture:
            self.tags.insert(0, first_tag)

        if is_tree:
            new_tup = Tree(tup.label(), new_tuple_list)
        else:
            new_tup = new_tuple_list[0]
        return valid, new_tup

    def check_words(self, words, tup):
        """
        compare an input list of tags or words to the tuple or a chunk

        input: list_of_strings, tuple
        output: boolean
        """
        if '.' in words:
            return True

        if hasattr(tup, 'label'):
            return tup.label() in words

        content, tag = tup

        for string in words:
            if string in self.constants and content.lower() in self.constants[string]:
                return True

            if string in PUNCT and content == PUNCT[string]:
                return True
            if string == 'PUNCT' and content in PUNCT.values():
                return True

            if string[0].isupper() and tag == string:
                return True
            elif string.lower() in content.lower().split():
                return True
        return False

    def generate_new_tuple_list(self):
        """
        generate new tuple list, given all modifications.
        """
        priority_to_add = iter(self.priority_mods['to_add'])
        priority_minus_deleted = (x for x in enumerate(self.tuple_list) if x not in self.priority_mods['to_delete'])
        new_tuple_list = list(chain(priority_to_add, priority_minus_deleted))

        to_add = iter(self.modifications['to_add'])
        minus_deleted = (x for x in new_tuple_list if x not in self.modifications['to_delete'])
        new_tuple_list = list(chain(to_add, minus_deleted))

        new_tuple_list.sort(key=itemgetter(0))
        return [x for i,x in new_tuple_list]

    def count_capture_groups(self):
        """Returns the number of capture groups in the search pattern"""
        return len([g for g in self.tree['groups'] if g['capture']])
