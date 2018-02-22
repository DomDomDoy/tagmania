# Tagmania

Tagmania is a mini-language designed for matching or transforming lists consisting of tuples or NLTK trees (henceforth 'chunks'). The transformations tagmania can peform are the following:
 - Replacing the tag of a chunk with a specified tag;
 - Putting several chunks under one chunk with a specified tag;
 
### The data

Before we continue, here is a description of the data we are transforming. Abstractly, we are looking at part-of-speech-tagged sentences, parse trees of sentences, and various stages in between. More concretely, what this means is that we have a list of chunks, where a chunk is defined recursively as follows:
 - A tuple in the form `(word, tag)`, or:
 - An nltk.tree.Tree object of the form `Tree(tag, [chunk1, chunk2, ..., chunkn])`

### Matching

In order to perform the transforms, tagmania must match particular chunks. Here are the matching features supported by tagmania:
 1. Matching any chunk (using the period `.`)
 2. Matching a chunk at the very beginning or end of a list (using the standard caret `^` and dollar `$` operators)
 3. Matching chunks that immediately follow one another (by separating them with spaces)
 4. Matching chunks that do not necessarily immediately follow one another, but that occur in sequence (by separating them with the double caret `^^`)
 5. Matching a chunk by specifying a set of words or tags that the chunk must contain one of (by separating the words or tags with pipes `|`)
 6. Optionally matching a chunk (using the question mark `?`)
 7. Matching anything other than the specified chunk (using the exclamation mark `!`)
 8. Matching a chunk zero or more times (using the kleene star `*`)
 9. Matching a chunk one or more times (using `+`)
 10. Matching a chunk by recursively matching its children (using the braces `{`, `}`) 



An example is the following:

```PATIENT VP{am|is|are|was|were|be|been|being VBN RP?} <ADVERBIAL{^by}>,AGENT```

In this rule, every group consists of only one individual pattern, and hence no non-capturing brackets are needed.

- The first group `PATIENT` denotes a chunk with the tag PATIENT
- The second group `VP{am|is|are|was|were|be|been|being VBN RP?}` denotes a chunk with tag VP, within which:
     - there should be a sub-chunk whose word is one of am, is, are, was, were, be, been, being
     - this sub-chunk should be followed by a sub-chunk whose tag is VBN
     - this sub-chunk can optionally be followed by a chunk whose tag is RP
- The third group `<ADVERBIAL{^by}>` is a capturing group, and denotes a chunk whose tag is ADVERBIAL and:
     - either the chunk's word is 'by', or:
     - within the chunk, the first sub-chunk has the word 'by'
- The tag is AGENT, which means one of two things, depending on tagmania's mode:
     - if tagmania is in POS-tagging mode, it will change the tag of the captured chunk from ADVERBIAL to AGENT
     - if tagmania is in chunking mode, it will replace the captured chunk with a new chunk whose tag is AGENT and whose sole child chunk is the captured chunk




### Rule structure

A tagmania rule consists of a search pattern, followed by a comma, followed by some tags or tag macros*.

The search pattern is broken up into groups, which are either capturing (marked for tag replacement or gathering under a new chunk) or non-capturing. The groups are separated by delimiters, i.e. either a space (` `) or a double caret (`^^`)

Each group consists of delimiter-separated individual patterns, which are intended to match or not match exactly one chunk. A group also may feature an operator (`!`, `?` or `*`, at the end), anchors (either `^` at the beginning or `$` at the end), and brackets (parentheses for non-capturing groups, angle brackets for capturing groups).

Each individual pattern consists of the words or tags to match (`.`, a word, or several words separated by pipes), and optionally a lookinside, which is an entire search pattern enclosed in braces meant to be recursively applied to the contents of one chunk. The individual patterns can also feature an operator and anchors.

### Declaring variables

Imagine you would like to search for a list of words, but within the framework of tagmania. I.e. Instead of writing 

<summer|winter|spring|fall|autumn>,SEASON 

you could just write SEASON,without running this rule. 


Steps

1) create csv file called SEASON.csv 
2) place file under tagmania_constants  
3) now in __init__.py in the tagmania_constants directory , add the following lines: 

```
constant_varnames['ref_name_here'] = ['SEASONS'] 
```

then add the following function: 

```
def load_ref_name_here_constants():
    return {var_name: load_const(var_name) for var_name in constant_varnames['ref_name_here']}
```

and then finally 

```
constant_factory_dict['ref_name_here'] = load_ref_name_here_constants
```

```
TagmaniaProcessor(rule_class'ref_name_here')
```


### Adding rule sets 

A rule set is a file consisiting of  a list of tagmania rules  

To add a new rule set, i.e. rule_set1 , in the "rules" directory, open __init__.py
and add the following line.

