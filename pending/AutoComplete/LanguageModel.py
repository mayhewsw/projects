# Import the corpus and functions used from nltk library
from nltk.corpus import reuters
from nltk.corpus import genesis
from nltk.corpus import brown
from nltk.probability import LidstoneProbDist, WittenBellProbDist
from nltk.model import NgramModel


corpus = brown.words(categories="news")

estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
lm = NgramModel(2, corpus, estimator)

prompt = "context word >> "
s = raw_input(prompt)

while s != "q":
    cont = s.split()[0]
    wrd = s.split()[1]

    if wrd in corpus:
        print lm.prob(wrd, [cont])
    else:
        print "Sorry: '" + wrd + "' is not in the corpus. Try another."

    s = raw_input(prompt)
    

