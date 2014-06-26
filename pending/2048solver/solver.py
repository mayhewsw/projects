#!/usr/bin/python
# Stephen Mayhew
# 2014

from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
from splinter import Browser
import re
from Strategy import Strategy, RandomStrategy

###############################################
### THIS IS THE ONLY THING THE USER WILL CHANGE

strat = RandomStrategy()
trials = 2

###############################################

# Set up stuff
m = PyMouse()
k = PyKeyboard()

pat = re.compile(r"tile-(\d+) tile-position-(\d)-(\d)")

# This section makes four functions called left(), 
dirs = ["up", "down", "left", "right"]
delay = 0.3
def mk(d, delay):
    def a(dly = delay):
        time.sleep(dly)
        k.tap_key(eval("k.{0}_key".format(d)))
    return a

for d in dirs:
    locals()[d] = mk(d, delay)
# UGLY ===========================================

scores = []
largestvals = []

for t in range(trials):

    browser = Browser()
    browser.visit("http://gabrielecirulli.github.io/2048/")

    # need to have this so that the body is in focus
    x_dim, y_dim = m.screen_size()
    m.click(x_dim/2, y_dim/2, 1)

    largest = 2
    
    # MAIN LOOP
    grid = ()
    while True:
        # this checks up on the current grid state
        div = browser.find_by_xpath("//div[contains(@class, 'tile-container')]")[0]
        grid = re.findall(pat, div.html)

        print grid
        firstg = map(lambda c: c[0], grid)
        intfirstg = map(int, firstg)
        largest = max(intfirstg)
        print largest
        
        # this makes a random move
        direc = strat.move(grid)

        # Actually make the move
        locals()[direc]()

        scoretext = browser.find_by_xpath("//div[@class='score-container']")[0]
        score = int(scoretext.text.split()[0])
        
        # find by xpath is too slow.
        if "game-over" in browser.html:
            print "game over!"
            break
            
    scores.append(int(score))
    largestvals.append(largest)

    browser.quit()


totscore = sum(scores)
avgscore = totscore / float(trials)
print "Average score: {0}".format(avgscore)
print "All scores: {0}".format(scores)

print largestvals




if __name__ == "__main__":
    pass
