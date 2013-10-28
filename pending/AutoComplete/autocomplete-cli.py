from minimumeditdistance import *
import hunspell
from Tkinter import *



# The way this works is as follows:
# read text
# every time a word is completed, do the following:
# check if it is in the dictionary, if so, leave it
# (consider: looking for higher probability words with small edit distance)
# if not in dictionary, find all words with small edit distance.
# for all words with small edit distance, get bigram (trigram? n-gram?) probability of occurrence.

# need a function like this:
# def getSimilar(word, dist=3):
#   ''' get all words with edit distance <= dist '''


# also think about incorporating keyboard key distance also. Hmm.


def populateDictionary():
    d = {}

    file = open('/etc/dictionaries-common/words', 'r')

    for line in file:
        dummy = 0
        d[line.strip()] = dummy

    return d
    




print LevenshteinDistance("this", "that")

if __name__ == "__main__":
    
    hobj = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')

    print "Press enter after each word"
    prompt = ">> "
    s = raw_input(prompt).split()
    fullS = ""
    
    while True:
        for word in s:
            if not hobj.spell(word):
                word = hobj.suggest(word)[0]
            fullS += word.strip() + " "
            print fullS

        s = raw_input(prompt).split()
        if s[0] == "":
            break

    #print fullS
