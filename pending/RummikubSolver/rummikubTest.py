import random
import unittest
import rummikub

class TestRummikub(unittest.TestCase):

    def setUp(self):
        self.board = []
        self.p = rummikub.Player(1)
        rummikub.gameTiles = rummikub.getTiles()


    def test_init(self):
        self.p.draw(14)

        self.assertEqual(self.p.getNumTiles(), 14)
        # self.assertEqual(sum(self.p.tiles.values()), 14)
        self.assertEqual(len(rummikub.gameTiles), 106 - 14)

    def test_len(self):
        self.assertEqual(self.p.getNumTiles(), 0)
        
    def test_draw(self):
        self.p.draw(1, ["blue:12", "red:1", "blue:3", "yellow:8","yellow:1", "yellow:3"])

        self.assertEqual(self.p.getNumTiles(), 6)
        self.assertEqual(self.p.tiles["yellow"][0], 1)
        self.assertEqual(self.p.tiles["yellow"][1], 3)
        self.assertEqual(self.p.tiles["yellow"][2], 8)

        self.p.draw(1, ["blue:12"])
        self.assertEqual(self.p.getNumTiles(), 7)
        self.assertEqual(self.p.tiles["blue"][0], 3)
        self.assertEqual(self.p.tiles["blue"][1], 12)
        self.assertEqual(self.p.tiles["blue"][2], 12)
        
    def test_true(self):
        self.p.draw(0, ["blue:12", "red:1", "blue:11", "yellow:8","blue:10"])
        v = self.p.play()
        self.assertTrue(v)
        # board has changed?

    def test_true2(self):
        self.p.draw(0, ["blue:10", "red:10", "yellow:10"])
        v = self.p.play()
        self.assertTrue(v)
        # board has changed?
        
    def test_false(self):
        self.p.draw(0, ["blue:1", "red:1", "blue:11", "yellow:8","yellow:10"])
        v = self.p.play()
        self.assertFalse(v)
        # board hasn't changed

    def test_false2(self):
        self.p.draw(0, ["blue:1", "red:1", "blue:2", "blue:3","yellow:10"])
        v = self.p.play()
        self.assertFalse(v)
        # board hasn't changed

    def test_seqs(self):
        seq = [1, 2, 3]
        self.assertEqual([seq], rummikub.getAllSequences(seq))

        in_seq = [1, 3, 6]
        self.assertEqual([], rummikub.getAllSequences(in_seq))

        in_seq = [1, 2, 3, 7, 8, 9, 10]
        out_seq = [[1, 2, 3], [7, 8, 9, 10]]
        self.assertEqual(out_seq, rummikub.getAllSequences(in_seq))
        
        in_seq = [1, 2, 3,4, 7, 8]
        out_seq = [[1, 2, 3,4]]
        self.assertEqual(out_seq, rummikub.getAllSequences(in_seq))

        
        
    def test_play(self):
        lenptiles = len(self.p.tiles)
        lengameTiles = len(rummikub.gameTiles)

        # FIXME: needs more stuff here
        
        
        
if __name__ == '__main__':
    unittest.main()
