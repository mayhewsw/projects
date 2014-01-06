
class BoardDrawer():

    def __init__(self, board):
        self.board = board
        #self.update()

    def update(self, currentplayer = None):
        print(chr(27) + "[2J")

        #print("Draw pile has: {} cards".format(len(self.board.drawpile)))
        print("Draw pile (top card): {}".format(self.board.drawpile[0]))
        print("Discard pile: {}\n".format(self.board.discardpile[0]))

        for p in self.board.players:
            if p == currentplayer:
                print("TURN -> ", end="")
            p.printvisiblehand()
            p.printfullhand()
            print("Score: {}".format(p.score(which="v")))
            print("\n")

        ignorethis = input("Press Enter to continue...")
        if ignorethis == "q":
            print("Ok, exiting...")
            import sys
            sys.exit(1)
