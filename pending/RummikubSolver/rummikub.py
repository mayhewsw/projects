# This is a Rummikub solver
# Stephen Mayhew
# December 2012

import random

# This will need a set of tiles (I don't know what the numbers are).
# 104 tiles, 2 joker tiles
# 1 through 13
# Four colors: black, yellow, blue, red.

# there is a "table" which contains all
# the "runs" (stored as lists of tiles)
# as well as all the unused tiles so far

# a "player" has a set of tiles in his "hand"
# and must, at each turn, choose to play
# or if that is not possible, draw from the table

def getTiles():
    ''' this creates the board. There are 106 tiles, this creates a
    list with a certain string representing each tile '''
    
    colors = ["black:", "blue:", "yellow:", "red:"]
    tiles = []
    for t in range(1,14):
        four_tiles = map(lambda c: c+str(t),colors)
        tiles.extend(four_tiles) # we do this twice
        tiles.extend(four_tiles)
    tiles.append("red:joker")
    tiles.append("black:joker")
    return tiles


# set some global variables
gameTiles = getTiles()
board = []

class Player:
    def __init__(self, playerNumber):
        self.num = playerNumber
        self.started = False
        self.tiles = []

    def __repr__(self):
        return "P" + str(self.num) + ": " + str(self.tiles)

    def play(self):
        ''' if can play, make the play (modify the board) and return true
        otherwise, return false '''
        global board
        if p.started:
            # normal move code goes here
            # examine the board
            pass
        else:
            # move has to be above 30
            # cannot use tiles from the board
            canMove = False
            
            if canMove:
                # move! then...
                self.started = True
            else:
                self.draw(1)
            
    def draw(self, n):
        ''' draw n tiles from gameTiles '''
        global gameTiles
        
        newtiles = random.sample(gameTiles, n)
        self.tiles.extend(newtiles)
        for t in newtiles:
            gameTiles.remove(t)
        

def mainGameLoop():
    # define the # of players
    numPlayers = 4
    
    # create players and deal
    players = []
    for i in range(numPlayers):
        pTiles = random.sample(gameTiles,14)
        p = Player(i+1, pTiles)
        print p
        players.append(p)

    # Game loop sentinel
    gameGoing = True

    # this variable stores the current turn
    turn = 0
    while gameGoing:
        # get the current player
        p = players[turn]

        if not p.play():
            p.draw(1)
                
        if len(p.tiles) == 0:
            print "Player", p.num, "has won!"
            gameGoing = False
            
        # update the current turn
        turn += 1
        turn %= numPlayers
    

if __name__ == "__main__":
    mainGameLoop()
