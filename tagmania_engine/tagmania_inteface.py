from nltk.tree import Tree
from operator import itemgetter
import readline, os

def convert_to_tree(treething):
    if isinstance(treething, Tree):
        return Tree(treething.label(), convert_to_tree(treething[:]))
    if isinstance(treething, list):
        return map(convert_to_tree, treething)
    if isinstance(treething, tuple):
        assert len(treething) == 2
        return Tree(treething[1], [treething[0]])
    return treething


def print_list_of_tuple_trees(tt_list):
    Tree('Sentence', convert_to_tree(tt_list)).pretty_print()

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree('{}_{}'.format(node.orth_, node.tag_), [to_nltk_tree(child) for child in node.children])
    else:
        return '{}_{}'.format(node.orth_, node.tag_)

def print_dependency_tree(message):
    if 'nlp' not in print_dependency_tree.__dict__:
        import spacy
        print_dependency_tree.nlp = spacy.load('en')
    doc = print_dependency_tree.nlp(message)
    [to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]

def main_loop():
    ascii_art = r'''
      ___          ___          ___          ___          ___          ___          ___                   ___          ___
     /\  \        /\  \        /\  \        /\  \        /\__\        /\  \        /\__\        ___      /\  \        /\  \
     \:\  \      /::\  \      /::\  \      /::\  \      /::|  |      /::\  \      /::|  |      /\  \    /::\  \      /::\  \
      \:\  \    /:/\:\  \    /:/\:\  \    /:/\:\  \    /:|:|  |     /:/\:\  \    /:|:|  |      \:\  \  /:/\:\  \    /:/\:\  \
      /::\  \  /::\~\:\  \  /::\~\:\  \  /::\~\:\  \  /:/|:|__|__  /::\~\:\  \  /:/|:|  |__    /::\__\/::\~\:\  \  /:/  \:\  \
     /:/\:\__\/:/\:\ \:\__\/:/\:\ \:\__\/:/\:\ \:\__\/:/ |::::\__\/:/\:\ \:\__\/:/ |:| /\__\__/:/\/__/:/\:\ \:\__\/:/__/ \:\__\
    /:/  \/__/\/_|::\/:/  /\:\~\:\ \/__/\:\~\:\ \/__/\/__/~~/:/  /\/__\:\/:/  /\/__|:|/:/  /\/:/  /  \/__\:\/:/  /\:\  \  \/__/
   /:/  /        |:|::/  /  \:\ \:\__\   \:\ \:\__\        /:/  /      \::/  /     |:/:/  /\::/__/        \::/  /  \:\  \
   \/__/         |:|\/__/    \:\ \/__/    \:\ \/__/       /:/  /       /:/  /      |::/  /  \:\__\        /:/  /    \:\  \
                 |:|  |       \:\__\       \:\__\        /:/  /       /:/  /       /:/  /    \/__/       /:/  /      \:\__\
                  \|__|        \/__/        \/__/        \/__/        \/__/        \/__/                 \/__/        \/__/   '''
    print ascii_art
    print 'Type a sentence here.'
    print 'Type "tree" to switch to looking at the spacy dependency tree (default)'
    print 'Type "info" to switch to looking at the info extraction'
    print 'Type "exit" to quit.'
    current_function = print_dependency_tree
    while True:
        input_sentence = raw_input('--> ').strip()
        if input_sentence == 'exit':
            break

        if input_sentence == 'tree':
            if current_function == print_dependency_tree:
                print 'Already looking at spacy dependency parser tree.'
                continue
            test = raw_input('   Do you want to switch to looking at the spacy dependency parser tree? (y/n) ')
            if test in ('y', 'yes'):
                print 'Switching to dependency parser tree.'
                current_function = print_dependency_tree
            else:
                print 'Function remaining what it is now.'

        elif input_sentence == 'info':
            if current_function == print_info_extracted:
                print 'Already looking at info extraction.'
                continue
            test = raw_input('   Do you want to switch to looking at info extraction? (y/n) ')
            if test in ('y', 'yes'):
                print 'Switching to info extraction.'
                current_function = print_info_extracted
            else:
                print 'Function remaining what it is now.'

        elif input_sentence == 'clear':
             os.system('clear')
        else:
            input_sentence = unicode(input_sentence, encoding='utf-8')
            out = current_function(input_sentence)
            if out:
                print "apply rule set (set:<RULESET>), rule (rule:<RULE>), or new query? (query)" 

if __name__ == '__main__':
    main_loop()
