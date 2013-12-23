# Create all the players necessary
from abc import ABCMeta, abstractmethod
import logging
FORMAT = "[%(asctime)s] : %(filename)s.%(funcName)s():%(lineno)d - %(message)s"
DATEFMT = '%H:%M:%S, %m/%d/%Y'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt=DATEFMT)
logger = logging.getLogger(__name__)
import random


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
        return "[{} {}]".format(self.__class__.__name__, self.num)

    def setmycards(self, cards):
        if len(cards) != self.NUM_CARDS:
            logger.error("Num cards needs to be {}, but is {}".format(self.NUM_CARDS, len(cards)))
            return
        self.mycards = [[cards[i], cards[i+1]] for i in range(0, self.NUM_CARDS, 2)]
        self.flip2()

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

    def score(self):
        """ This will score the board of this player at the end of the game, or before
        """
        # 1 pairs: 0 points
        # 2 pairs: -10
        # 3 pairs: -15
        # score -5

        from collections import defaultdict
        pairs = defaultdict(int)

        # otherwise, get the sum
        score = 0
        for c1, c2 in self.mycards:
            #print(c1, c2)
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

        return score

    def isdone(self):
        """
        Check if this player is done. (If any of "?" remain in cardisvisible, then NO)
        """
        return not "?" in sum(self.cardisvisible, [])

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
        #logger.debug("player {} takes turn".format(self.num))
        #logger.debug(self.mycards)
        #logger.debug(self.cardisvisible)

        # dumb player: always choose from the draw pile
        drawn = self.board.drawpile[0]
        del self.board.drawpile[0]

        # find a location that is unseen, and replace it.
        for i, v in enumerate(self.cardisvisible):
            if v[0] == "?":
                # use this
                self.board.discardpile.insert(0, self.mycards[i][0])
                self.mycards[i][0] = drawn
                v[0] = drawn
                return
            elif v[1] == "?":
                # use this
                self.board.discardpile.insert(0, self.mycards[i][1])
                self.mycards[i][1] = drawn
                v[1] = drawn
                return


class SlightlyBetterPlayer(Player):
    """ This player chooses randonly from the different options.
    """

    def maketurn(self):
        """
        Do a turn
        """

        # first check if we have a match for the discard
        discard = self.board.discardpile[0]
        for v, card in zip(self.cardisvisible, self.mycards):
            if card[1] == discard and card[0] != discard:
                # replace card[0]
                self.board.discardpile.insert(0, card[0])
                card[0] = discard
                v[0] = discard
                return
            elif card[0] == discard and card[1] != discard:
                # replace card[1]
                self.board.discardpile.insert(0, card[1])
                card[1] = discard
                v[1] = discard
                return

        # dumb player: always choose from the draw pile
        drawn = self.board.drawpile[0]
        del self.board.drawpile[0]

        # if this is -5, replace the largest card that is not a pair
        if drawn == -5:
            for v, card in zip(self.cardisvisible, self.mycards):
                if v[0] == "?":
                    self.board.discardpile.insert(0, drawn)
                    v[0] = card[0]
                    return
                elif v[1] == "?":
                    self.board.discardpile.insert(0, drawn)
                    v[1] = card[1]
                    return

        # if this card can make a pair then keep it and return
        for v, card in zip(self.cardisvisible, self.mycards):
            if card[1] == drawn and card[0] != drawn:
                # replace card[0]
                self.board.discardpile.insert(0, card[0])
                card[0] = drawn
                v[0] = drawn
                return
            elif card[0] == drawn and card[1] != drawn:
                # replace card[1]
                self.board.discardpile.insert(0, card[1])
                card[1] = drawn
                v[1] = drawn
                return

        total = 0
        for c in sum(self.cardisvisible,  []):
            if c == "?":
                total += 1

        if total > 1:
            # just open up the first unopened one
            for v, card in zip(self.cardisvisible, self.mycards):
                if v[0] == "?":
                    self.board.discardpile.insert(0, drawn)
                    v[0] = card[0]
                    return
                elif v[1] == "?":
                    self.board.discardpile.insert(0, drawn)
                    v[1] = card[1]
                    return



if __name__ == "__main__":
    pass
