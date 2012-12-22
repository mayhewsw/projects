from Tkinter import *
import Mezmory
import string



def debug(item, message=""):
    """Print a debug line to the screen.

    This fuction should be only used once and deleted once I am sure I understand how it is working."""

    # If there are two parts, seperate them by a colon.
    if message<>"":
        print "[debug]",item,":[",message,"]"
    else:
        print "[debug]",item

class MezmoryBoard(Frame):
    '''The GUI, like a white or black board, but a Mezmory board instead.

    The main component of the board is self.text, a Text Widget.

    When the user types, the text is allowed to be added
        until the user switches the type of word
        then the word is removed from the board and attempted to be found
        using the Tablet, which is the underlying structure that actually
        stores the user's results.

    The tablet is parsed and displayed within this Board's text.
        The display is color coded using self.text's Tag feature
        The display can be refreshed at any time based on contents of the Tablet,
            the only information in text that is not in the tablet is the newly typed word.
            (so perhaps one should only refresh between words, come to think of it?)
        Also, for speed, an algorithm for adding and removing words will be
            developed to insert the appropriate words in an identical manner to the refresh.
    '''

def __init__(self, master=None, destroyOnClose=True):
        """Create a new MezmoryBoard.	master = (Typically Tk()... that is the toplevel application)        destroyOnClose = Whether to actually remove the program when it stops.                Users will expect this to be True                For debug purposes it is nice to be able to stop the program running,                so that we can play with its code.
        """

        # Set up and save the master, usually the top of the appication.
        if master==None:
            master = Tk()
        self.master = master


        # Save whether the user wants to destroy (remove) the program when they quit.
        self.destroyOnClose=destroyOnClose

        
        Frame.__init__(self, master)
        self.pack(side=LEFT, fill=BOTH)
        self.createWidgets()

        self.userTypeInit()

        self.version = "0.9"

        # Set the title bar
        master.title("Mezmory " + self.version)
        
        # The book is the parsed file the user is trying to type
        self.book = Mezmory.Book()

        # Give the user a chance to pick a book
        fd = FileDialog(master)

        try:
            if fd.result:
                try:
                    self.book.parseFile(fd.result)
                except IOError: # If there is any kind of IO Error, try the default file
                    self.book.parseFile()
            else: # if no result use the default file
                self.book.parseFile()
        except IOError: # If there is any kind of IO Error, just quit!
            # TODO: add a gentler error handling!
            self.quit
            
        # The tablet stores the user's work.
        #  The text is considered volatile, while the tablet stores the "real" work.
        self.tablet = Mezmory.Tablet(self.book)

        # The tags are based on the tablet score types, so you need the tablet first
        self.initTags()

        self.status.set("Welcome to Mezmory.  Please remember to focus on the meaning of the text!")    

     def close(self, event=None):
     	"""The user chooses to close the program.
	
        Destroy: Whether or not to actually remove the program. Usually the user wishes to do so.
        	"""
        	self.quit()    # Stops the program running

        if self.destroyOnClose:
            self.master.destroy()  # actually removes the program

    def help(self, event=None):
        '''Gives the use help. To start with using the status bar.'''
        self.status.set("Type the text from memory.  Tab=hint, Control-Delete=delete word, Ctrl+F=Fast Forward, Shift+Delete Rewind")

    def refreshText(self, event=None):
        """Displays the contents of the tablet, plus the word being typed.

        Clears all the text except the word currently being typed.
        Writes the words in the Tablet, with formatting.

        See Mezmory.Book and Tablet for the structure of the book and tablet.

        The event is so that this method can be bound to a key sequence.
        """

        #1. First save the partially typed word
        newWord = self.text.get("leftOfNewText",INSERT) # gets to text up to but not including the letter just typed
        
        #2. Clear the text
        self.text.delete("1.0",END)

        #3. Print the words up to the current word before the insert point
        self.text.mark_gravity(INSERT, RIGHT) #The text will add to the left (the INSERT will move right)

        # Warning: Reading attributes of tablet directly
        if self.tablet.lastIsWord:
            stopIndex = self.tablet.currentIndex
        else :
            # after writing whitespace, the index automatically advances to the next word.
            stopIndex = self.tablet.currentIndex - 1

        for index in range(0,stopIndex + 1):    # the range does not include the last number given, so we must add 1
            word = self.book[index][0]
            if index < self.tablet.currentIndex or not self.tablet.lastIsWord:
                # only write the whitespace after the last word, if whitespace has just been written
                whitespace = self.book[index][1]
            else:
                whitespace = ""
                
            # The tag is the formatting. These are defined in self.initTags()
            tag = str(self.tablet[index])

            self.text.insert(INSERT,word+whitespace,tag)

        #4. Put the partially typed word back
        self.text.mark_set("leftOfNewText", INSERT)
        self.text.insert(INSERT,newWord)

        #5. Print the words after the current word (at the END)
        if False: # maybe one day we'll want this, but for now, I'm turning it off.
            self.text.mark_gravity(INSERT, LEFT) #The text will add to the right (the INSERT will move left)

            for index in range(self.tablet.currentIndex+1,self.tablet.maxIndex+1):
                # Note: need to go to maxIndex+1 because range goes to but not including the given number.
                word = self.book[index][0]
                whitespace = self.book[index][1]
                tag = str(self.tablet[index])
                self.text.insert(END,word+whitespace,tag)

            self.text.mark_gravity(INSERT, RIGHT) #The text will add to the left again (so we don't confuse the user!)

    def initTags(self):
        """Tags: (correspond to the Tablet score types)
        blank
        correct
        close
        skipped
        continued
        (Tags are the way Tk does formatting of its Text)
        """
        self.text.tag_config(str(self.tablet.blank),foreground="gray")
        self.text.tag_config(str(self.tablet.correct),foreground="black")
        self.text.tag_config(str(self.tablet.close),foreground="orange")
        self.text.tag_config(str(self.tablet.skipped),foreground="blue")
        self.text.tag_config(str(self.tablet.continued),foreground="blue4")
        self.text.tag_config(str(self.tablet.hint),foreground="green3")
        
    def userTyped(self, event):
        """Any time the user presses a key, this function will look to see if he has finished a word."""

        char = event.char

        if len(char)==0: # If the shift, alt, or Control key were pressed, there will be no character given 
            return
        elif not char in string.printable: # if the user types a non printable character, just ignore it, and let tk Text handle it.
            return

        # check the current word type (whitespace or not) with the last character
        # (Note: If currentlyIsWord is None, then we have just started!
        if self.currentlyIsWord <> None and Mezmory.isWord(char) <> self.currentlyIsWord :
            self.userFinishedWord()

        if char == '\t': # if the user types tab, give him a hint.
            self.giveHint()

        # save the current word so we can compare with it for the next key
        self.currentlyIsWord = Mezmory.isWord(char)

    def userTypeInit(self):
        """Set up the variables used for managing the user's input"""
        self.currentlyIsWord = None #We don't know what the user will type first! 
        self.userStartedWord()

    def userDeleted(self, event):
        """Delete the last typed word."""
        self.tablet.deleteWord()
        self.refreshText()

    def userFinishedWord(self, writeWord=True):
        """The user just switched from typing word to whitespace or vise versa.

        Tk Text Marks:
            * leftOfNewText: seems self explanatory

        writeWord tells whether or not to try to write the word to the Tablet
                (Hints don't need to write the word, as the hint method takes care of that)

        Note: This gets called before tk Text receives the letter,
        so no matter what we do, when we are done the new letter will be inserted.
            """

        # Get the word that the user has just typed
        newWord = self.text.get("leftOfNewText",INSERT) # gets to text up to but not including the letter just typed
        self.text.delete("leftOfNewText",INSERT)
        debug("newWord",newWord)

        # If the caller expects us to write the word to the underlying tablet, do so
        if writeWord:
            # If the user has deleted the word/whitespace they were entering, then ignore it... as if they typed an error.
            if len(newWord)==0:
                indexChange = 0
            else:
                # Write the word to the tablet
                indexChange = self.tablet.writeWord(newWord)
        # If they don't want us to write the word, they've probably already written it...
        else:
            indexChange = 1 #If we aren't going to process it, then assume a normal continue

        # If the index hasn't changed, then we don't need to do anything
        if indexChange == 0:
            pass # Silenty accept mistakes
        # If the index has progressed normally, we can just write the new word/whitespace
        elif indexChange == 1:
            tag = str(self.tablet.getScore()) # The tag is the formatting, see self.initTags()
            self.text.insert(INSERT,self.tablet.getWord(),tag)
        # Otherwise, we'll rewrite everytihng from scratch...
        else:
            self.refreshText()
            
        # (For testing) refresh when the word refresh is typed.
        if newWord=='refresh':
            self.refreshText()

        # Start the new word
        self.userStartedWord()

    def userStartedWord(self):
        """Get ready for the user to type a new word."""
        self.text.mark_set("leftOfNewText", INSERT)
        self.text.mark_gravity("leftOfNewText", LEFT) #The mark will move to the left of any insertions at the mark.

    def giveHint(self):
        '''Add the next word, as a hint.
        '''
        # First write the preceding space, if necessary.
        if self.tablet.writeHintSpace():
            self.userFinishedWord(writeWord=False)

        # Next write the word
        # Do the normal stuff for finishing a word, but don't process it, as we've already done that. 
        self.tablet.writeHint()
        self.userFinishedWord(writeWord=False)

    def fastForward(self, event):
        '''Hint several words at a time.'''
        for iteration in range(0,50):
            self.tablet.writeHintSpace()  # Will only write the space if needed
            self.tablet.writeHint()
        self.refreshText()

        # Start the new word
        # self.userStartedWord()
        
    def fastRewind(self, event):
        '''Delete several words at a time.'''
        for iteration in range(0,50):
            self.tablet.deleteWord()
        self.refreshText()
                
    ### Initialization ###

    def createWidgets(self):
        """Set up the widgets... including the key bindings (i.e. 'shortcuts')."""
        # A note on packing: any thing that is "packed"
        #    will take a slice off the side indicated, first things "slice" first
        #    the pack method packs the object into its parent/master

        self.status = StatusBar(self)
        self.status.pack(side=BOTTOM, fill=X)

        self.toolbar = Frame(self)
        
        self.QUIT = Button(self.toolbar,text="QUIT",fg="red")
        self.QUIT["command"] =  self.close
        self.QUIT.pack({"side": "left"})

        self.btnHelp = Button(self.toolbar,text="Help",command=self.help)
        self.btnHelp.pack(side=LEFT)

        self.toolbar.pack(side=TOP, fill=X)

        self.text = Text(self)
        self.text.pack(side=LEFT, fill=Y)
        # Bind any key pressed in the Text box to be processed in the userTyped method
        self.text.bind("<Key>",self.userTyped) 

        self.text.bind("<Control-BackSpace>",self.userDeleted)
        self.text.bind("<Shift-BackSpace>",self.fastRewind)
        self.text.bind("<Control-r>",self.fastRewind)
        self.text.bind("<Shift-Tab>",self.fastForward)
        self.text.bind("<Control-f>",self.fastForward)
        self.text.bind("<Control-R>",self.refreshText)
        self.text.bind("<Control-q>",self.close)
        self.text.bind("<F1>",self.help)

