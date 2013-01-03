'''
This was written for Python 3.1
Stephen Mayhew
Nov. 17, 2010

'''
import sys
from math import sqrt,floor

def BoggleSolver():
    '''
    This solves a game of boggle using a dictionary file. 
    
    Letters are stored as tuples representing positions on the grid. 
    
    '''
    
    # Input some file with a list of words separated by whitespace 
    file = open('words.txt', 'r')
    dictFile = file.read()
    dict = MyDict(dictFile)
    
    # Grid string is the characters from each row of the board. 
    # If the board looks like:
    #     s h o r
    #     g i s t
    #     h t e d
    #     s s e n
    # Then gridString is: 'shorgisthtedssen'
	
    # 4 is the standard size for boggle boards, but other numbers work as well.
    # Naturally, larger boards will slow down computation times.    
    boardSize = 4
    gridString = "shorgisthtedssen"
    
    # If there are commands from the command line
    if len(sys.argv) > 1:
        gridString = sys.argv[1] 
	boardSize = math.sqrt(len(gridString))
	if sqrt(boardSize) - floor(sqrt(boardSize)) != 0:
		print("Error: input string is not a square number")
		return
        print("Using word: " + gridString)
    else:
        print("Using default word: " + gridString)
        
    
    if len(gridString) != boardSize * boardSize:
        print("String must be %d characters long!" % (boardSize * boardSize))
        return

    # This takes the gridString and converts it
    # into a nested (boardSize x boardSize) list
    grid = []
    for i in range(boardSize):
        newList = []
        for j in range(boardSize):
            c = gridString[i * boardSize + j]
            if c == 'q':
                c = 'qu'
            newList.append(c)
        grid.append(newList)
    
    wordList = []
    
    for row in range(boardSize):
        for col in range(boardSize):
            
            # A word is simply a set of coordinates. We can get 
            firstWord = [(row, col)]
            
            # find all words starting with letter
            wordList.append(firstWord)
            #print(wordList)

            # this will grow wordlist as it adds 
            for word in wordList:
                    newWords = getWords(word, grid, boardSize)
                    if len(newWords) > 0:
                        addUsIn = []
                        for w in newWords:
                            #if w does not lead to another string
                            s = convertListToLetters([w], grid, boardSize)[0]
                            # if s is a single letter, or if is in dict
                            if len(s) == 1 or dict.contains(s) and not w in wordList:    
                                addUsIn.append(w)
                            
                        wordList += addUsIn
                        
    # Convert the list of lists of tuples to a list of strings
    allWords = convertListToLetters(wordList, grid, boardSize)
    final = []
    
    # Remove words that aren't actually words, but only lead to other words
    # Note the use of the optional argument in contains. This forces it to 
    # match the word exactly, instead of allowing partial matches
    for word in allWords:
        if dict.contains(word, True) and len(word) > 2 and word not in final:
            final.append(word)
    
    # Put the largest words first
    final.sort(key=len, reverse=True)
    
    print("Word list: (" + str(len(final)) + " words)\n")
    finalString = ""
    for f in final:
        finalString += f + ", "
        
    finalString = finalString[:-2]
    print(finalString)
    
    
                    

def convertListToLetters(wordList, grid, gridsize):
    '''
    wordList is a list of lists of tuples. 
        Viz: [[(0,0), (0,1)], [(0,0)]]
    '''
    
    words = []
    for list in wordList:
        s = ""
        for c in list:
            s += grid[c[0]][c[1]]
            
        words.append(s)
        
    return words 
    


def getWords(word, grid, gridsize):
    '''
    This takes a word (in this case, a list of tuples), and finds what possible squares from the grid could be 
    tacked on the end. The only restrictions are that you can't use the same grid square twice, and you have to
    stay within the boundaries of the board. 
    
    This returns a list of lists of tuples. 
    '''
    
    last = word[-1]
    
    newLettersToAdd = []

    # this could be greatly simplified, I think...
    if last[0] > 0:
        new = (last[0] - 1, last[1])
        if not new in word:
            newLettersToAdd.append(new)
    if last[1] > 0:
        new = (last[0], last[1] - 1)
        if not new in word:
            newLettersToAdd.append(new)
    if last[0] > 0 and last[1] > 0:
        new = (last[0] - 1, last[1] - 1)
        if not new in word:
            newLettersToAdd.append(new)
    if last[0] < gridsize - 1:
        new = (last[0] + 1, last[1])
        if not new in word:
            newLettersToAdd.append(new)
    if last[1] < gridsize - 1:
        new = (last[0], last[1] + 1)
        if not new in word:
            newLettersToAdd.append(new)
    if last[0] < gridsize - 1 and last[1] < gridsize - 1:
        new = (last[0] + 1, last[1] + 1)
        if not new in word:
            newLettersToAdd.append(new)
    if last[0] > 0 and last[1] < gridsize - 1:
        new = (last[0] - 1, last[1] + 1)
        if not new in word:
            newLettersToAdd.append(new)
    if last[0] < gridsize - 1 and last[1] > 0:
        new = (last[0] + 1, last[1] - 1)
        if not new in word:
            newLettersToAdd.append(new)
        
  
    returnMe = []
    for letter in newLettersToAdd:
        returnMe.append(word + [letter])
    

    return returnMe


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
    from timeit import Timer
    t = Timer("BoggleSolver()", "from __main__ import BoggleSolver")
    print("\n\nIt took %f seconds to solve this board." % t.timeit(1))
