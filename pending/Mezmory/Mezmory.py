# This is supposed to be a gift for Josiah...


def isWord(character):
    """Checks whether the given character is a word or whitespace.

    If a word is given, the first character is used.

    Throughout this document I've used the term "whitespace" far too liberally.
    When I say "whitespace" I mean anything that is not a word,
    including numbers and punctuation as well as whitespace.
    """
    if len(character) == 0:
        raise NoWordError
    elif len(character) > 1 :
        character = character[0] #Allow words, sampling the first character
    return ('a' <= character <= 'z') or ('A' <= character <= 'Z')

def sameWord(word1,word2):
    """Checks whether the two words are the same.

    In the future may allow mispelling to some extent."""
    return word1.lower()==word2.lower()

class Book:
    """The text that a person wishes to memorize.

    The text is simply parsed and stored here."""

    def __init__(self):
        """Initializes an empty Book.

        self.words = [['This',' '],['is',' '],['an',' '],['example'],['.']]

        self.dictionary = dictionary of counts of words

        self.maxSearch = the farthest the search algorithm will look for the word.

        self.freqFact = how many words past the predicted frequency of the word we are willing to search.
                1 = exactly at prediction, 2 = twice the predicted distance, .5 = half the distance etc.
        """
        self.words=[]
        
        self.dictionary = dict()

        self.maxSearch = 20 #perhaps we'll want to raise this value later.

        self.freqFact = .1
            # Todo: set dynamically?  (Higher percentage for shorter texts?)
            # How do you decide what value to use? A study of the "evenness" of word spreading?

    def __getitem__(self, index):
        """Returns the [word,whitespace] pair indexed."""
        return self.words[index]

    def parseFile(self, path="James (NIV).txt"):
        """Breaks the file into a list of word/whitespace pairs.

        E.g. [[word, whitespace &/or punctuation],[word, whitespace &/or punctuation]]
        """
        
        print path

        f = open(path)  #Allow the user to catch any exceptions in the opening of the file

        lastChar = " "
        word, white = "", ""

        for line in f:
            for character in line:
                if isWord(character)==isWord(lastChar):
                    # keep adding to exising word or whitespace
                    if isWord(character):
                        word = word + character
                    else :
                        white = white + character
                elif isWord(character):
                    # beginning a new word, save the old words
                    if not (not word and not white): # Don't add the original empty set 
                        self.words = self.words + [[word, white]]
                        self.addToDictionary(word)
                    word, white = character, ""
                else : white = white + character

                lastChar = character

        # Add the last word
        self.words = self.words + [[word, white]]
        self.addToDictionary(word)

    def wordCount(self,word) :
        """Returns the number of times the word appears in the text"""
        return self.dictionary[word.lower()]
        
    def addToDictionary(self, word):
        """Adds the given word to the stats dictionary"""
        keyWord = word.lower()
        if keyWord in self.dictionary :
            self.dictionary[keyWord] = self.dictionary[keyWord] + 1
        else :
            self.dictionary[keyWord] = 1

    def isSkippedWord(self, word, checkIndex, targetIndex):
        """Guesses whether the word is skipped based on word frequency and the current position.

        checkIndex = index to check
        targetIndex = index where the students is currently writing.
        """
        actualWord = self.words[checkIndex][0]
        if sameWord(word,actualWord):
            if abs(checkIndex-targetIndex) <= len(self.words)/self.wordCount(actualWord)*self.freqFact:
                return True
            else :
                return False
        else :
            return False
    