```
rule_files = ['rule_set1']
```


### Tag Macros

GET_FIRST_TAG: 
changes the tags of the capture group to the first tag in the capture group

i.e. 
<. NN>,GET_FIRST_TAG

### Example

All examples can be found in (tagmania_examples.py)
 

The bill passed 81-18. Sixteen Democrats and two libertarian-minded Republicans voted against it. Among them were a number of potential Democratic presidential candidates in 2020 including Cory Booker, Kirsten Gillibrand, Kamala Harris, Bernie Sanders and Elizabeth Warren.


pos_tagged by spacey:

```

[(u'81-', u'PERCENT'),
 (u'Sixteen', u'CARDINAL'),
 (u'Democrats', u'NORP'),
 (u'two', u'CARDINAL'),
 (u'Republicans', u'NORP'),
 (u'Democratic', u'NORP'),
 (u'2020', u'DATE'),
 (u'Cory Booker', u'PERSON'),
 (u'Kirsten Gillibrand', u'PERSON'),
 (u'Kamala Harris', u'PERSON'),
 (u'Bernie Sanders', u'ORG'),
 (u'Elizabeth Warren', u'PERSON')]


 [(u'The', u'DT'),
 (u'bill', u'NN'),
 (u'passed', u'VBD'),
 (u'81', u'CD'),
 (u'-', u'SYM'),
 (u'18', u'CD'),
 (u'.', u'.'),
 (u'Sixteen', u'CD'),
 (u'Democrats', u'NNPS'),
 (u'and', u'CC'),
 (u'two', u'CD'),
 (u'libertarian', u'JJ'),
 (u'-', u'HYPH'),
 (u'minded', u'JJ'),
 (u'Republicans', u'NNPS'),
 (u'voted', u'VBD'),
 (u'against', u'IN'),
 (u'it', u'PRP'),
 (u'.', u'.'),
 (u'Among', u'IN'),
 (u'them', u'PRP'),
 (u'were', u'VBD'),
 (u'a', u'DT'),
 (u'number', u'NN'),
 (u'of', u'IN'),
 (u'potential', u'JJ'),
 (u'Democratic', u'JJ'),
 (u'presidential', u'JJ'),
 (u'candidates', u'NNS'),
 (u'in', u'IN'),
 (u'2020', u'CD'),
 (u'including', u'VBG'),
 (u'Cory', u'NNP'),
 (u'Booker', u'NNP'),
 (u',', u','),
 (u'Kirsten', u'NNP'),
 (u'Gillibrand', u'NNP'),
 (u',', u','),
 (u'Kamala', u'NNP'),
 (u'Harris', u'NNP'),
 (u',', u','),
 (u'Bernie', u'NNP'),
 (u'Sanders', u'NNP'),
 (u'and', u'CC'),
 (u'Elizabeth', u'NNP'),
 (u'Warren', u'NNP'),
 (u'.', u'.')]

```

Take:

```
...
 (u'81', u'CD'),
 (u'-', u'SYM'),
 (u'18', u'CD'),
 ... 
	
```	
Let's say I wanted to consider CD SYM CD as simply a CD , then I would write a rule as such: 

```

<CD SYM CD>, CD 

```

out:
```
...
Tree('CD', [(u'81', u'CD'), (u'-', u'SYM'), (u'18', u'CD')]),
...
```
or 

let's say you trust the people that the spacey NER spits out , tags, and insert them into the tags, as such: 

```
pers =  [(u'Cory Booker', u'PERSON'),
 (u'Kirsten Gillibrand', u'PERSON'),
 (u'Kamala Harris', u'PERSON'),
 (u'Bernie Sanders', u'ORG'),
 (u'Elizabeth Warren', u'PERSON')]

```

so after getting the NER of names from spacey, 
we can insert them into 

```

for text,tag in pers:
	<text>,PERSON
```
Now imagine, we want to be able to group PERSONS and call them a PERSON_LISTING  

<(PERSON COMMA PERSON)+>,PERSON_LISTING  


taking a look at the output of our rule set we get the following: 
```
... 
 (u'in', u'IN'),
 (u'2020', u'CD'),
 (u'including', u'VBG'),
 Tree('PERSON_LISTING', [Tree('PERSON', [(u'Cory', u'NNP'), (u'Booker', u'NNP')]), (u',', u','), Tree('PERSON', [(u'Kirsten', u'NNP'), (u'Gillibrand', u'NNP')]), (u',', u','), Tree('PERSON', [(u'Kamala', u'NNP'), (u'Harris', u'NNP')]), (u',', u',')]),
 (u'Bernie', u'NNP'),
 (u'Sanders', u'NNP'),
 (u'and', u'CC'),
 Tree('PERSON', [(u'Elizabeth', u'NNP'), (u'Warren', u'NNP')]),

```



