#!/usr/bin/python

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
from svmutil import *

from FeatureVector import FeatureVector

# corpora
# cess_esp: spanish
# alpino: dutch
# treebank: english

# French website
# http://www.lemonde.fr/

def parseLang(corpus, langname, loc=None):
    if loc is not None:
        locale.setlocale(locale.LC_CTYPE, loc)
    tokenlist = []
    seen = set()
    total = 0
    for w in corpus:
        if w not in seen:
            tokenlist += splitWord(w, 2)
            seen.add(w)
            total += 1
    return makeHist(tokenlist, langname)

def makeVector(w, lang):
    fv = FeatureVector()
    for f in splitWord(w,2):
        fv.add(f)
    fv.setLabel(lang)
    return fv

def parse():
    #dicts = []

    y, x = [], []
    
    print "Parsing English..."
    # Parse english first
    #enDict = parseLang(nltk.corpus.treebank.words(), "english")
    #dicts.append(enDict)
    for w in nltk.corpus.treebank.words():
        fv = makeVector(w, "english")
        y.append(fv.getLabel())
        x.append(fv.getFeatDict())


    print "Parsing Spanish..."
    #esDict = parseLang(nltk.corpus.cess_esp.words(), "spanish", 'es_ES.utf8')
    #dicts.append(esDict)
    for w in nltk.corpus.cess_esp.words():
        fv = makeVector(w, "spanish")
        y.append(fv.getLabel())
        x.append(fv.getFeatDict())

    
    print "Parsing Dutch..."
    #nlDict = parseLang(nltk.corpus.alpino.words(), "dutch", 'nl_NL.utf8')
    #dicts.append(nlDict)
    for w in nltk.corpus.alpino.words():
        fv = makeVector(w, "dutch")
        y.append(fv.getLabel())
        x.append(fv.getFeatDict())


    print "Num features:"
    print len(FeatureVector._featuremap.feat_ind)

    ratio = 0.8
    split = int(len(x)*ratio)

    x_train = x[:split]
    x_test = x[split:]
    
    y_train = y[:split]
    t_test = y[split:]

    m = svm_train(y_train, x_train)
    p_label, p_acc, p_val = svm_predict(y_test, x_test, m)

    print p_label, p_acc, p_val
    ACC, MSE, SCC = evaluations(y, p_label)
    print ACC, MSE, SCC

    
    # locale.resetlocale(locale.LC_CTYPE)

    # latin_langs = filter(lambda n: "Latin" in n, udhr.fileids())
    # for lang in latin_langs:
    #     print "Parsing " + lang + "..."
    #     lang_list= []
    #     for w in udhr.words(lang):
    #         lang_list = splitWord(w, 2)
    #     lang_dict = makeHist(lang_list, lang)
    #     dicts.append(lang_dict)

    # return all dictionaries
    # return dicts

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
    #dicts = parse()
    parse()

    # print "Enter a word: (q to quit)"
    # user = raw_input()
    # while(user != 'q'):
    #     scoredict = test(user, dicts)
    #     sorted_dict = sorted(scoredict.iteritems(), key=operator.itemgetter(1))
    #     sorted_dict.reverse()
    #     for i in range(len(sorted_dict)):
    #         print sorted_dict[i]
    #     print "\nEnter a word: (q to quit)"
    #     user = raw_input()
