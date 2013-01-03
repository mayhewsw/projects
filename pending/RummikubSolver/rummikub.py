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

_sep = ":"
colors = ["black", "blue", "yellow", "red"]


def getTiles():
    ''' this creates the board. There are 106 tiles, this creates a
    list with a certain string representing each tile '''

    mycolors = map(lambda s: s + _sep, colors)
    
    tiles = []
    for t in range(1,14):
        four_tiles = map(lambda c: c+str(t),mycolors)
        tiles.extend(four_tiles) # we do this twice
        tiles.extend(four_tiles)
    tiles.append("red:-5")
    tiles.append("black:-5")
    return tiles


# set some global variables
gameTiles = getTiles()
board = []

class Player:
    def __init__(self, playerNumber):
        self.num = playerNumber
        self.started = False
        # tiles is dictionary of form:
        #   {color : [num, num, num], ...}
        self.tiles = {}
        for c in colors:
            self.tiles[c] = []

    def __repr__(self):
        return "P" + str(self.num) + ": " + str(self.tiles)

    def getNumTiles(self):
        return sum(map(len, self.tiles.values()))
    
    def play(self):
        ''' if can play, make the play (modify the board) and return true
        otherwise, return false '''
        global board
        if self.started:
            # normal move code goes here
            # examine the board
            canMove = False
            if canMove:
                # then move!
                return True
            else:
                return False
                
        else:
            # move has to be above 30
            # cannot use tiles from the board
            canMove = False

            plays = []
            for c in self.tiles:
                nums = self.tiles[c]
                # are there three consecutive
                cplays = getAllSequences(nums)
                fplays = []
                for p in cplays:
                    fplays.append(map(lambda n: c + _sep + str(n), p))
                plays.extend(fplays)
            # now check the plays...
            # is the sum greater than 30?

            for i in range(1, 14):
                # do all four colors contain i?
                t = map(lambda lst: i in lst, self.tiles.values())
                # are there 3 or more trues in t?
                if sum(t) >= 3:
                    play = []
                    for color, val in zip(self.tiles.keys(), t):
                        if val:
                            play.append(color + _sep + str(i))
                    plays.append(play)

            # FIXME: need to check for conflicts...

            # get the sum of all values in plays
            total = 0
            for play in plays:
                total += sum(map(lambda s: int(s.split(_sep)[1]), play))

            if total >= 30:
                # change the board
                return True
            else:
                return False
                
    def draw(self, n, l=[]):
        ''' draw n tiles from gameTiles '''
        global gameTiles

        # get the tiles
        if len(l) == 0:
            newtiles = random.sample(gameTiles, n)
        else:
            newtiles = l

        # remove tiles from remaining
        # add the new tiles to the hand
        for t in newtiles:
            gameTiles.remove(t)
            color, num = t.split(_sep)
            self.tiles[color].append(int(num))

        # sort the tiles in each color
        for t in self.tiles:
            self.tiles[t] = sorted(self.tiles[t])

def getAllSequences(nums):
    ''' given a (sorted) list of numbers, this will
    find all consecutive sequences of length 3
    or greater, and return a list of those sequences '''
    if len(nums) == 0:
        return []
    plays = []
    play = [nums[0]]
    for n in nums[1:]:
        if n == play[-1] + 1:
            play.append(n)
        else:
            if len(play) >= 3:
                plays.append(play)
            play = [n]
    if len(play) >= 3:
        plays.append(play)
    return plays

            
            
def mainGameLoop():
    # define the # of players
    numPlayers = 4
    
    # create players and deal
    players = []
    for i in range(numPlayers):
        p = Player(i+1)
        p.draw(14)
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