It looks like as if now, Bernie sanders wasn't considered as a Person and left behind as a NNP!. Well with the following tagmania rule we can fix that....   
```

PERSON PERSON|COMMA+ <NNP+> and PERSON,PERSON
```
Now that Bernie Sanders , is a Person 
```
Tree('PERSON', [(u'Bernie', u'NNP'), (u'Sanders', u'NNP')])
```
Let's group these people into an abstract notion called PERSON_LISTING 

```
<PERSON COMMA|PERSON+ and PERSON>,PERSON_LISTING
```
once you run that rule you get the following output...

```
..... 	
 (u'number', u'NN'),
 (u'of', u'IN'),
 (u'potential', u'JJ'),
 (u'Democratic', u'JJ'),
 (u'presidential', u'JJ'),
 (u'candidates', u'NNS'),
 (u'in', u'IN'),
 (u'2020', u'CD'),
 (u'including', u'VBG'),
 Tree('PERSON_LISTING', [Tree('PERSON', [(u'Cory', u'NNP'), (u'Booker', u'NNP')]), (u',', u','), Tree('PERSON', [(u'Kirsten', u'NNP'), (u'Gillibrand', u'NNP')]), (u',', u','), Tree('PERSON', [(u'Kamala', u'NNP'), (u'Harris', u'NNP')]), (u',', u','), Tree('PERSON', [(u'Bernie', u'NNP'), (u'Sanders', u'NNP')]), (u'and', u'CC'), Tree('PERSON', [(u'Elizabeth', u'NNP'), (u'Warren', u'NNP')])])]

```

Which allows for very easy tokenizing.


we have currently decided on using the nltk tree structure, because it does inherit from python's list data type  which can be useful. In addition, we tried to build something more hopeful than the rule based matching in nltk, where one can search using both tags/words in a way that is tailored and understandable to linguists. When you don't have time to train a new language model and want to save some time on annontation, or do some research into what types of linguistic phenomenon occurs in text, this could be good library to try out.



Example 2:

Let's think of another use case where tagmania could be useful. Let's take, for example the difficult problem of identifying agent and action in a sentence with a relative clause. If you take a look in relative_clauses.txt, you will find in the following sentences:

I'm looking for a secretary who can use a computer well.
She has a son that is a doctor.
We bought a house which is 200 years old.
I sent a letter which arrived three weeks later.
The people that live on the island are very friendly.
The man who phoned is my brother.
The camera which costs £100 is over there.
The house that belongs to Julie is in London. 


.... So using the following rules, 

```
<I|she|he|we|you|they>,Pronoun
<DT JJ? NN|NNP|NNS>,Object
<^Pronoun|Object>,Subject
<is|was|were|are|am VBG>,Gerund
Subject that|who|which <Gerund|VBZ|VBP|VBD>^^<VBZ|VBP|VBD>,VP ACTION  
Subject <Gerund|VBZ|VBP|VBD>, ACTION 
```
I can start to write rules based on linguistic phenomenon , to manipulate the tags accordingly. 
as seen. 

i.e. 
In:

```
[(u'The', u'DT'),
 (u'man', u'NN'),
 (u'who', u'WP'),
 (u'phoned', u'VBD'),
 (u'is', u'VBZ'),
 (u'my', u'PRP$'),
 (u'brother', u'NN'),
 (u'.', u'.')]
```
Out:
```
[Tree('Subject', [Tree('Object', [(u'The', u'DT'), (u'man', u'NN')])]),
 (u'who', u'WP'),
 Tree('VP', [(u'phoned', u'VBD')]),
 Tree('ACTION', [(u'is', u'VBZ')]),
 (u'my', u'PRP$'),
 (u'brother', u'NN'),
 (u'.', u'.')]
```	
applied rules
```
[u'<DT JJ? NN|NNP|NNS>,Object',
 u'<^Pronoun|Object>,Subject',
 u'Subject that|who|which <Gerund|VBZ|VBP|VBD>^^<VBZ|VBP|VBD>,VP ACTION']
```
 
(to see full output, run tagmania_examples in /tests or see examples_out.txt)  

So that is the idea, by uploading rules , and tweaking them , one can manipulate pos-tags and use their information, position to extract information that might be important for annotation, or understanding text in general. 


Tagmania is very much still in production and the rule processing needs some work. and that is why I humbly am asking anyone interested to contribute. I believe in Tagmania and that it should bring linguists closer together. I wanted to release this very first version to get the juices flowing, (both cranal and alcoholic/non-alcoholic beverages) which by the way you can support, by donating here!


 

### Dependencies 
nltk,spacy,cytoolz,parsimonious

