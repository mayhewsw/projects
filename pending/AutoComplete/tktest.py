from Tkinter import *
import hunspell


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.textwnd = Text(frame, width=80, font=("Helvetica", 12, ""))
        self.textwnd.pack(padx=5, pady=5)
        self.textwnd.config(state=DISABLED)


        self.entry = Entry(frame, width=50, font=("Helvetica", 20, ""))
        self.entry.bind("<space>", self.space_pressed)
        self.entry.bind("<Return>", self.enter_pressed)
        
        self.entry.pack(padx=5, pady=10)

        self.entry.focus_set()

        
        self.button = Button(frame, text="Quit", command=frame.quit,highlightthickness=0, font=("Helvetica", 15, ""))
        self.button.pack(padx = 5,pady=5, side=LEFT)
        

    def space_pressed(self, event):
        s = self.entry.get()
        lastword = s.split()[-1]

        punc = ""
        if lastword[-1] in [".", "?","!",'"', "'"]:
            punc = lastword[:-1]


        hobj = hunspell.HunSpell('/usr/share/hunspell/en_US.dic', '/usr/share/hunspell/en_US.aff')
        
        if not hobj.spell(lastword):
            fixed = hobj.suggest(lastword)[0] + punc
        else:
            fixed = lastword + punc

        # clear the box
        self.entry.delete(0, END)
        # insert something new into it
        self.entry.insert(0, s[:-len(lastword)] + fixed)

    def enter_pressed(self, event):
        self.space_pressed(event)
        self.textwnd.config(state=NORMAL)
        #self.textwnd.delete(1.0, END)
        self.textwnd.insert(END, self.entry.get() + "\n")
        self.textwnd.config(state=DISABLED)
        
        self.entry.delete(0, END)
        

if __name__ == "__main__":
    root = Tk()
    
    app = App(root)
    
    root.mainloop()