class Tablet:
    """This is the place the student "writes" the text from memory.

    Only the correct (or almost correct) words are saved though.
    Actually, only the score for each word and the stuent's position are saved,
    though it will feel to the student as if he is typing it, only the correct text will appear,
    as saved in the Book.
    """
    
    def __init__(self, theBook):
        """Sets up an empty test array the same size as the book it is to wrap."""
        self.book = theBook

        self.scores = []

        # Possible scores (constants!)
        self.blank = 0
        self.correct = "Y"
        self.close = "y"
        self.skipped = "s"
        self.continued = "S"
        self.hint = "h"

        self.possibleScores = [self.blank, self.correct, self.close, self.skipped, self.continued, self.hint]

        if len(theBook.words) == 0:
            raise UserWarning, "The book is empty, use parseFile before initializing this class"

        for word in theBook.words:
            self.scores = self.scores + [[self.blank,self.blank]]

        self.maxIndex = 0 # The furthest index the student has reached 
        self.currentIndex = 0 # The current index where the student is writing

        self.lastIsWord = None # Indicates whether the last given item was word or whitespace
            #Note: Originally I avoided using this variable - usually check the input to see if a word or whitespace was given

    def __getitem__(self, index):
        """Returns the scores of the word (not whitespace) indexed.

        Accessed as if the tablet itself were an array: tablet[index]
        """
        return self.scores[index][0]

    def getWord(self, index=None, isWord=None):
        '''Returns the indexed word or whitespace

        If no index is given, returns the most recent word.'''

        if isWord==None:
            isWord = self.lastIsWord

        if isWord:
            if index==None:
                index = self.currentIndex

            return self.book[index][0]
        else:
            if index==None:
                index = self.currentIndex - 1 # We have to subtract 1, since we always advance after whitespace

            return self.book[index][1]                

    def getScore(self, index=None, isWord=None):
        '''Returns the indexed word.

        If no index is given, returns the score of the most recently entered word.
        '''

        if isWord==None:
            isWord = self.lastIsWord

        if isWord:
            if index==None:
                index = self.currentIndex
            return self.scores[index][0]
        else:
            if index==None:
                index = self.currentIndex - 1 # We have to subtract 1, since we always advance after whitespace
            return self.scores[index][1]

    def setScore(self, index=None, isWord=None, score=None):
        """Sets the score, if not yet set.

        WARNING: Untested method!!! Need to add to the tests.
        """
        if score == None:
            score = self.blank

        if not score in self.possibleScores:
            raise Warning('Attempting to set non-valid score!')

        if isWord==None:
            isWord = self.lastIsWord

        # Handle words and whitespace differently
        if isWord:
            if index==None:
                index = self.currentIndex
            self.scores[index][0] = score
        else:
            if index==None:
                index = self.currentIndex - 1 # We have to subtract 1, since we always advance after whitespace
            self.scores[index][1] = score

    def writeHintSpace(self):
        '''Writes the next space to the tablet, if necessary.

        Returns True if there was a space that needed to be hinted
        '''

        result = ""

        if self.lastIsWord:
            self.scores[self.currentIndex][1] = self.hint # mark the whitespace as correct
            result = result + self.getWord(self.currentIndex,isWord=False) # add the whitespace to the result
            if self.currentIndex < len(self.book.words) - 1:
                self.currentIndex = self.currentIndex + 1 # Advance to the next word
            self.lastIsWord = False # We have just written a space, so the last is not a word.
            return True  #There was a space needed.
        else:
            return False #There was no space needed.

    def writeHint(self):
        '''Writes the next word automatically, with no user input.

        Should be used after writeHintSpace, to ensure the previous space has been hinted if necessary.
        '''
        if self.lastIsWord == True:
            raise Warning('Sequence error: write Hint should only be used after writeHintSpace, to ensure the next word is a hint.')

        # Set the score if not already set
        # TODO: Test and use getScore and setScore here!
        if self.scores[self.currentIndex][0] == self.blank:
            self.scores[self.currentIndex][0] = self.hint # Score the word as hint

        # Advance
        self.lastIsWord = True # When hinting, the last is always a word

    def findWord(self, studentsWord, index):
        """Attempts to find the given word near to the given index.

        Won't return words that have already been written, which is why it is in the Tablet class.

        Returns: The index of the first word found,
                searching first at the index given,
                then leading towards the index from the back,
                finally searhing ahead of the index

                If the word is not found, returns None
        """
        # Words and whitespace will be handled differently
        if not isWord(studentsWord):
            if self.scores[index][0]<>self.blank:
                return index # White space is always "correct"
            else :
                return None # Unless the previous word has not yet been typed         
        else : 
            # Check if they are right, the easiest case!
            if sameWord(studentsWord,self.book.words[index][0]):
                return index
            else :
                # now we must find the word, start backwords
                for searchIndex in range(max(index-self.book.maxSearch,0),max(index,0)):
                    if self.book.isSkippedWord(studentsWord,searchIndex,index) and not self.isWritten(searchIndex):
                        return searchIndex
                # next search forwards
                for searchIndex in range(min(index+1,len(self.book.words)),
                                         min(index+self.book.maxSearch,len(self.book.words))):
                    if self.book.isSkippedWord(studentsWord,searchIndex,index) and not self.isWritten(searchIndex):
                        return searchIndex         

    def isWritten(self, index):
        """Indicates if the students has already written the word."""
        return self.scores[index][0]!=self.blank

    def writeWord(self, studentsWord):
        """The student attemtps to write the next word.

        Returns the change in index.
            If the user is remembering correctly this should be 1
            If the user has typed a completely incorrect word it will be 0
                (as the index will remaind where it was before)
            Otherwise a posive index indicates the number of words skipped forward
                and negative the number backwards.
        """
        #   Note: The current index "anticipates" by pointing to where we expect the user to be typing.
        #   Thus the change in index is not simply the differnce between the current and old indices.
        
        currentIndex = self.findWord(studentsWord, self.currentIndex)

        if currentIndex == None:
            return 0 # If the user hasn't typed a new word, the index hasn't changed

        # We have to update the max index before the tests because we may have jumped ahead
        self.maxIndex = max(currentIndex, self.maxIndex)

        if isWord(studentsWord):
            wwIndex = 0 # Sets the word/whitespace index
        else :
            wwIndex = 1

        #Save the old index
        oldIndex = self.currentIndex

        #...before we update self.currentIndex
        if isWord(studentsWord):
            # If we just typed a word, we need to stay to type the whitespace
            self.currentIndex = currentIndex
        elif currentIndex >= len(self.book.words) - 1 :
            # If we have reached the end, don't pass it.
            self.currentIndex = len(self.book.words) - 1
        else:
           # If it is whitespace we need to advance
            self.currentIndex = currentIndex + 1
 
        #If the word matches the furthest word found so far mark it as correct
        if currentIndex == self.maxIndex:
            self.scores[currentIndex][wwIndex]=self.correct
        #Otherwise, if it matches the word where the user is typing,
                #mark it as correct, continuing where he is
        elif currentIndex == oldIndex:
            self.scores[currentIndex][wwIndex]=self.continued
        #Otherwise he must be going back to fill in a missed word, which we mark as skipped    
        else:
            self.scores[currentIndex][wwIndex]=self.skipped

        # Save what the last item entered was 
        self.lastIsWord = isWord(studentsWord)

        # Return the advance amount of the index
        # We have to add one to the the difference to account for the "anticipation" that we do.
        return  currentIndex - oldIndex + 1

    def deleteWord(self):
        """Removes the score of the last given word, and whitespace.

        Will end with the previously typed word with whitespace."""

        if not self.lastIsWord: # if they just entered whitespace
            self.scores[self.currentIndex][1] = self.blank # delete

        # No matter what, delete the last typed word and 
        self.scores[self.currentIndex][0] = self.blank

        # we don't want to back up past the beginning...
        if self.currentIndex>0:
            # back up the indicator of the max advance if the user is currently at the end,
            # This is because effectively the user is starting over
            if self.currentIndex == self.maxIndex:
                self.maxIndex = self.maxIndex -1
            
            # back up to the previous word.
            self.currentIndex = self.currentIndex-1
 
class NoWordError(Exception):
    """Thrown if not given a word when one is expected.

    This should never happen. But then bugs are never supposed to happen!
    """

    def __init__(self, description="An empty string was given as a word or whitespace."):
        ''' Typically this will be called when "An empty string was given as a word or whitespace."
        '''
        self.description=description

    def __str__(self):
        '''Returns the description of why the error was thrown.'''
        return repr(self.description)
