# Tagmania

Tagmania is a mini-language designed for matching or transforming lists consisting of tuples or NLTK trees (henceforth 'chunks'). The transformations tagmania can peform are the following:
 - Replacing the tag of a chunk with a specified tag;
 - Putting several chunks under one chunk with a specified tag;

## Getting Started


1) 

```
git clone https://github.com/DomDomDoy/tagmania.git 
```

2) place tagmania repo in project directory

3)
```
from tagmania.tagmania_engine import TagmaniaProcessor 

test_rule = u'<this is a test>,TEST'
tagged = [(u'this', u'DT'), (u'is', u'VBZ'), (u'a', u'DT'), (u'test', u'NN')] 

processor = TagmaniaProcessor(test_rule)
valid, mods, transformed_input = processor.transform(tagged)

Out:
[Tree('TEST', [(u'this', u'DT'), (u'is', u'VBZ'), (u'a', u'DT'), (u'test', u'NN')])]

```


### Prerequisites



```
pip install -r requirements.txt
```

*Tagmania is pos-tag agnostic, so any input is a list of tuples and nltk Trees regardless of the pos-tags used

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests
To run pytests, go to tests/ and run the following command

```
pytest -v -m basic tagmania_tests.py

```



### Break down into end to end tests

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



## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Dominic Doyle** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
* **Alex McKenzie** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Big thanks to Alex McKenzie for code review and help with grammar design
* Big thanks to Assaf Bar-Moshe, the linguist who inspired that library 
* I also want to thank Sam lavigne for is open source NLP experiments, spacy and all other open source contributers out there. 

