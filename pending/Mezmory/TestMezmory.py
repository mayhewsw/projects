# A test module of the Mezmory Module
import MezmoryBoard
import Mezmory

class TestMezmory:
    def __init__(self):
        """Initialize the instances of the classes to test"""
        print "Testing Mezmory"

        self.b = Mezmory.Book()

        # These values are good for testing, but not for real use
        self.b.maxSearch = 10
        self.b.freqFact = .75

        self.b.parseFile("James (NIV).txt")

        self.t = Mezmory.Tablet(self.b)

        
        print __name__ # Just to check

        # Set up some counters to compare how many of the tests have matched what was expected
        self.matchCount = 0
        self.nonmatchCount = 0

    def TestMatch(self,a,b,description=''):
        """Tests if two variables are the same.

        Prints the results and also stores up stats."""
        if a == b:
            print a,"=",b,'\t',description
            self.matchCount=self.matchCount+1
        else:
            print a,"<>",b,description
            self.nonmatchCount=self.nonmatchCount+1

    def TestMatchSummary(self):
        """Prints the final test results for the self.TestMatch"""
        print "Success:",self.matchCount,"Failure:",self.nonmatchCount

    def TestFindWord(self, t):
        """Test Mezmory.Tablet.findWord(...)"""
        self.TestMatch(0, t.findWord("James",0))
        self.TestMatch(0, t.findWord("jaMes",0))

        self.TestMatch(0, t.findWord("james",3))

        self.TestMatch(19, t.findWord("Greetings",10))
            
        return

    def TestFindWordAlreadyWritten(self, t):
        """ Test findWord AFTER words are already Written """
        self.TestMatch(0, t.findWord("James",0),"If you look for a word exactly at the word, you should find it... even if it is already written.")
        self.TestMatch(None, t.findWord("James",1),"If you look for a word that is already written you should not find it.")


    def TestIsSkippedWord(self, b):
        """Test Mezmory.Book.isSkippedWord(...)"""
        self.TestMatch(True, b.isSkippedWord("the",7,6))
        self.TestMatch(True, b.isSkippedWord("the",7,8))
        self.TestMatch(True, b.isSkippedWord("the",17,18))
        self.TestMatch(False, b.isSkippedWord("the",17,6))
        self.TestMatch(True, b.isSkippedWord("Greetings",19,6))

    def TestWriteWord(self, t):
        """Tests the writing in the Tablet (and the corresponding search)."""
        
        self.TestMatch(0, t.findWord("James",0))
        
        self.TestMatch(t.blank, t.scores[0][0])
        t.writeWord("James")
        self.TestMatch(t.correct, t.scores[0][0],"James")
        t.writeWord(" ")
        self.TestMatch(t.correct, t.scores[0][1],"space")
        t.writeWord("a")
        self.TestMatch(t.correct, t.scores[1][0],"a")
        t.writeWord("  ")
        self.TestMatch(t.correct, t.scores[1][1],"too many spaces")
        t.writeWord("SERVant")
        self.TestMatch(t.correct, t.scores[2][0],"SERVant")
        t.writeWord(" ")
        self.TestMatch(t.correct, t.scores[2][1],"space")
        t.writeWord("of")
        self.TestMatch(t.correct, t.scores[3][0],"of")
        t.writeWord(".")
        self.TestMatch(t.correct, t.scores[3][1],".")
        t.writeWord("the")
        self.TestMatch(t.correct, t.scores[7][0],"the")
        t.writeWord(" ")
        self.TestMatch(t.correct, t.scores[7][1]," ")
        t.writeWord("Lord")
        self.TestMatch(t.correct, t.scores[8][0],"Lord")
        t.writeWord(" ")
        t.writeWord("God")
        self.TestMatch(t.skipped, t.scores[4][0]," God")
        t.writeWord(" ")
        t.writeWord("and")
        self.TestMatch(t.continued, t.scores[5][0]," and")
        t.writeWord(" ")
        t.writeWord("BigRedBaloon")
        self.TestMatch(t.blank, t.scores[6][0]," BigRedBaloon")
        t.writeWord(" ")
        self.TestMatch(t.blank, t.scores[6][1],"(unexpected whitespace)")
        t.writeWord("of")
        self.TestMatch(t.continued, t.scores[6][0],"of")
        t.writeWord(" ")
        t.writeWord("Jesus")
        self.TestMatch(t.correct, t.scores[9][0],"' Jesus'")
        t.deleteWord()
        self.TestMatch(t.blank, t.scores[9][0],"(deleted)")
        t.writeWord("Jesus")
        self.TestMatch(t.correct, t.scores[9][0],"' Jesus (rewritten)'")            
        t.writeWord(" ")
        t.writeWord("Christ")
        self.TestMatch(t.correct, t.scores[10][0],"' Christ'")

        # Test the get methods
        self.TestMatch(t.getWord(0),"James","First word is James")
        self.TestMatch(t[0][0],t.correct,"First score is correct")
        self.TestMatch(t.getScore(4),t.skipped,"Another way to get scores")

        # The default get methods should be the most recent value
        self.TestMatch(t.getWord(),"Christ","Most recent word is Christ")
        self.TestMatch(t.getScore(),t.correct,"Most recent score is 'correct'")

        # Test whitespace too!
        t.writeWord(" ")
        self.TestMatch(t.getWord(),",\n","The latest word should be a comma and newline")
        self.TestMatch(t.getScore(),t.correct,"White space is always correct!")

        # Test hinting functionality
        self.TestMatch(t.writeHintSpace(), False, "Try to write a hint, whitespace... should be 'False' as whitespace is NOT needed.")

        t.writeHint()
        self.TestMatch(t.getWord(),"To","Now we write the hint... which is To'")
        self.TestMatch(t.getScore(11),t.hint,"The word 'To' is now scored as 'hint'")

        self.TestMatch(t.writeHintSpace(), True, "Try to write a hint, space... should be 'True' whitespace is needed.")
        self.TestMatch(t.getScore(11,isWord=False),t.hint,"The whitespace is scored as a hint.")
        
        t.writeHint()
        self.TestMatch(t.getWord(),"the","the hinted word was 'the'")
        self.TestMatch(t.getScore(12),t.hint,"The word 'the' is scored as 'hint'")
        
        print t.scores

        # TO DO: Add tests of reaching the end of the file gracefully.  (The test file is short anyway!)

    def RunTests(self):
        self.TestFindWord(self.t)
        self.TestIsSkippedWord(self.b)
        self.TestWriteWord(self.t)
        self.TestFindWordAlreadyWritten(self.t)
        self.TestMatch(self.b.freqFact,.75,"The frequency factor hasn't changed")

        self.TestMatchSummary()



     
tm = TestMezmory()
tm.RunTests()