import os

class Dialog(Toplevel):
    '''A Dialog that handles common dialog like things.

    Straight from the tkinter introduction.'''


    def __init__(self, parent, title = None):
        '''
        The main trickery is done in the constructor; first, transient is used to associate this window
        with a parent window (usually the application window from which the dialog was launched).
        The dialog won't show up as an icon in the window manager (it won't appear in the task bar
        under Windows, for example), and if you iconify the parent window, the dialog will be hidden
        as well. Next, the constructor creates the dialog body, and then calls grab_set to make the
        dialog modal, geometry to position the dialog relative to the parent window, focus_set to move
        the keyboard focus to the appropriate widget (usually the widget returned by the body
        method), and finally wait_window.
        '''
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent
        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
        
        self.initial_focus.focus_set()
        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body. return widget that should have
        # initial focus. this method should be overridden
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)
        self.bind("&lt;Return>", self.ok)
        self.bind("&lt;Escape>", self.cancel)
        box.pack()

    #
    # standard button semantics
    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    def validate(self):
        return 1 # override

    def apply(self):
        pass # override

class FileDialog(Dialog):
    '''A simple dialog to elicit which file to open.'''
    def body(self, master):
        '''Set up the body to include only one line - the line to enter the file name.'''
        Label(master, text="Filename:").grid(row=0)
        self.fileEntry = Entry(master)
        self.fileEntry.grid(row=0, column=1)
        return self.fileEntry # initial focus is on the fileEntry box

    def apply(self):
        self.result = self.fileEntry.get()    

class StatusBar(Frame):
    '''A simple status bar.

    Code started from "An introduction to TkInter.
    I expect I'll be adding functionaltiy as I want it.
    '''

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

mb = MezmoryBoard()
mb.mainloop()

