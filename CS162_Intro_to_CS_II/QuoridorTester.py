# Author: Christopher Felt
# Date: 8/04/2021
#
# Description: Unit test program for testing the Quoridor program. Tests gameplay using the place_fence and move_pawn
# methods.

# import modules
from Quoridor import QuoridorGame
import unittest


class UnitTests(unittest.TestCase):
    """Class for testing the Quoridor program. Inherits from Unit test."""

    def test_QuoridorGame_place_fence(self):
        """Test place_fence method"""

        # create game object
        q = QuoridorGame()

        # test bad input
        self.assertFalse(q.place_fence(1, 7, (6, 5)))  # no h or v
        self.assertFalse(q.place_fence(4, 'h', (6, 5)))  # no player 4
        self.assertFalse(q.place_fence(1, 'h', 'z'))  # not a tuple
        self.assertFalse(q.place_fence(1, 'h', ('z', 1)))  # tuple does not contain two ints

        # ----------------------------- horizontal tests ------------------------------------
        # player 1 places fence at col 6 row 5
        self.assertTrue(q.place_fence(1, 'h', (6, 5)))  # player 1: 9 fences remaining

        # player 1 attempts to place fence at col 7 row 5 out of turn
        self.assertFalse(q.place_fence(1, 'h', (7, 5)))

        # player 2 attempts to place fence at col 6 row 5
        self.assertFalse(q.place_fence(2, 'h', (6, 5)))

        # player 2 attempts to place fence at col 6 row 0
        self.assertFalse(q.place_fence(2, 'h', (6, 0)))

        # player 2 places fence at col 6 row 1
        self.assertTrue(q.place_fence(2, 'h', (6, 1)))  # player 2: 9 fences remaining

        # player 1 attempts to place fence at col 6 row 5
        self.assertFalse(q.place_fence(1, 'h', (6, 5)))

        # player 1 attempts to place fence at col 7 row 0
        self.assertFalse(q.place_fence(1, 'h', (7, 0)))

        # player 1 places fence at col 7 row 5
        self.assertTrue(q.place_fence(1, 'h', (7, 5)))  # player 1: 8 fences remaining

        # player 2 places fence at col 0 row 4
        self.assertTrue(q.place_fence(2, 'h', (0, 4)))  # player 2: 8 fences remaining

        # q.print_board()

        # ----------------------------- vertical tests ------------------------------------
        # player 1 places fence at col 6 row 5
        self.assertTrue(q.place_fence(1, 'v', (6, 5)))  # player 1: 7 fences remaining

        # player 1 attempts to place fence at col 7 row 5 out of turn
        self.assertFalse(q.place_fence(1, 'v', (7, 5)))

        # player 2 attempts to place fence at col 6 row 5
        self.assertFalse(q.place_fence(2, 'v', (6, 5)))

        # player 2 attempts to place fence at col 0 row 6
        self.assertFalse(q.place_fence(2, 'v', (0, 6)))

        # player 2 places fence at col 6 row 1
        self.assertTrue(q.place_fence(2, 'v', (6, 1)))  # player 2: 7 fences remaining

        # player 1 attempts to place fence at col 6 row 5
        self.assertFalse(q.place_fence(1, 'v', (6, 5)))

        # player 1 attempts to place fence at col 0 row 7
        self.assertFalse(q.place_fence(2, 'v', (0, 7)))

        # player 1 places fence at col 7 row 5
        self.assertTrue(q.place_fence(1, 'v', (7, 5)))  # player 1: 6 fences remaining

        # player 2 places fence at col 5 row 0
        self.assertTrue(q.place_fence(2, 'v', (5, 0)))  # player 2: 6 fences remaining

        # q.print_board()

        # ----------------------------- fence limit test ------------------------------------
        # player 1 places fence at col 8 row 5
        self.assertTrue(q.place_fence(1, 'v', (8, 5)))  # player 1: 5 fences remaining

        # player 2 places fence at col 4 row 0
        self.assertTrue(q.place_fence(2, 'v', (4, 0)))  # player 2: 5 fences remaining

        # player 1 places fence at col 4 row 4
        self.assertTrue(q.place_fence(1, 'h', (4, 4)))  # player 1: 4 fences remaining

        # player 2 places fence at col 4 row 8
        self.assertTrue(q.place_fence(2, 'h', (4, 8)))  # player 2: 4 fences remaining

        # player 1 places fence at col 1 row 4
        self.assertTrue(q.place_fence(1, 'h', (1, 4)))  # player 1: 3 fences remaining

        # player 2 places fence at col 1 row 8
        self.assertTrue(q.place_fence(2, 'h', (1, 8)))  # player 2: 3 fences remaining

        # player 1 places fence at col 2 row 4
        self.assertTrue(q.place_fence(1, 'h', (2, 4)))  # player 1: 2 fences remaining

        # player 2 places fence at col 2 row 8
        self.assertTrue(q.place_fence(2, 'h', (2, 8)))  # player 2: 2 fences remaining

        # player 1 places fence at col 3 row 4
        self.assertTrue(q.place_fence(1, 'h', (3, 4)))  # player 1: 1 fences remaining

        # player 2 places fence at col 3 row 8
        self.assertTrue(q.place_fence(2, 'h', (3, 8)))  # player 2: 1 fences remaining

        # player 1 places fence at col 3 row 4
        self.assertTrue(q.place_fence(1, 'v', (3, 4)))  # player 1: 0 fences remaining

        # player 2 places fence at col 3 row 8
        self.assertTrue(q.place_fence(2, 'v', (3, 8)))  # player 2: 0 fences remaining

        # player 1 places fence at col 3 row 7
        self.assertFalse(q.place_fence(1, 'v', (3, 7)))  # player 1: no fences!

        # player 2 places fence at col 3 row 7
        self.assertFalse(q.place_fence(2, 'v', (3, 7)))  # player 2: no fences!

        # q.print_board()

    def test_QuoridorGame_move_pawn(self):
        """Test move_pawn method"""

        # create game object
        q = QuoridorGame()

        # test bad input
        self.assertFalse(q.move_pawn(4, (4, 8)))  # no such player
        self.assertFalse(q.move_pawn('hi', (4, 1)))  # not an integer
        self.assertFalse(q.move_pawn(1, 'hi'))  # not a tuple
        self.assertFalse(q.move_pawn(1, ('hi', 1)))  # not a tuple
        self.assertFalse(q.move_pawn(1, (4, 9)))  # out of bounds!

        # ----------------------------- fence blocking test ------------------------------------
        # player 1 blocks player 2 pawn
        self.assertTrue(q.place_fence(1, 'h', (4, 8)))

        # player 2 attempts to move through fence
        self.assertFalse(q.move_pawn(2, (4, 7)))

        # player 2 attempts to move too far away
        self.assertFalse(q.move_pawn(2, (8, 7)))

        # player 2 attempts to move too far away
        self.assertFalse(q.move_pawn(2, (7, 8)))

        # player 2 sidesteps fence
        self.assertTrue(q.move_pawn(2, (5, 8)))

        # player 1 blocks player 2 pawn again
        self.assertTrue(q.place_fence(1, 'h', (5, 8)))

        # player 2 attempts to move through fence
        self.assertFalse(q.move_pawn(2, (5, 7)))

        # player 2 sidesteps fence
        self.assertTrue(q.move_pawn(2, (6, 8)))

        # player 1 attempts a diagonal move
        self.assertFalse(q.move_pawn(1, (5, 1)))

        # player 1 attempts to move off board
        self.assertFalse(q.move_pawn(1, (4, -1)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (4, 1)))

        # player 2 blocks player 1
        self.assertTrue(q.place_fence(2, 'h', (4, 2)))

        # player 1 attempts to move through fence
        self.assertFalse(q.move_pawn(1, (4, 2)))

        # player 1 sidesteps fence
        self.assertTrue(q.move_pawn(1, (5, 1)))

        # player 2 blocks player 1 again
        self.assertTrue(q.place_fence(2, 'v', (5, 1)))

        # player 1 attempts to move through fence
        self.assertFalse(q.move_pawn(1, (4, 1)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (5, 2)))

        # player 2 blocks player 1 again
        self.assertTrue(q.place_fence(2, 'v', (6, 2)))

        # player 1 attempts to move through fence
        self.assertFalse(q.move_pawn(1, (6, 2)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (5, 3)))

        # player 2 blocks player 1 backward movement
        self.assertTrue(q.place_fence(2, 'h', (5, 3)))

        # player 1 attempts to move through fence
        self.assertFalse(q.move_pawn(1, (5, 2)))

        # q.print_board()

        # ----------------------------- pawn face-off test ------------------------------------

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (5, 4)))

        # player 2 moves
        self.assertTrue(q.move_pawn(2, (6, 7)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (5, 5)))

        # player 2 moves
        self.assertTrue(q.move_pawn(2, (6, 6)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (5, 6)))  # face-off

        # player 2 attempts to move into opponent
        self.assertFalse(q.move_pawn(2, (5, 6)))

        # player 2 attempts to move diagonally with no fence
        self.assertFalse(q.move_pawn(2, (5, 5)))

        # player 2 jumps over opponent
        self.assertTrue(q.move_pawn(2, (4, 6)))

        # player 1 jumps over opponent
        self.assertTrue(q.move_pawn(1, (3, 6)))

        # player 2 drops a fence behind player 1
        self.assertTrue(q.place_fence(2, 'v', (5, 6)))

        # player 1 places fence
        self.assertTrue(q.place_fence(1, 'h', (4, 7)))

        # player 2 places fence
        self.assertTrue(q.place_fence(2, 'h', (8, 3)))

        # player 1 attempts illegal jump
        self.assertFalse(q.move_pawn(1, (5, 6)))

        # player 1 attempts illegal diagonal
        self.assertFalse(q.move_pawn(1, (4, 7)))

        # player 1 moves diagonally
        self.assertTrue(q.move_pawn(1, (4, 5)))

        # player 2 fences themselves into a corner
        self.assertTrue(q.place_fence(2, 'v', (4, 6)))

        # player 1 attempts illegal jump
        self.assertFalse(q.move_pawn(1, (4, 7)))

        # player 1 attempts illegal diagonal
        self.assertFalse(q.move_pawn(1, (5, 6)))

        # player 1 attempts illegal diagonal to the other side
        self.assertFalse(q.move_pawn(1, (3, 6)))

        # player 1 places fence behind themself
        self.assertTrue(q.place_fence(1, 'h', (4, 5)))

        # player 2 moves diagonally
        self.assertTrue(q.move_pawn(2, (5, 5)))

        # player 1 places fence behind player 2
        self.assertTrue(q.place_fence(1, 'v', (6, 5)))

        # player 2 places fence
        self.assertTrue(q.place_fence(2, 'h', (5, 4)))

        # player 1 moves diagonally
        self.assertTrue(q.move_pawn(1, (5, 4)))

        # player 2 places fence
        self.assertTrue(q.place_fence(2, 'v', (6, 4)))

        # player 1 places fence
        self.assertTrue(q.place_fence(1, 'v', (7, 4)))

        # player 2 attempts illegal diagonal
        self.assertFalse(q.move_pawn(2, (6, 4)))

        # player 2 moves diagonally
        self.assertTrue(q.move_pawn(2, (4, 4)))

        # q.print_board()

    def test_QuoridorGame_diagonal_edge_case(self):
        """Test all edge cases for diagonal move."""

        # ----------------------------- illegal vertical test ------------------------------------
        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 1), (4, 2))

        # fence setup
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'h', (4, 1)))
        self.assertTrue(q.place_fence(1, 'v', (4, 2)))
        self.assertTrue(q.place_fence(2, 'v', (4, 1)))
        self.assertTrue(q.place_fence(1, 'v', (5, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 1)))

        # test diagonal moves player 1
        self.assertFalse(q.move_pawn(1, (5, 2)))
        self.assertFalse(q.move_pawn(1, (3, 2)))
        self.assertTrue(q.place_fence(1, 'h', (6, 4)))

        # test diagonal moves player 2
        self.assertFalse(q.move_pawn(2, (5, 1)))
        self.assertFalse(q.move_pawn(2, (3, 1)))

        # start new game, no fences
        q = QuoridorGame()
        q.change_pawn_loc((4, 1), (4, 2))

        # test diagonal moves player 1
        self.assertFalse(q.move_pawn(1, (5, 2)))
        self.assertFalse(q.move_pawn(1, (3, 2)))
        self.assertTrue(q.place_fence(1, 'h', (6, 4)))

        # test diagonal moves player 2
        self.assertFalse(q.move_pawn(2, (5, 1)))
        self.assertFalse(q.move_pawn(2, (3, 1)))

        # q.print_board()

        # ----------------------------- legal vertical test ------------------------------------
        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 1), (4, 2))

        # place fences
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'h', (4, 1)))

        # test diagonal moves player 1
        self.assertTrue(q.move_pawn(1, (5, 2)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 1), (4, 2))

        # place fences
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'h', (4, 1)))

        # test diagonal moves player 1
        self.assertTrue(q.move_pawn(1, (3, 2)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 1), (4, 2))

        # place fences
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'h', (4, 1)))
        self.assertTrue(q.place_fence(1, 'h', (2, 7)))

        # test diagonal moves player 2
        self.assertTrue(q.move_pawn(2, (5, 1)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 1), (4, 2))

        # place fences
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'h', (4, 1)))
        self.assertTrue(q.place_fence(1, 'h', (2, 7)))

        # q.print_board()

        # ----------------------------- illegal horizontal test ------------------------------------
        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # fence setup
        self.assertTrue(q.place_fence(1, 'v', (3, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 2)))
        self.assertTrue(q.place_fence(1, 'h', (4, 2)))
        self.assertTrue(q.place_fence(2, 'h', (3, 2)))
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'h', (3, 3)))

        # test diagonal moves player 1
        self.assertFalse(q.move_pawn(1, (4, 1)))
        self.assertFalse(q.move_pawn(1, (4, 3)))
        self.assertTrue(q.place_fence(1, 'h', (6, 4)))

        # test diagonal moves player 2
        self.assertFalse(q.move_pawn(2, (3, 1)))
        self.assertFalse(q.move_pawn(2, (3, 3)))

        # start new game, no fences
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # test diagonal moves player 1
        self.assertFalse(q.move_pawn(1, (4, 1)))
        self.assertFalse(q.move_pawn(1, (4, 3)))
        self.assertTrue(q.place_fence(1, 'h', (6, 4)))

        # test diagonal moves player 2
        self.assertFalse(q.move_pawn(2, (3, 1)))
        self.assertFalse(q.move_pawn(2, (3, 3)))

        # q.print_board()

        # ----------------------------- legal horizontal test ------------------------------------
        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # fence setup
        self.assertTrue(q.place_fence(1, 'v', (3, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 2)))

        # test diagonal moves player 1
        self.assertTrue(q.move_pawn(1, (4, 1)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # fence setup
        self.assertTrue(q.place_fence(1, 'v', (3, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 2)))

        # test diagonal moves player 1
        self.assertTrue(q.move_pawn(1, (4, 3)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # fence setup
        self.assertTrue(q.place_fence(1, 'v', (3, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 2)))
        self.assertTrue(q.place_fence(1, 'h', (2, 7)))

        # test diagonal moves player 2
        self.assertTrue(q.move_pawn(2, (3, 1)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # fence setup
        self.assertTrue(q.place_fence(1, 'v', (3, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 2)))
        self.assertTrue(q.place_fence(1, 'h', (2, 7)))

        # test diagonal moves player 2
        self.assertTrue(q.move_pawn(2, (3, 3)))

        # q.print_board()

        # ----------------------------- double fence test ------------------------------------
        # start new game horizontal test
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # fence setup
        self.assertTrue(q.place_fence(1, 'v', (4, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 2)))

        self.assertFalse(q.move_pawn(1, (4, 1)))
        # player 1 drops fence
        self.assertTrue(q.place_fence(1, 'v', (3, 2)))

        # test diagonal moves player 2
        self.assertFalse(q.move_pawn(1, (3, 1)))

        q.print_board()

        # start new game vertical test
        q = QuoridorGame()
        q.change_pawn_loc((4, 1), (4, 2))

        # place fences
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'h', (4, 2)))

        # test diagonal moves player 1
        self.assertFalse(q.move_pawn(1, (3, 2)))
        # player 1 drops fence
        self.assertTrue(q.place_fence(1, 'h', (4, 1)))

        # test diagonal moves player 2
        self.assertFalse(q.move_pawn(1, (5, 1)))

        # q.print_board()

    def test_QuoridorGame_orthogonal_edge_case(self):
        """Test all edge cases for horizontal move."""

        # ----------------------------- illegal horizontal test ------------------------------------
        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # double fence setup
        self.assertTrue(q.place_fence(1, 'v', (4, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 2)))

        # test jump right player 1
        self.assertFalse(q.move_pawn(1, (5, 2)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # double fence setup
        self.assertTrue(q.place_fence(1, 'v', (4, 2)))
        self.assertTrue(q.place_fence(2, 'v', (3, 2)))
        self.assertTrue(q.place_fence(1, 'h', (5, 6)))

        # test jump left player 2
        self.assertFalse(q.move_pawn(2, (2, 2)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # single fence setup close
        self.assertTrue(q.place_fence(1, 'v', (4, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 7)))

        # test jump right player 1
        self.assertFalse(q.move_pawn(1, (5, 2)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # single fence setup far
        self.assertTrue(q.place_fence(1, 'v', (5, 2)))
        self.assertTrue(q.place_fence(2, 'v', (5, 7)))

        # test jump right player 1
        self.assertFalse(q.move_pawn(1, (5, 2)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # single fence setup close
        self.assertTrue(q.place_fence(1, 'v', (4, 2)))

        # test jump left player 2
        self.assertFalse(q.move_pawn(2, (2, 2)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # single fence setup far
        self.assertTrue(q.place_fence(1, 'v', (3, 2)))

        # test jump left player 2
        self.assertFalse(q.move_pawn(2, (2, 2)))

        # start new game with pawns far apart
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (7, 2))

        # test jump right player 1
        self.assertFalse(q.move_pawn(1, (5, 2)))

        # test far jump right player 1
        self.assertFalse(q.move_pawn(1, (6, 2)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (2, 2)))

        # test jump left player 2
        self.assertFalse(q.move_pawn(2, (5, 2)))

        # test far jump left player 2
        self.assertFalse(q.move_pawn(2, (4, 2)))

        # start new game with pawns at edge of board
        q = QuoridorGame()
        q.change_pawn_loc((0, 4), (1, 4))

        # player 1 places fence
        self.assertTrue(q.place_fence(1, 'v', (7, 7)))

        # player 2 attempts to jump off board
        self.assertFalse(q.move_pawn(2, (-1, 4)))

        # start new game with pawns at edge of board
        q = QuoridorGame()
        q.change_pawn_loc((7, 4), (8, 4))

        # player 1 attempts to jump off board
        self.assertFalse(q.move_pawn(1, (9, 4)))

        # ----------------------------- legal horizontal test ------------------------------------
        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((3, 2), (4, 2))

        # jump right player 1
        self.assertTrue(q.move_pawn(1, (5, 2)))

        # player 2 places fence
        self.assertTrue(q.place_fence(2, 'v', (7, 7)))

        # jump left player 1
        self.assertTrue(q.move_pawn(1, (3, 2)))

        # jump left player 2
        self.assertTrue(q.move_pawn(2, (2, 2)))

        # ----------------------------- illegal vertical test ------------------------------------
        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 2), (4, 3))

        # double fence setup
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'h', (4, 4)))

        # test jump down player 1
        self.assertFalse(q.move_pawn(1, (4, 4)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 2), (4, 3))

        # double fence setup
        self.assertTrue(q.place_fence(1, 'h', (4, 2)))
        self.assertTrue(q.place_fence(2, 'h', (4, 3)))
        self.assertTrue(q.place_fence(1, 'h', (5, 6)))

        # test jump up player 2
        self.assertFalse(q.move_pawn(2, (4, 1)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 2), (4, 3))

        # single fence setup close
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))
        self.assertTrue(q.place_fence(2, 'v', (5, 7)))

        # test jump down player 1
        self.assertFalse(q.move_pawn(1, (4, 4)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 2), (4, 3))

        # single fence setup far
        self.assertTrue(q.place_fence(1, 'h', (4, 4)))
        self.assertTrue(q.place_fence(2, 'v', (5, 7)))

        # test jump down player 1
        self.assertFalse(q.move_pawn(1, (4, 4)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 2), (4, 3))

        # single fence setup close
        self.assertTrue(q.place_fence(1, 'h', (4, 3)))

        # test jump up player 2
        self.assertFalse(q.move_pawn(1, (4, 1)))

        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 2), (4, 3))

        # single fence setup far
        self.assertTrue(q.place_fence(1, 'h', (4, 2)))

        # test jump up player 2
        self.assertFalse(q.move_pawn(1, (4, 1)))

        # start new game with pawns far apart
        q = QuoridorGame()
        q.change_pawn_loc((3, 3), (7, 3))

        # test jump up player 1
        self.assertFalse(q.move_pawn(1, (3, 1)))

        # test far jump up player 1
        self.assertFalse(q.move_pawn(1, (3, 0)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (3, 2)))

        # test jump down player 2
        self.assertFalse(q.move_pawn(2, (7, 5)))

        # test far jump down player 2
        self.assertFalse(q.move_pawn(2, (7, 6)))

        # start new game with pawns at edge of board
        q = QuoridorGame()
        q.change_pawn_loc((4, 0), (4, 1))

        # player 1 places fence
        self.assertTrue(q.place_fence(1, 'v', (7, 7)))

        # player 2 attempts to jump off board
        self.assertFalse(q.move_pawn(2, (4, -1)))

        # start new game with pawns at edge of board
        q = QuoridorGame()
        q.change_pawn_loc((4, 7), (4, 8))

        # player 1 attempts to jump off board
        self.assertFalse(q.move_pawn(1, (4, 9)))

        # ----------------------------- legal vertical test ------------------------------------
        # start new game
        q = QuoridorGame()
        q.change_pawn_loc((4, 2), (4, 3))

        # jump down player 1
        self.assertTrue(q.move_pawn(1, (4, 4)))

        # player 2 places fence
        self.assertTrue(q.place_fence(2, 'v', (7, 7)))

        # jump up player 1
        self.assertTrue(q.move_pawn(1, (4, 2)))

        # jump up player 2
        self.assertTrue(q.move_pawn(2, (4, 1)))

        #  player 1 places fence
        self.assertTrue(q.place_fence(1, 'h', (7, 7)))

        # jump down player 2
        self.assertTrue(q.move_pawn(2, (4, 3)))

        # ----------------------------- edge of board test ------------------------------------

        # start new game left-right test
        q = QuoridorGame()
        q.change_pawn_loc((0, 2), (8, 2))

        # player 1 attempts to move off board
        self.assertFalse(q.move_pawn(1, (-1, 2)))

        # player 1 attempts to jump off board
        self.assertFalse(q.move_pawn(1, (-2, 2)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (1, 2)))

        # player 2 attempts to move off board
        self.assertFalse(q.move_pawn(2, (9, 2)))

        # player 2 attempts to jump off board
        self.assertFalse(q.move_pawn(2, (10, 2)))

        # start new game up-down test
        q = QuoridorGame()
        q.change_pawn_loc((2, 0), (2, 8))

        # player 1 attempts to move off board
        self.assertFalse(q.move_pawn(1, (2, -1)))

        # player 1 attempts to jump off board
        self.assertFalse(q.move_pawn(1, (2, -2)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (2, 1)))

        # player 2 attempts to move off board
        self.assertFalse(q.move_pawn(2, (2, 9)))

        # player 2 attempts to jump off board
        self.assertFalse(q.move_pawn(2, (2, 10)))

        # q.print_board()

        # start new game pawn adjacent test jump up
        q = QuoridorGame()
        q.change_pawn_loc((2, 1), (2, 0))

        # player 1 attempts to jump off board
        self.assertFalse(q.move_pawn(1, (2, -1)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (2, 2)))

        # start new game pawn adjacent test jump down
        q = QuoridorGame()
        q.change_pawn_loc((2, 7), (2, 8))

        # player 1 attempts to jump off board
        self.assertFalse(q.move_pawn(1, (2, 9)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (2, 6)))

        # start new game pawn adjacent test jump right
        q = QuoridorGame()
        q.change_pawn_loc((7, 2), (8, 2))

        # player 1 attempts to jump off board
        self.assertFalse(q.move_pawn(1, (9, 2)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (6, 2)))

        # start new game pawn adjacent test jump left
        q = QuoridorGame()
        q.change_pawn_loc((1, 2), (0, 2))

        # player 1 attempts to jump off board
        self.assertFalse(q.move_pawn(1, (-1, 2)))

        # player 1 moves
        self.assertTrue(q.move_pawn(1, (2, 2)))

        # q.print_board()

    def test_is_winner(self):
        """Test the is_winner method."""

        # ----------------------------- win condition test ------------------------------------

        # start new game with pawns close to win
        q = QuoridorGame()
        q.change_pawn_loc((4, 7), (4, 1))
        # player 1 wins
        self.assertTrue(q.move_pawn(1, (4, 8)))
        # check is_winner
        self.assertTrue(q.is_winner(1))
        # player 2 tries to move, but game is over
        self.assertFalse(q.move_pawn(2, (4, 0)))
        # player 2 tries to place a fence, but game is over
        self.assertFalse(q.place_fence(2, 'v', (4, 4)))

        # q.print_board()

        # start new game with pawns close to win
        q = QuoridorGame()
        q.change_pawn_loc((4, 7), (4, 1))
        # player 1 moves
        self.assertTrue(q.move_pawn(1, (3, 7)))
        # check is_winner
        self.assertFalse(q.is_winner(1))
        # player 2 wins
        self.assertTrue(q.move_pawn(2, (4, 0)))
        # check is_winner
        self.assertTrue(q.is_winner(2))
        # player 1 tries to win, but the game is over
        self.assertFalse(q.move_pawn(1, (3, 8)))
        # player 1 tries to place a fence, but the game is over
        self.assertFalse(q.place_fence(1, 'h', (3, 8)))

        # q.print_board()

        # start new game, players attempt to win on the wrong side of the board
        q = QuoridorGame()
        q.change_pawn_loc((4, 1), (4, 7))
        # player 1 moves
        self.assertTrue(q.move_pawn(1, (4, 0)))
        # check is_winner
        self.assertFalse(q.is_winner(1))
        # player 2 wins
        self.assertTrue(q.move_pawn(2, (4, 8)))
        # check is_winner
        self.assertFalse(q.is_winner(2))
