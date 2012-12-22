#!/usr/bin/python3
# Play Nine, programmed in Python

# We need a board class

class Board():

    def __init__(self):
        unseenCards = {}
        unseenCards = {r : 8 for r in range(13)}
        unseenCards[-5] = 8
        
        print(unseenCards)
        #players = [RandomPlayer, RandomPlayer, RandomPlayer, RandomPlayer]

    def getAverageUnseenValue(self):
        pass


if __name__ == "__main__":
    b = Board()
    
