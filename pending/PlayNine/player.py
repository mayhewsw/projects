# Create all the players necessary
from abc import ABCMeta, abstractmethod
import logging
import random
from strategies import *
from collections import defaultdict
import sys
import math

FORMAT = "[%(asctime)s] : %(filename)s.%(funcName)s():%(lineno)d - %(message)s"
DATEFMT = '%H:%M:%S, %m/%d/%Y'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
logger = logging.getLogger(__name__)


class Player():
    __metaclass__ = ABCMeta

    # this number needs to be even
    NUM_CARDS = 8

    def __init__(self, num, board):
        # initialize cards from deck
        self.num = num
        self.board = board

        self.mycards = []
        self.cardisvisible = [["?", "?"] for i in range(0, self.NUM_CARDS, 2)]

    def __str__(self):
        return "[{} {}]".format(self.num, self.__class__.__name__)

    def setmycards(self, cards):
        if len(cards) != self.NUM_CARDS:
            logger.error("Num cards needs to be {}, but is {}".format(self.NUM_CARDS, len(cards)))
            return
        self.mycards = [[cards[i], cards[i+1]] for i in range(0, self.NUM_CARDS, 2)]
        self.flip2()

    def wrap(self, strat, card):
        """
        This wraps the strategy functions. (Just for saving space)
        """
        discard = strat(card, self.cardisvisible, self.mycards)
        if discard:
            self.board.discardpile.insert(0, discard)
            return True
        return False

    def flip2(self):
        """
        set two cards to be face up.
        """
        r1 = (random.randint(0, self.NUM_CARDS/2-1), random.randint(0,1))
        r2 = (random.randint(0, self.NUM_CARDS/2-1), random.randint(0,1))

        while r1 == r2:
            r2 = (random.randint(0, self.NUM_CARDS/2-1), random.randint(0,1))

        self.cardisvisible[r1[0]][r1[1]] = self.mycards[r1[0]][r1[1]]
        self.cardisvisible[r2[0]][r2[1]] = self.mycards[r2[0]][r2[1]]

    def score(self, which="c"):
        """ This will score the board of this player at the end of the game, or before
        """
        # 1 pairs: 0 points
        # 2 pairs: -10
        # 3 pairs: -15
        # score -5

        if which == "c":
            deck = self.mycards
        elif which == "v":
            deck = self.cardisvisible
        else:
            logger.error("Bad arguments to player.score(which=???)! Exiting...")
            sys.exit(-1)

        pairs = defaultdict(int)

        # otherwise, get the sum
        score = 0
        for c1, c2 in deck:
            # don't score the unknown cards
            if c1 == "?":
                c1 = random.random() / 100.
            if c2 == "?":
                c2 = random.random() / 100.

            if c1 != c2 or c1 == -5 or c2 == -5:
                score += c1 + c2
            else:
                # they are the same
                pairs[c1] += 1

        for k in pairs:
            t = pairs[k]
            if t == 2:
                score -= 10
            if t == 3:
                score -= 15

        return math.floor(score+0.5)

    def isdone(self):
        """
        Check if this player is done. (If any of "?" remain in cardisvisible, then NO)
        """
        return not "?" in sum(self.cardisvisible, [])

    def printvisiblehand(self):
        toprow = map(lambda p: p[0], self.cardisvisible)
        bottomrow = map(lambda p: p[1], self.cardisvisible)

        fstring = ["{:<5}"] * len(self.cardisvisible)
        fstring = " ".join(fstring)
        print(self)
        print(fstring.format(*toprow))
        print(fstring.format(*bottomrow))
        print("")

    def printfullhand(self):
        toprow = map(lambda p: p[0], self.mycards)
        bottomrow = map(lambda p: p[1], self.mycards)

        fstring = ["{:<5}"] * len(self.cardisvisible)
        fstring = " ".join(fstring)
        print(fstring.format(*toprow))
        print(fstring.format(*bottomrow))
        print("")

    @abstractmethod
    def maketurn(self):
        pass


class RandomPlayer(Player):
    """ This player chooses randonly from the different options.
    """

    def maketurn(self):
        """
        Do a turn
        """

        # dumb player: always choose from the draw pile
        drawn = self.board.drawpile[0]
        del self.board.drawpile[0]

        if self.wrap(firstempty, drawn):
            return


class SlightlyBetterPlayer(Player):
    """
    This does the regular good thing.
    """

    def maketurn(self):
        """
        Do a turn
        """

        # first check if we have a match for the discard
        fromdiscard = self.board.discardpile[0]

        # if this is -5, put it in the first open spot
        if fromdiscard == -5:
            if self.wrap(firstempty, fromdiscard):
                return

        if self.wrap(findpair, fromdiscard):
            return

        # otherwise, choose from the draw pile
        drawn = self.board.drawpile[0]
        del self.board.drawpile[0]

        # if this is -5, put it in the first open spot
        if drawn == -5:
            if self.wrap(firstempty, drawn):
                return

        # if this card can make a pair then keep it and return
        if self.wrap(findpair, drawn):
            return

        total = 0
        for c in sum(self.cardisvisible,  []):
            if c == "?":
                total += 1

        if total > 1:
            if self.wrap(firstempty, drawn):
                return


class MinimizeCostPlayer(Player):
    """
    This player tries to minimize cost...
    """

    def maketurn(self):
        """
        Do a turn
        """

        # first check if we have a match for the discard
        discard = self.board.discardpile[0]

        # if this is -5, put it in the first open spot
        if discard == -5 and self.wrap(firstempty, discard):
            return

        # check to see if card has a pair
        if self.wrap(findpair, discard):
            return

        # otherwise, choose from the draw pile
        drawn = self.board.drawpile[0]
        del self.board.drawpile[0]

        # if this is -5, put it in the first open spot
        if drawn == -5 and self.wrap(firstempty, drawn):
            return

        # if this card can make a pair then keep it and return
        if self.wrap(findpair, drawn):
            return

        # if this card
        if self.wrap(lowerscore, drawn):
            return

        total = 0
        for c in sum(self.cardisvisible,  []):
            if c == "?":
                total += 1

        if total > 1:
            if self.wrap(flipfirstunopened, drawn):
                return

        # this means I've done nothing
        self.wrap(ignore, drawn)


if __name__ == "__main__":
    pass
