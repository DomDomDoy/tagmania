# Tagmania: A Non-technical Overview

Tagmania is a library designed for linguists to manipulate part of speech tags. So there may be a couple questions you are asking yourself such as: 

what are part-of-speech tags?  
why is this important?

In the field of Natural Language Processing , a field where the main focus is writing programs that understand language, one very important tool is a POS Tagger, or Part of Speech Tagger. Part of Speech Taggers refer ususally to taking an input text and outputting the input text with it's pos-tags. 


Here is an example:

``` 
Input Sentence: Today we are learning about part of speech taggers! 
Output: Today|NOUN we|NOUN are|VERB learning|VERB about|ADP part|NOUN of|ADP speech|NOUN taggers|NOUN !|PUNCT

``` 

This example was taken from an open source NLP library called Spacey. If you want to try your own example, please visit the following website: [Online Text Analysis](http://textanalysisonline.com/spacy-pos-tagging)

Part of speech tags add another layer of information to text, making it come to life. There are ; however, some issues surrounding the use of this information reliabily in application development. One example of this is being able to search these two layers of information (text,pos-tag) interchangably. Another issue, focuses on increasing the already high accuracy of pos-tags. 


So what is Tagmania and how does it tackle these issues? 

Tagmania tackles these issues allowing users (usually linguists) to write rules. For examples of rules, see section
 ***Some more concrete examples*** below. 


# Tagmania: A Technical Overview


Tagmania can be defined as a mini-language designed for matching or transforming lists consisting of tuples or NLTK trees (henceforth 'chunks'). The transformations tagmania can peform are the following:
 - Replacing the tag of a chunk with a specified tag;
 - Putting several chunks under one chunk with a specified tag; 



### Input

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




### Rule Structure

A tagmania rule consists of a search pattern, followed by a comma, followed by some tags or tag macros*.

The search pattern is broken up into groups, which are either capturing (marked for tag replacement or gathering under a new chunk) or non-capturing. The groups are separated by delimiters, i.e. either a space (` `) or a double caret (`^^`)

Each group consists of delimiter-separated individual patterns, which are intended to match or not match exactly one chunk. A group also may feature an operator (`!`, `?` or `*`, at the end), anchors (either `^` at the beginning or `$` at the end), and brackets (parentheses for non-capturing groups, angle brackets for capturing groups).

Each individual pattern consists of the words or tags to match (`.`, a word, or several words separated by pipes), and optionally a lookinside, which is an entire search pattern enclosed in braces meant to be recursively applied to the contents of one chunk. The individual patterns can also feature an operator and anchors.





# How To





## Getting Started
```

git clone https://github.com/DomDomDoy/tagmania.git 
pip install -r requirements.txt
```

## How To Run A Single Rule
```
from tagmania.tagmania_engine import TagmaniaProcessor 

test_rule = u'<this is a test>,TEST'
tagged = [(u'this', u'DT'), (u'is', u'VBZ'), (u'a', u'DT'), (u'test', u'NN')] 

processor = TagmaniaProcessor(test_rule)
valid, mods, transformed_input = processor.transform(tagged)

Out:
[Tree('TEST', [(u'this', u'DT'), (u'is', u'VBZ'), (u'a', u'DT'), (u'test', u'NN')])]

```

Tagmania is pos-tag agnostic, so any input is a list of tuples and nltk Trees regardless of the pos-tags used, whether it be [Penn State Tree Bank](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html) or a different set of tags. 


## Running The Tests

To run pytests, go to tests/ and run the following command

```
pytest -v -m basic tagmania_tests.py

```

to generate the pytest parameters run (look in main in tagmania_tests for more details)

```
python tagmania_tests.py

```

### Break Down The Tests 
These tests are meant to check if tagmania's engine is working correctly.

```
=========================================================================================== test session starts ============================================================================================
platform linux2 -- Python 2.7.12, pytest-3.2.3, py-1.4.34, pluggy-0.4.0 -- /usr/bin/python

collected 14 items                                                                                                                                                                                         
tagmania_tests.py::test_search_engine[<DT NN>,Nope] PASSED
tagmania_tests.py::test_search_engine[<^VB PRP>,Nope] PASSED
tagmania_tests.py::test_search_engine[<PERIOD$>,Nope] PASSED
tagmania_tests.py::test_search_engine[<VB|VBZ> PRP|DT,Nope] PASSED
tagmania_tests.py::test_search_engine[<VB> DT!,Nope] PASSED
tagmania_tests.py::test_search_engine[<VP{was}>,Nope] PASSED
tagmania_tests.py::test_search_engine[VP{was}^^<PLACE$>,Tag1] PASSED
tagmania_tests.py::test_search_engine[<VB> PRP!,Nope] xfail
tagmania_tests.py::test_search_engine[<a NN|of*>, NER] PASSED
tagmania_tests.py::test_search_engine[<she VP+>, PRONOUN_COPULA] xfail
tagmania_tests.py::test_search_engine[<he VP+>, PRONOUN_COPULA] PASSED
tagmania_tests.py::test_search_engine[<he> <VP{was}>,PRONOUN COPULA] PASSED
tagmania_tests.py::test_search_engine[he <VP{<was>}>,VERB_COPULA COPULA] PASSED
tagmania_tests.py::test_search_engine[<he> <VP{<was>}>,PRONOUN VERB_COPULA COPULA] PASSED

=================================================================================== 12 passed, 2 xfailed in 1.26 seconds ===================================================================================

```


### Some more concrete examples

#### Example 1


All examples can be found in (tagmania_examples.py)
 
```
The bill passed 81-18. Sixteen Democrats and two libertarian-minded Republicans voted against it. Among them were a number of potential Democratic presidential candidates in 2020 including Cory Booker, Kirsten Gillibrand, Kamala Harris, Bernie Sanders and Elizabeth Warren.
```

pos_tagged by spacy:


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

let's say you trust the people that the spacy [NER](https://en.wikipedia.org/wiki/Named-entity_recognition) spits out , tags, and insert them into the tags, as such: 

```
pers =  [(u'Cory Booker', u'PERSON'),
 (u'Kirsten Gillibrand', u'PERSON'),
 (u'Kamala Harris', u'PERSON'),
 (u'Bernie Sanders', u'ORG'),
 (u'Elizabeth Warren', u'PERSON')]

```

so after getting the (NER) [https://en.wikipedia.org/wiki/Named-entity_recognition] of names from spacy, 
we can insert them into the rules list 

```
rules = []
rules += ["<{0}>,PERSON".format(text) for text,tag in pers]
    
```
Now imagine, we want to be able to group PERSONS and call them a PERSON_LISTING, we add the following rule to the above rules.  
```
rules.append('<(PERSON COMMA PERSON)+>,PERSON_LISTING') 
```

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


#### Example 2:

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
 
(to see full output, run tagmania_examples in /tests)  

So that is the idea, by uploading rules , and tweaking them , one can manipulate pos-tags and use their information, position to extract information that might be important for annotation, or understanding text in general.



## Authors

* **Dominic Doyle** - *Initial work* - [DomDomDoy](https://github.com/DomDomDoy)
* **Alex McKenzie** - *Initial work* - [Arrrlex](https://github.com/Arrrlex)


## Acknowledgments

* Big thanks to Assaf Bar-Moshe, the linguist who inspired this library 
* Big thanks to Sam Lavigne [antiboredom](https://github.com/antiboredom) for his inspiring NLP experiments
* Big thanks to  the github and all the open source libraries out there 

