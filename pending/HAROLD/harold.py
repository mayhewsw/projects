## This comes from:
## http://stackoverflow.com/questions/2667057/english-dictionary-as-txt-or-xml-file-with-support-of-synonyms
## >>> from nltk.corpus import wordnet
##  >>> 
##  >>> # Get All Synsets for 'dog'
##  >>> # This is essentially all senses of the word in the db
##  >>> wordnet.synsets('dog')
##  [Synset('dog.n.01'), Synset('frump.n.01'), Synset('dog.n.03'), 
##   Synset('cad.n.01'), Synset('frank.n.02'),Synset('pawl.n.01'), 
##   Synset('andiron.n.01'), Synset('chase.v.01')]

##  >>> # Get the definition and usage for the first synset
##  >>> wn.synset('dog.n.01').definition
##  'a member of the genus Canis (probably descended from the common 
##  wolf) that has been domesticated by man since prehistoric times; 
##  occurs in many breeds'
##  >>> wn.synset('dog.n.01').examples
##  ['the dog barked all night']

##  >>> # Get antonyms for 'good'
##  >>> wordnet.synset('good.a.01').lemmas[0].antonyms()
##  [Lemma('bad.a.01.bad')]

##  >>> # Get synonyms for the first noun sense of 'dog'
##  >>> wordnet.synset('dog.n.01').lemmas
##  [Lemma('dog.n.01.dog'), Lemma('dog.n.01.domestic_dog'), 
##  Lemma('dog.n.01.Canis_familiaris')]

##  >>> # Get synonyms for all senses of 'dog'
##  >>> for synset in wordnet.synsets('dog'): print synset.lemmas
##  [Lemma('dog.n.01.dog'), Lemma('dog.n.01.domestic_dog'), 
##  Lemma('dog.n.01.Canis_familiaris')]
##  ...
##  [Lemma('frank.n.02.frank'), Lemma('frank.n.02.frankfurter'), 


# Logic.
# Find most common words from shakespeare. Store these, or load them.
# Whenever a word is inputted, from those most common words, then search for the
# phrase.
# If no common word is inputted, try asking a simple question.
from nltk import *
from nltk.corpus import gutenberg
from nltk.corpus import wordnet as wn
import string
import random
from nltk.corpus import PlaintextCorpusReader

class KeyPhrase:
    '''
    The main purpose of this class is store
    a keyword, an associated phrase, and a list of synonyms
    '''
    def __init__(self, keyword, phrases=["default list"]):
        self.keyword = keyword
        self.synonyms = getSynonyms(self.keyword)
        self.phrases = phrases

    def kpcontains(self, word):
        return word in self.getWordAndSyns()

    def getAnyPhrase(self):
        phrase = random.choice(self.phrases)
        return joinSmartPunc(phrase)
        
    def getWordAndSyns(self):
        return self.synonyms + [self.keyword]

    def getKeyword(self):
        # TODO: perhaps return stems of word?
        return self.keyword

    def setPhrases(self, phrases):
        self.phrases = phrases


def joinSmartPunc(wordList):
    # str.join() is a little too naive for this.
    # Need correct spaces after punctuation
    stop_punc = [".",";","!","?", ":", ","]

    st = ""
    nextsepshort = False
    for wd in wordList:
        if nextsepshort:
            sep = ""
            nextsepshort = False
        else:
            sep = " "
        if wd in stop_punc:
            sep = ""
        elif wd in string.punctuation:
            sep = ""
            nextsepshort = True
        st = st + sep + wd
    return st.strip()


def getNimportant(text, n):
    '''
    This takes a text and finds n most popular
    nouns, verbs, and adjectives in the text.
    '''
    fdist = FreqDist(text)
    vocab = fdist.keys()

    # Filter out stopwords
    stopwords = corpus.stopwords.words('english')
    #newVocab = [w for w in first500 if w.lower() not in stopwords and w.lower() not in string.punctuation]

    # From the first n most popular words, extract all nouns, verbs, and adjectives.
    newVocab = []
    brk = False
    for word in vocab:
        # we only want n of these
        if len(newVocab) >= n:
            break
        if word.lower() in stopwords or word.lower() in string.punctuation:
            continue

        for synset in wn.synsets(word):
            for lemma in synset.lemmas:
                p = lemma.synset.pos
                if p == 's' or p == 'v' or p == 'a':
                    newVocab.append(word.lower())
                    brk = True
                    break
            # I'm happy if at least one
            # word in the synset is a noun,
            # verb or adjective
            if brk:
                break

    return newVocab


