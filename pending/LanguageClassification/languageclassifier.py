# Language classifier
# In short:
# Tokenize corpora by space, and create bigrams, trigrams, using letters.
# For example: "frogs eat fancy mangers" -> $f, fr, ro, og, gs, s_, _e, ea, ... etc.
# Testing would just be checking against various types of classifiers...
# Could also come up with backwards english classifier.

import nltk
from nltk.corpus import udhr
import string
from collections import defaultdict
import re
import locale
import math
import operator

# corpora
# cess_esp: spanish
# alpino: dutch
# treebank: english

# French website
# http://www.lemonde.fr/

def parse():

    dicts = []

    # print "Parsing English..."
    # # Parse english first
    # enList = []
    # for w in nltk.corpus.treebank.words():
    #     enList += splitWord(w, 2)
    #     # enList += splitWord(w, 3)
    # enDict = makeHist(enList, "english")
    # dicts.append(enDict)
    
    # print "Parsing Spanish..."
    # esList = []
    # # Parse Spanish
    # locale.setlocale(locale.LC_CTYPE, 'es_ES')
    # for w in nltk.corpus.cess_esp.words():
    #     esList += splitWord(w, 2)
    #     # esList += splitWord(w, 3)
    # esDict = makeHist(esList, "spanish")
    # dicts.append(esDict)


    # print "Parsing Dutch..."
    # # Parse Dutch
    # locale.setlocale(locale.LC_CTYPE, 'nl_NL')
    # nlList = []
    # for w in nltk.corpus.alpino.words():
    #     nlList += splitWord(w, 2)
    #     # nlList += splitWord(w, 3)
    # nlDict = makeHist(nlList, "dutch")
    # dicts.append(nlDict)

    # locale.resetlocale(locale.LC_CTYPE)

    latin_langs = filter(lambda n: "Latin" in n, udhr.fileids())
    for lang in latin_langs:
        print "Parsing " + lang + "..."
        lang_list= []
        for w in udhr.words(lang):
            lang_list = splitWord(w, 2)
        lang_dict = makeHist(lang_list, lang)
        dicts.append(lang_dict)

    # return all dictionaries
    return dicts

def train():
    # for each language, make the dictionaries.
    pass

def test(input, dicts):
    # for a given input, split it
    splinput = splitWord(input, 2)

    scoredict = {}

    # get the counts from each dictionary, add 1 to all of them
    for d in dicts:
        currscore = 0
        for b in splinput:
            # currscore += math.log(d[b] / d["totalsize"])
            val = float(d[b]+1) / (d["totalsize"] + len(d))
            currscore += math.log(val)
        scoredict[d["language"]] = currscore

    return scoredict
    
    # get the log probabilities
    
    
        
def makeHist(ngramlst, language):
    ''' Create a histogram given a list '''
    d = defaultdict(int)
    for w in ngramlst:
        d[w] += 1
    d["totalsize"] = len(ngramlst)
    d["language"] = language
    return d
        

def splitWord(w, n):
    ''' Given a word w, split it up into blocks of characters, each
    block having length n. Return a list of those blocks. '''
    # Make toLower
    w = w.lower()

    # Remove punctuation
    #w = string.translate(w, None, r"!',.?/\\@#$%^&*()-_+=[]{}|;:<>\"")
    w = "".join(filter(lambda c: re.match(r"\w", c, re.LOCALE), w))

    
    w = "$"*(n-1) + w + "$"*(n-1)
    if n == 1:
        return list(w)

    l = []
    for i in range(n):
        l.append(w[i:])

    return map(lambda lst: "".join(lst), zip(*l))

    
    
if __name__ == "__main__":
    dicts = parse()

    print "Enter a word: (q to quit)"
    user = raw_input()
    while(user != 'q'):
        scoredict = test(user, dicts)
        sorted_dict = sorted(scoredict.iteritems(), key=operator.itemgetter(1))
        sorted_dict.reverse()
        for i in range(5):
            print sorted_dict[i]
        print "\nEnter a word: (q to quit)"
        user = raw_input()
