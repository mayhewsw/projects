# Import the corpus and functions used from nltk library
from nltk.corpus import reuters
from nltk.corpus import genesis
from nltk.corpus import brown
from nltk.probability import LidstoneProbDist, WittenBellProbDist
from nltk.model import NgramModel


n = 4
corpus = brown.words(categories="news")
est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
lm = NgramModel(n, corpus, estimator=est)


print "Working with {0}-grams".format(n)
prompt = "context word >> "
s = raw_input(prompt)

while s != "q":
    if len(s.split()) != n:
        print "please enter {0} words".format(n)
    else:
    
        cont = s.split()[0]
        wrd = s.split()[1]

        if wrd in corpus:
            print lm.prob(wrd, cont.split())
        else:
            print "Sorry: '" + wrd + "' is not in the corpus. Try another."

    s = raw_input(prompt)
    

