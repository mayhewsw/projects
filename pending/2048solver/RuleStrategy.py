#!/usr/bin/python

from Strategy import Strategy
from util import *

class RuleStrategy(Strategy):

    def move(self, grid):
        """
        Idea: move in this order: left, up, down, right.

        Only go down the list if move isn't possible.
        """

        ret = ""
        if canMoveDir("right", grid):
            ret = "right"
        elif canMoveDir("up", grid):
            ret = "up"
        elif canMoveDir("down", grid):
            ret = "down"
        else:
            ret = "left"
        
        return ret
