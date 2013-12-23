#!/usr/bin/python3
# Play Nine, programmed in Python

# how many cards:
# 8 of each card
# 0-12
# -5

from player import RandomPlayer, Player, SlightlyBetterPlayer
from random import shuffle
import logging
FORMAT = "[%(asctime)s] : %(filename)s.%(funcName)s():%(lineno)d - %(message)s"
DATEFMT = '%H:%M:%S, %m/%d/%Y'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
logger = logging.getLogger(__name__)
import sys


class Board():
    """ We need a board class """

    MAX_PLAYERS = 6

    def __init__(self):
        self.drawpile = []

        for i in range(13):
            self.drawpile.extend([i]*Player.NUM_CARDS)

        self.drawpile.extend([-5]*Player.NUM_CARDS)

        shuffle(self.drawpile)

        self.discardpile = [self.drawpile[0]]
        del self.drawpile[0]
        self.players = []

    def addplayer(self, player):
        if len(self.players) == self.MAX_PLAYERS:
            logger.error("Cannot add a player! Only allow {} players".format(self.MAX_PLAYERS))
            sys.exit(-1)

        self.players.append(player)

    def deal(self):
        for player in self.players:
            player.setmycards(self.drawpile[:Player.NUM_CARDS])
            # now remove them from the drawpile
            self.drawpile = self.drawpile[Player.NUM_CARDS:]

    def rungame(self, num=0):
        if num % 500 == 0:
            logger.debug("Run game : {}".format(num))

        firsttogoout = ""
        checkdone = True

        if len(self.players) == 0:
            logger.error("Cannot play with 0 players!")
            return

        totalturns = 0
        while True:
            for player in self.players:
                if firsttogoout == player:
                    #logger.debug("END OF GAME!")
                    break
                player.maketurn()
                totalturns += 1

                logger.debug(len(self.drawpile))
                if len(self.drawpile) == 0:
                    logger.debug("0 len drawpile!!!")
                    sys.exit(-1)

                if player.isdone() and checkdone:
                    #logger.debug(str(player) + " has finished")
                    firsttogoout = player
                    checkdone = False
            else:
                continue
            break

        minscore = 200000
        minp = None

        #logger.debug("Total turns: {}".format(totalturns))

        for p in self.players:
            s = p.score()
            #print("{} : {}".format(p, s))
            if s < minscore:
                minscore = s
                minp = p
        #logger.debug("Winner is: {} with score: {}".format(minp, minscore))
        return minscore, minp


def runmanygames():
    from collections import defaultdict

    winners = defaultdict(int)
    winnerscores = defaultdict(int)

    for j in range(10000):
        b = Board()


        b.addplayer(RandomPlayer(1, b))
        b.addplayer(RandomPlayer(2, b))
        b.addplayer(SlightlyBetterPlayer(3, b))
        b.addplayer(SlightlyBetterPlayer(4, b))

        b.deal()

        minscore, minp = b.rungame(j)

        winners[str(minp)] += 1
        winnerscores[str(minp)] += minscore

    print("{:<30} {:<15} {:<15} {:<15}".format("Player", "Games Won", "Cum. Score", "Avg. Score"))
    print("=====================================================================================")
    for k in sorted(winners):
        print("{:<30} {:<15} {:<15} {:<15}".format(k, winners[k], winnerscores[k], winnerscores[k] / float(winners[k])))

    #print(winners)
    #print(winnerscores)


def runsinglegame():
    b = Board()

    #b.addplayer(RandomPlayer(1, b))
    #b.addplayer(RandomPlayer(2, b))
    b.addplayer(SlightlyBetterPlayer(1, b))
    b.addplayer(SlightlyBetterPlayer(2, b))
    b.addplayer(SlightlyBetterPlayer(3, b))
    b.addplayer(SlightlyBetterPlayer(4, b))

    b.deal()

    minscore, minp = b.rungame(1)

    #for p in b.players:
    #    print(p.mycards)
    #    print(p.cardisvisible)

    print(minscore, str(minp))

if __name__ == "__main__":
    #runsinglegame()
    runmanygames()