def provideAnswer(text, kps, shake):
    '''
    This extracts useful words from the input, and provides an answer
    kps is a list of KeyPhrases
    '''

    # Filter out stopwords
    stopwords = corpus.stopwords.words('english')
    newVocab = [w for w in text.split() if w.lower() not in stopwords]
    #print newVocab
    
    # If nothing left...
    #if len(newVocab) == 0:
    #    print "You say nothing of consequence."
    #    return
    
    # Strip punctuation
    

    # If it's a question
    if text.strip()[-1] == "?":
        exclam = ["Well, to answer that I would look to where ", "Interesting question. "]
    else:
        exclam = ["Ah, interesting. ", "Yes, indeed. ", "Well, it's interesting you say that, because ", "It's funny you should mention that. I was just reading where ", "In one of my favorite lines of all time, ",]

    # If one of the words is in the set.
    p = getRelevantPhrase(newVocab, kps, shake)
    if p:
        print random.choice(exclam) + "Shakespeare wrote:"
        # TODO: maybe take from stock phrases here?
        print "\"" + p + "\""
        return

    # TODO: come up with better stock phrases
    if "to be or not to be" in text:
        print "That is the question, isn't it?"
        return

    # if of form, YOU ARE, return Very observant!
    # if of form, other stuff, return, other stuff
    
    print "WHAT'S THAT? YOU'LL HAVE TO SPEAK UP. I CAN'T HEAR YOU."


def getRelevantPhrase(wordlist, kps, shake):
    '''
    Takes a list of words from a phrase, and a list of KeyPhrases
    The goal of this function is to search the KeyPhrases for a
    phrase that matches the wordlist the most.
    If no match is found, then return None
    '''
    # we want the kps with the most matches to the phrase
    maxLen = 0
    mxKps = None
    save = None
    for k in kps:
        # Check to see if keyword actually shows up
        if not k.getKeyword() in wordlist:
            continue
        
        # get intersection of wordlist and kps word and syns
        i = intersect(k.getWordAndSyns(), wordlist)

        l = len(i)
        if l > maxLen:
            #print k.getWordAndSyns()
            maxLen = l
            mxKps = k
            save = i

    #print save
    if mxKps:
        return joinSmartPunc(getRandPhrase(mxKps.getKeyword(), shake))

    return None


def intersect(a, b):
    ''' Returns the intersection of two lists '''
    return list(set(a) & set(b))


def getSynonyms(word):
    ''' Return a list of synonyms of a word '''
    syns = []
    for s in  wn.synsets(word):
        syns += s.lemma_names
    
    return list(set(syns))


def getRandPhrase(word, text):
    '''
    Get phrases from text
    '''
    # Find all indices of word in text
    inds = [i for i, x in enumerate(text) if x.lower() == word.lower()]
    stop_punc = [".",";","!","?"]

    # pick a random index
    irand = random.choice(inds)
    
    # move backward from index until you find stop punctuation (or the beginning)
    currstart = irand
    while text[currstart] not in stop_punc:
        currstart -= 1
        if currstart == 0:
            break
                    
    # move forward from index until you find stop punctuation (or the end)
    currend = irand
    while text[currend] not in stop_punc:
        currend += 1
        if currend == len(text)-2:
            break

    return text[currstart+1:currend+1]
    

def repl():
    '''
    This is the Read-Eval-Print loop for the dialogue.
    '''

    # Setup the dictionary, preprocessing
    print "You'll have to pardon me, at my age, it takes several moments to memorize all of Shakespeare..."
    #shake = gutenberg.words('shakespeare-caesar.txt')
    #shake = gutenberg.words('shakespeare-complete.txt')
    #print "Done with getwords"
    pcr = PlaintextCorpusReader(".", 'shakespeare.*')
    shake = pcr.words("shakespeare-complete.txt")
    imps = getNimportant(shake,500)
    print imps
    #print "Done with get imps"
    
    # divide the text into blocks of 3000 words (split on periods?)
    # store blocks? Hmm. or just read from shake by line, based on block number
    # can actually just index each word.

    # need a way to index the text
    kps = []
    for word in imps:
        #kps.append(KeyPhrase(word, getPhrases(word, shake)))
        kps.append(KeyPhrase(word))

    #print "Done with kps stuff"

    #print imps

    # Define words that will exit the program
    goodbyeWords = ["quit", "bye", "goodbye", "q", "exit", "leave"]

    # Greetings
    print "Ah, finally someone who will speak Shakespeare with me! How do you do, sir?"
    print

    # Main loop
    while True:
        # Prompt
        text = raw_input('> ').lower()
        print

        # Exit strategy
        if text in goodbyeWords:
            print "Goodbye!"
            break

        # Answer
        provideAnswer(text, kps, shake)
        print
        

def main():
    repl()
    #shake = gutenberg.words('shakespeare-caesar.txt')
    #print "OK..."
    #ph = getPhrases("Rome", shake)
    #for p in ph:
    #    print string.join(p)


if __name__ == '__main__':
    main()
