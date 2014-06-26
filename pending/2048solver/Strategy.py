#!/usr/bin/python
# Stephen Mayhew
# 2014

import random

class Strategy:
    '''
    This is just a superclass. This always returns 'up' as a move.

    This is never intended to be used, always subclassed.
    '''

    def move(self, grid):
        """
        This must return one of 'up', 'down', 'left', 'right'
        """
        return "up"

        
class RandomStrategy(Strategy):

    def move(self, grid):
        return random.choice(["up", "down", "left", "right"])

