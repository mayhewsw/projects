
def allCombsOfNums(n):
    ''' Returns all combinations of length n using numbers 1-9'''
    if n == 1:
        return map(lambda x: str(x), range(2,10))

    retList = []
    lst = allCombsOfNums(n-1)
    for num in lst:
        for i in range(2, 10):
            retList.append(str(i) + num)

    return retList
         
    
def wordsFromNumString(n):
    l = []
    l.append(["a", "b", "c"])
    l.append(["d", "e", "f"])
    l.append(["g", "h", "i"])
    l.append(["j", "k", "l"])
    l.append(["m", "n", "o"])
    l.append(["p", "q", "r", "s"])
    l.append(["t", "u", "v"])
    l.append(["w", "x", "y", "z"])
    
    mfile = open('/etc/dictionaries-common/words', 'r')
    dictFile = mfile.read()
    mdict = MyDict(dictFile)
    
    wrds = []
    # move all numbers down by 2, that is, 2277 becomes 0055
    for i in n:
        d= int(i) - 2
        wrds.append(l[d])

    allcombs = combine(wrds)
    retList = []
    for comb in allcombs:
        if mdict.contains(comb, True):
            retList.append(comb)

    return retList
            
            
def combine(lst):
    if len(lst) == 1:
        return lst[0] #map(lambda x: [x], lst)

    retList = []
    clst = combine(lst[1:])
    for c in lst[0]:
        for d in clst:
            retList.append(c + d)

    return retList



class MyDict(object):
    '''
    My own datastructure. This is basically a cross between a dictionary and a list. The keys are 2 letter sequences, 
    which are all the beginnings of the words from the list passed in (dictString). The values are strings, specifically pipe separated words that begin
    with the 2 letter key sequence. 
    An example dictionary might look like this:
        {'da' : "|dare|daring|dastardly|...|", 'ze' : "|zest|zealously|zebra|...|", ...}
        
    The contains function takes the first 2 letters of the word in question and gets the list associated with those letters from the 
    dictionary. From there, it is simple string search. 
    
    '''

    def __init__(self, dictString):
        '''
        Constructor: expects a dictString, a string of words separated by whitespace
        '''
        # a dictionary
        self.dict = {}
        
        self.__populateDict(dictString)
        

    def __populateDict(self, dictString):
        '''
        __populateDict simply takes the 
        '''
        dictSplit = dictString.split()
        
        # Get the first 2 letters of the first word
        comb = dictSplit[0][0:2]
        
        # This will contain all the words that begin with that particular combination
        wordsList = [dictSplit[0]]
        
        
        for word in dictSplit:
            
            if word[0:2] != comb:
                self.dict[comb] = "|" + "|".join(wordsList) + "|"
                wordsList = []
                
            comb = word[0:2]
            wordsList.append(word)
               
    def contains(self, word, strict=False):
        ''' This checks if the dictionary contains the given word, or if there is a word that starts with the given word.
            If strict is set to True, then it only checks if the whole word is in the dictionary, and does not check for parts of words
            Examples: a search for 'tree' should return true
                      a search for 'cr' should return true (because crass, for example, is in the dictionary)
                      a search for 'pm' should return false because there are no words that begin with pm '''
        
        
        beginning = word[0:2]
        itShouldBeInHere = []
        
        if beginning in self.dict:
            itShouldBeInHere = self.dict[beginning]
            
            if strict:
                s = "|" + word + "|"
                return s in itShouldBeInHere
            else:
                return "|" + word in itShouldBeInHere
        
            
            # now check if any part of the word is in here
            
        return False
         
        
    def __binarySearch(self, n):
        # haven't implemented this yet.
        this = "function is empty"
     
        
    def __repr__(self):
        '''
        Overrides the print function for the class
        '''
        print(self.dict.keys())

if __name__ == "__main__":
    #l = wordsFromNumString("2117")
    out = open("numpadwords.txt", 'w')
    

    for i in range(6, 7):
        numCombs =  allCombsOfNums(i)
        for num in numCombs:

            wrds = wordsFromNumString(num)
            if len(wrds) <= 1:
                continue

            print num
            # We're only interested in those key combinations that form
            # at least 2 words
            out.write("\n" + num + "\n")
            for w in wrds:
                out.write(w + " ")
            out.write("\n")
       
    out.close()

