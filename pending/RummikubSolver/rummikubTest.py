import random
import unittest
import rummikub

class TestRummikub(unittest.TestCase):

    def setUp(self):
        self.board = []
        self.p = rummikub.Player(1)

    def test_init(self):
        rummikub.gameTiles = rummikub.getTiles()
        self.p.draw(14)

        self.assertEqual(len(self.p.tiles), 14)
        self.assertEqual(len(rummikub.gameTiles), 106 - 14)
        

    def test_start(self):
        # give the player a set of tiles
        tiles = ["red:9", "red:10", "red:11"]
        self.p.tiles = tiles
        self.assertTrue(self.p.canStart())
        self.assertTrue(self.p.started)

        tiles = ["red:11", "blue:11", "yellow:11"]
        self.p.tiles = tiles
        self.assertTrue(self.p.canStart())
        self.assertTrue(self.p.started)
        
        tiles = ["red:9", "blue:9", "yellow:9"]
        self.p.tiles = tiles
        self.assertFalse(self.p.canStart())
        self.assertFalse(self.p.started)

        tiles = ["red:12", "blue:12", "yellow:11"]
        self.p.tiles = tiles
        self.assertFalse(self.p.canStart())
        self.assertFalse(self.p.started)

        
    def test_play(self):
        lenptiles = len(self.p.tiles)
        lengameTiles = len(rummikub.gameTiles)

        # FIXME: needs more stuff here
        
        
        
if __name__ == '__main__':
    unittest.main()
