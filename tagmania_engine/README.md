# Tagmania Engine

This repo consists of the code for processing tagmania rules, as well as the rules we use for linguistic information extraction (currently: POS tagging, chunking, clause splitting, semantic role labelling and geographical token extraction).

## Tagmania

Tagmania is a mini-language designed for matching or transforming lists consisting of tuples or NLTK trees (henceforth 'chunks'). The transformations tagmania can peform are the following:
 - Replacing the tag of a chunk with a specified tag;
 - Putting several chunks under one chunk with a specified tag;
 - Adding a special "clause opening" or "clause closing" chunk with a specified tag

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
 9. Matching a chunk by recursively matching its children (using the braces `{`, `}`)

### Rule structure

A tagmania rule consists of a search pattern, followed by a comma, followed by some tags.

The search pattern is broken up into groups, which are either capturing (marked for tag replacement or gathering under a new chunk) or non-capturing. The groups are separated by delimiters, i.e. either a space (` `) or a double caret (`^^`)

Each group consists of delimiter-separated individual patterns, which are intended to match or not match exactly one chunk. A group also may feature an operator (`!`, `?` or `*`, at the end), anchors (either `^` at the beginning or `$` at the end), and brackets (parentheses for non-capturing groups, angle brackets for capturing groups).

Each individual pattern consists of the words or tags to match (`.`, a word, or several words separated by pipes), and optionally a lookinside, which is an entire search pattern enclosed in braces meant to be recursively applied to the contents of one chunk. The individual patterns can also feature an operator and anchors.


### Example

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

