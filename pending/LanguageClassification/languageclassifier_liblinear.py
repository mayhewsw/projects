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
import random
import sys
import argparse

from liblinearutil import *

from FeatureVector import FeatureVector

# corpora
# cess_esp: spanish
# alpino: dutch
# treebank: english

# French website
# http://www.lemonde.fr/

def makeVector(w, lang=None):
    fv = FeatureVector()
    
    for ind, c in enumerate(w):
        fv.add(str(ind) + "-" + c)
    for ind, f in enumerate(splitWord(w,2)):
        fv.add(str(ind) + "-" + f)
    for ind, f in enumerate(splitWord(w, 3)):
        fv.add(str(ind) + "-" + f)
    if lang is not None:
        fv.setLabel(lang)
        
    return fv


def addLanguage(corpus, langname, y, x, seen):
    print "Parsing " + langname + "..."
    for w in corpus:
        #w = w.lower()
        if w in seen:
            continue
        seen.add(w)
        fv = makeVector(w, langname)
        y.append(fv.getLabel())
        x.append(fv.getFeatDict())

    

def read():
    y, x = [], []

    seen = set()

    addLanguage(nltk.corpus.treebank.words(), "english", y,x,seen)
    addLanguage(nltk.corpus.cess_esp.words(), "spanish", y,x,seen)
    addLanguage(nltk.corpus.alpino.words(), "dutch", y,x,seen)

    
    # wantedlangs = ["English", "Dutch", "French", "German"]
    
    # latin_langs = filter(lambda n: "Latin" in n, udhr.fileids())
    # for lang in latin_langs:
    #     for l in wantedlangs:
    #         if l in lang and lang.index(l) == 0:
    #             addLanguage(udhr.words(lang), lang, y,x,seen)
    #             break
        

    # return all dictionaries
    # return dicts


    
    FeatureVector._featuremap.writeLexicon("words.lex")
    
    return y,x

def parse():
    y,x = read()

    print "Num features:"
    print len(FeatureVector._featuremap.feat_ind)

    ratio = 0.8
    split = int(len(x)*ratio)

    yx = zip(y,x)
    random.shuffle(yx)
    y,x = zip(*yx)
    
    x_train = x[:split]
    x_test = x[split:]
    
    y_train = y[:split]
    y_test = y[split:]

    prob = problem(y_train, x_train)
    param = parameter('-c 2 -B 1 -v 5')
    m = train(prob, param)

    save_model("langclass.model", m)
    p_label, p_acc, p_val = predict(y_test, x_test, m)

    #print p_label, p_acc, p_val
    evaluations(y_test, p_label)
    return m


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

    # hack to allow -i and -p to be alone
    if "-i" in sys.argv:
        sys.argv.insert(sys.argv.index('-i')+1, "True")

    parser = argparse.ArgumentParser(description='Classify a language')
    parser.add_argument('-m', dest='modelfile', help="model file", default=None)
    parser.add_argument('-i', dest="interactive", default="False", help='display an interactive loop', type=bool)
    
    args = parser.parse_args()

    fv = FeatureVector()

    if args.modelfile is not None:
        m = load_model(args.modelfile)
        fv._featuremap.readLexicon("words.lex") # so FeatureMap will be populated
    else:
        m = parse()

    if args.interactive:
        print "Enter a word: (q to quit)"
        user = raw_input()
        while(user != 'q'):
            fv = makeVector(user)
            fv_feats = fv.getFeatDict()

            p_label, p_acc, p_val = predict([None], [fv_feats], m)

            print "This word is: " + fv._featuremap.getLabelName(p_label[0])
            print "\nEnter a word: (q to quit)"
            user = raw_input()
        
    

