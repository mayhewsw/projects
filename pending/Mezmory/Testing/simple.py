from Tkinter import *

def hello():
	print "hello"

root = Tk()
menu = Menu(root)

filemenu = Menu(menu, tearoff = 0)
filemenu.add_command(label="Open", command = hello)
filemenu.add_command(label = "save", command = hello)
filemenu.add_separator()
filemenu.add_command(label = "Quit", command = root.quit)




menu.add_cascade(label="File", menu = filemenu)
menu.add_command(label="Quit", command = root.quit)




root.config(menu = menu)
root.mainloop()


