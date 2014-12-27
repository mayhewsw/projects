#!/usr/bin/python

from Strategy import Strategy
from util import *
import random

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


class RuleStrategy2(Strategy):

    def move(self, grid):
        """
        Idea: move in this order: left, up/down, up/down, right.

        Only go down the list if move isn't possible.
        """

        canup = canMoveDir("up", grid)
        candown = canMoveDir("down", grid)

        ret = ""
        if canMoveDir("right", grid):
            ret = "right"
        elif canup and candown:
            ret = random.choice(["up", "down"])
        elif canup:
            ret = "up"
        elif candown:
            ret = "down"
        else:
            ret = "left"
        
        return ret


class RuleStrategy3(Strategy):

    def move(self, grid):
        """
        Idea: move in this order: left, up/down, up/down, right.

        Only go down the list if move isn't possible.
        """

        canup = canMoveDir("up", grid)
        candown = canMoveDir("down", grid)

        # if right side column is full (with no duplicate parents)
        a = grid[0][3]
        b = grid[1][3]
        c = grid[2][3]
        d = grid[3][3]

        rightcolfull = True
        if any([a==0,b==0,c==0,d==0]):
            rightcolfull = False
        if any([a==b, b==c, c==d]):
            rightcolfull = False

        # default values.
        canfirst = canup
        firstdir = "up"

        cansecond = candown
        seconddir = "down"

        # but if right col is full...
        if rightcolfull:
            canfirst = candown
            firstdir = "down"
            cansecond = canup
            seconddir = "up"
            
        ret = ""
        if canMoveDir("right", grid):
            ret = "right"
        elif canfirst:
            ret = firstdir
        elif cansecond:
            ret = seconddir
        else:
            ret = "left"
        
        return ret
