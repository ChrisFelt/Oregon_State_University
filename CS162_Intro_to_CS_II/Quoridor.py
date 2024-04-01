# Author: Christopher Felt
# Date: 8/04/2021
#
# Description: Program for playing a board game called Quoridor. Players use the move_pawn and place_fence methods in
# the QuoridorGame class to play the game. Additionally, players can use is_winner in the QuoridorGame class to check
# who the winner of the current game is, if any.
#
# The QuoridorGame Class uses the Player, Board, and Cell classes to play the game. The Player class represents a player
# of the game, and contains the player's ID, number of fences remaining (start with 10), and the location of their pawn
# on the board. The Board class contains a nested dictionary of rows for each column, and a Cell object for each
# row-column coordinate (board is 9x9 cells) The dictionary is automatically populated with Cells when the Board object
# is created. The Cell class represents an individual cell for the board, and contains data on its sides - whether it
# is on the edge of the board, and whether there is a fence on that side, and also tracks whether a pawn is present in
# the cell.
#
# See the following link for game rules:
# https://en.gigamic.com/files/media/fiche_pedagogique/educative-sheet_quoridor-english.pdf
#

class Cell:
    """Represents a cell on a Quoridor game board. Holds a dictionary of the four borders of the cell for board edges
    and placement of fences. When the Cell object is created, the initial values for the fences must be passed: None is
    assigned to the edges of the board, and False is assigned to all other borders (a True value means a fence exists
    on that border)."""
    # initialize data members
    def __init__(self, top, right, bot, left):
        self._fence = {"top": top,  # fence values for the borders of the cell. None = edge of board.
                       "right": right,  # False = no fence. True = fence.
                       "bot": bot,
                       "left": left}

        self._pawn = False  # pawn present in cell

    def get_fence(self, side):
        """Takes a string corresponding with one of the keys in the self._fence dictionary and returns the value for
        that key."""
        return self._fence[side]

    def set_fence(self, side):
        """Takes a string that corresponds with one of the keys in the self._fence dictionary and sets the value for
        that key to True. Returns nothing."""
        self._fence[side] = True

    def set_pawn(self, value):
        """Takes a Boolean and sets self._pawn to that value. Returns nothing."""
        self._pawn = value

    def get_pawn(self):
        """Takes no parameters and returns self._pawn."""
        return self._pawn


class Board:
    """Represents a board for a Quoridor game. Has a compositional relationship with the Cell class; upon creation,
    generates and holds a nested dictionary containing Cell objects for each cell of the board. The board and its
    cells are used by the QuoridorGame class to make moves and place fences."""
    # initialize data members
    def __init__(self):
        self._cells = {}  # create empty cells dictionary
        self.__generate_cells()  # call generate cells to create the cell dictionary

    def __generate_cells(self):
        """Contains a nested loop: 1 outer loop that iterates through each column and 1 inner loop that iterates
        through each row. Adds a nested dictionary entry to self._cells for each column (key is column number, value is
        a dictionary). The nested dictionary in turn contains the row number as key and a cell object is generated as
        the value. Cell object's fence will be set to None where the edge of the board lies and False for all other cell
        borders."""
        # iterate through columns
        for col in range(9):
            self._cells[col] = {}  # nested empty dictionary with col as key

            # iterate through rows
            for row in range(9):
                # initialize cell borders
                if col == 0:  # set left side of cell
                    left = None  # edge of board
                else:
                    left = False  # no fence, inside of board

                if col == 8:  # set right side of cell
                    right = None
                else:
                    right = False

                if row == 0:  # set top of cell
                    top = None
                else:
                    top = False

                if row == 8:  # set bottom of cell
                    bot = None
                else:
                    bot = False
                # create Cell object as the value with row as key
                self._cells[col][row] = Cell(top, right, bot, left)

    def get_cell(self, coord):
        """Takes a tuple with integer values for column and row as the parameter and returns a Cell object at the
        dictionary location corresponding with those coordinates."""
        return self._cells[coord[0]][coord[1]]  # return cell object at coord


class Player:
    """Represents a player for the Quoridor game, with an initial ID and pawn location as specified by the initial
    parameters passed. The player also has an initial fences value of 10. The Player class is used by the QuoridorGame
    class to hold and manipulate these values in a single object."""
    # initialize data members
    def __init__(self, player_id, pawn_loc):
        self._player_id = player_id  # player number (e.g., 1, 2)
        self._pawn_loc = pawn_loc  # cell coordinates of current pawn location
        self._fences = 10  # starting fences

    def set_pawn_loc(self, coord):
        """Takes a tuple with integer values for column and row as the parameter and sets the self._pawn_loc data member
         to it. Returns nothing."""
        self._pawn_loc = coord

    def get_pawn_loc(self):
        """Takes no parameters and returns self._pawn_loc."""
        return self._pawn_loc

    def get_fences(self):
        """Takes no parameters and returns self._fences."""
        return self._fences

    def use_fence(self):
        """Takes no parameters. Reduces self._fences count by 1. Returns nothing."""
        self._fences -= 1


class QuoridorGame:
    """Represents a Quoridor game. Has a compositional relationship with the Player and Board classes; these classes are
    used to store much of the necessary data to play the game. The QuoridorGame calls these classes when it is
    initialized to create a board and two player objects. The game is played through the use of the QuoridorGame methods
    move_pawn and place_fence. Game status can be checked with the is_winner method."""
    # initialize data members
    def __init__(self):
        self._board = Board()  # generate game board object with Game class

        # generate dictionary of player objects. pass initial pawn locations
        self._players = {1: Player(1, (4, 0)),
                         2: Player(2, (4, 8))}

        # initialize pawn locations
        self._board.get_cell((4, 0)).set_pawn(True)
        self._board.get_cell((4, 8)).set_pawn(True)

        self._winner = None  # track winner of the game. can be None, 1, or 2
        self._player_turn = 1  # track turn. player 1 goes first

    def is_winner(self, player):
        """Given an integer that represents the player, checks if self._winner is equal to that integer. If it is,
        returns True. Otherwise, returns False."""
        # check if player passed is the winner
        if self._winner == player:
            return True

        else:
            return False

    def move_pawn(self, player, coord):
        """Given an integer that represents the player and a tuple of the coordinate location of the attempted
        attempted move, calls the check_initial_parameters and check_move_legality methods to determine if values
        passed and movement are valid. If they aren't, returns False. Otherwise, moves the pawn to the target cell,
        checks the win conditions, changes the turn, and returns True."""
        # check game status, values passed, and player turn with check_initial_parameters method
        if not self.__check_initial_parameters(player, coord):
            return False  # failed basic checks!

        # check if move is illegal with check_move_legality method
        if not self.__check_move_legality(player, coord):
            return False  # illegal move

        else:
            # move pawn to new cell
            self._board.get_cell(coord).set_pawn(True)
            # remove pawn from last cell
            self._board.get_cell(self._players[player].get_pawn_loc()).set_pawn(False)
            # update player's pawn location
            self._players[player].set_pawn_loc(coord)

            # check if this move resulted in a win
            if self.__check_win_condition(player):
                return True  # turn is not changed

            # change the turn
            self.__change_turn()

            return True

    def place_fence(self, player, orient, coord):
        """Given an integer that represents the player, a character (v or h) that represents orientation, and a tuple of
        the coordinate location of the attempted fence placement, calls the check_initial_parameters and
        check_fence_legality methods to determine if values passed and fence placement are valid. If they aren't returns
        False. Otherwise, places the fence in the target cell, reduces the player's fences by 1, changes the turn, and
        returns True."""
        # check initial parameters
        if not self.__check_initial_parameters(player, coord, orient):
            return False

        # check if fence placement legal
        if not self.__check_fence_legality(orient, coord):
            return False

        # check if orientation horizontal
        if orient == 'h':
            self._board.get_cell(coord).set_fence("top")  # place fence at top of target cell
            # place another fence at bottom of cell above target cell
            self._board.get_cell((coord[0], coord[1] - 1)).set_fence("bot")

        # check if orientation vertical
        if orient == 'v':
            self._board.get_cell(coord).set_fence("left")  # place fence on left side of target cell
            # place another fence on the right side of cell to the left of target cell
            self._board.get_cell((coord[0] - 1, coord[1])).set_fence("right")

        # use player's fence
        self._players[player].use_fence()

        # change turns
        self.__change_turn()

        return True  # fence placed successfully!

    def __check_fence_legality(self, orient, coord):
        """Given a character (v or h) that represents orientation, and a tuple of the coordinate location of the
        attempted fence placement, returns False if the player is out of fences, or if the fence placement was illegal.
        Otherwise returns True."""
        # check player's remaining fences
        if self._players[self._player_turn].get_fences() < 1:
            return False  # not enough fences!

        # check if horizontal orientation
        if orient == 'h':
            if coord[1] == 0:  # check if row is 0
                return False  # can't place fence on edge of board!

            if self._board.get_cell(coord).get_fence("top"):  # check if fence already in target side of cell
                return False

            else:
                return True  # legal fence placement

        # check if vertical orientation
        if orient == 'v':
            if coord[0] == 0:  # check if col is 0
                return False  # can't place fence on edge of board!

            if self._board.get_cell(coord).get_fence("left"):  # check if fence already in target side of cell
                return False

            else:
                return True  # legal fence placement

    def __check_move_legality(self, player, coord):
        """Given an integer that represents the player and a tuple of the coordinate locations of the attempted move,
        returns True if the move was legal by calling the orthogonal_move and diagonal_move methods. Otherwise returns
        False."""
        # check for opponent's pawn in destination cell
        if self._board.get_cell(coord).get_pawn():
            return False

        # call orthogonal_move function to check if move is orthogonal and no fences block the way
        orthogonal = self.__orthogonal_move(player, coord)
        if orthogonal:
            return True  # move was orthogonal and legal!

        # if move was NOT orthogonal, call diagonal_move to check if move is diagonal and legal
        if orthogonal is None:
            if self.__diagonal_move(player, coord):
                return True  # move was diagonal and legal!

        else:
            return False  # illegal move

    def __orthogonal_move(self, player, coord):
        """Given an integer that represents the player and a tuple of the coordinate location of the attempted move,
        returns True if the move was orthogonal and legal. Returns False if the move was orthogonal and illegal. Returns
        None if the move was not orthogonal."""
        pawn_coord = self._players[player].get_pawn_loc()  # current player's pawn coordinates

        if player == 1:
            enemy_pawn = self._players[2].get_pawn_loc()

        else:
            enemy_pawn = self._players[1].get_pawn_loc()

        # check if direction of move is orthogonal
        standard_orthogonal = self.__orthogonal_move_standard(coord, pawn_coord)
        if standard_orthogonal:
            return True

        # check if direction of move is orthogonal and move is a jump over enemy pawn
        jump_orthogonal = self.__orthogonal_move_jump(coord, pawn_coord, enemy_pawn)
        if jump_orthogonal:
            return True

        if standard_orthogonal is None and jump_orthogonal is None:
            return None  # not orthogonal

        else:
            return False

    def __orthogonal_move_standard(self, coord, pawn_coord):
        """Given the coordinates of the move and the pawn coordinates of the current player both as tuples, finds
        direction of move and returns a call of the orthogonal_fence_check method. Returns None if the move is not
        orthogonally adjacent to the player's pawn."""
        # find direction of movement if orthogonal
        if pawn_coord[0] + 1 == coord[0] and pawn_coord[1] == coord[1]:  # moving to right
            return self.__orthogonal_fence_check(pawn_coord, "right")

        if pawn_coord[0] - 1 == coord[0] and pawn_coord[1] == coord[1]:  # moving to left
            return self.__orthogonal_fence_check(pawn_coord, "left")

        if pawn_coord[0] == coord[0] and pawn_coord[1] + 1 == coord[1]:  # moving down
            return self.__orthogonal_fence_check(pawn_coord, "bot")

        if pawn_coord[0] == coord[0] and pawn_coord[1] - 1 == coord[1]:  # moving up
            return self.__orthogonal_fence_check(pawn_coord, "top")

    def __orthogonal_move_jump(self, coord, pawn_coord, enemy_pawn):
        """Given target coordinates, player's pawn coordinates, and enemy pawn coordinates each as a tuple, finds the
        direction of the move and returns a call of the orthogonal_fence_check method. Returns None if the move is not
        orthogonally two spaces away from the player's pawn"""
        # check if attempting orthogonal jump
        if pawn_coord[0] + 2 == coord[0] and pawn_coord[1] == coord[1]:  # moving to right
            adjacent = (pawn_coord[0] + 1, pawn_coord[1])  # bookmark cell being jumped
            return self.__orthogonal_fence_check(pawn_coord, "right", enemy_pawn, adjacent)  # check the way

        if pawn_coord[0] - 2 == coord[0] and pawn_coord[1] == coord[1]:  # moving to left
            adjacent = (pawn_coord[0] - 1, pawn_coord[1])  # bookmark cell being jumped
            return self.__orthogonal_fence_check(pawn_coord, "left", enemy_pawn, adjacent)  # check the way

        if pawn_coord[0] == coord[0] and pawn_coord[1] + 2 == coord[1]:  # moving down
            adjacent = (pawn_coord[0], pawn_coord[1] + 1)  # bookmark cell being jumped
            return self.__orthogonal_fence_check(pawn_coord, "bot", enemy_pawn, adjacent)  # check the way

        if pawn_coord[0] == coord[0] and pawn_coord[1] - 2 == coord[1]:  # moving up
            adjacent = (pawn_coord[0], pawn_coord[1] - 1)  # bookmark cell being jumped
            return self.__orthogonal_fence_check(pawn_coord, "top", enemy_pawn, adjacent)  # check the way

    def __orthogonal_fence_check(self, pawn_coord, side, enemy_pawn=None, adjacent=None):
        """Given pawn_coord as a tuple, a side of a cell as a string for a standard orthogonal move, and enemy_pawn
        coordinates as a tuple and the coordinates of the adjacent cell as a tuple in addition for jump moves, returns
        False if a fence bars the way. Otherwise returns True."""
        # jump orthogonal fence check
        if enemy_pawn is not None and adjacent is not None:
            # check if opposing pawn adjacent in direction of jump
            if enemy_pawn != adjacent:
                return False

            # check given side of player pawn's cell AND enemy pawn's cell
            if self._board.get_cell(pawn_coord).get_fence(side) or self._board.get_cell(enemy_pawn).get_fence(side):
                return False  # fence in the way!
            else:
                return True  # the way is clear

        # standard orthogonal fence check
        else:
            if self._board.get_cell(pawn_coord).get_fence(side):  # check given side of current cell
                return False  # fence in the way!
            else:
                return True  # the way is clear

    def __diagonal_move(self, player, coord):
        """Given an integer that represents the player and a tuple of the coordinate location of the attempted move,
        calls the diagonal_move_vertical and/or the diagonal_move_horizontal methods to check direction of move
        relative to the enemy pawn, then returns True if the move was legal and not blocked by a fence. Otherwise,
        returns False."""
        pawn_coord = self._players[player].get_pawn_loc()  # current player's pawn coordinates
        tar_cell = self._board.get_cell(coord)  # destination cell object

        # call diagonal_move_vertical method to check vertical conditions
        if self.__diagonal_move_vertical(coord, pawn_coord, -1, "top") or \
                self.__diagonal_move_vertical(coord, pawn_coord, 1, "bot"):

            # check if move is to the left
            if pawn_coord[0] - 1 == coord[0]:
                if not tar_cell.get_fence("right"):  # check if fence in the way
                    return True  # move valid!

            # check if move is to the right
            elif pawn_coord[0] + 1 == coord[0]:
                if not tar_cell.get_fence("left"):  # check if fence in the way
                    return True  # move valid!

            else:
                return False  # illegal move

        # call diagonal_move_vertical method to check horizontal conditions
        if self.__diagonal_move_horizontal(coord, pawn_coord, -1, "left") or \
                self.__diagonal_move_horizontal(coord, pawn_coord, 1, "right"):

            # check if move is up
            if pawn_coord[1] - 1 == coord[1]:
                if not tar_cell.get_fence("bot"):  # check if fence in the way
                    return True  # move valid!

            # check if move is down
            elif pawn_coord[1] + 1 == coord[1]:
                if not tar_cell.get_fence("top"):  # check if fence in the way
                    return True  # move valid!

            else:
                return False  # illegal move

    def __diagonal_move_vertical(self, coord, pawn_coord, value, side):
        """Given a tuple of two integers representing coordinates, the coordinates of the current player's pawn,
        an integer value 1 or -1, returns True/False for each of the following checks: 1) move is vertical, 2) opposing
        pawn is vertically adjacent, 3) a fence is behind the opposing pawn, and 4) no fence in between
        player's pawn and opposing pawn."""
        # make sure cells checked are not out of bounds
        if pawn_coord[1] + value not in range(9):
            return False

        # check if move is up or down
        direc = pawn_coord[1] + value == coord[1]
        # check if opposing pawn orthogonally up or down and adjacent
        enemy_pawn = self._board.get_cell((pawn_coord[0], pawn_coord[1] + value)).get_pawn()
        # check if fence behind opposing pawn
        far_fence = self._board.get_cell((pawn_coord[0], pawn_coord[1] + value)).get_fence(side)
        # check if fence in the way in current player's pawn's cell
        adjacent_fence = not self._board.get_cell(pawn_coord).get_fence(side)

        return direc and enemy_pawn and far_fence and adjacent_fence

    def __diagonal_move_horizontal(self, coord, pawn_coord, value, side):
        """Given a tuple of two integers representing coordinates, the coordinates of the current player's pawn,
        an integer value 1 or -1, returns True/False for each of the following checks: 1) move is horizontal, 2)
        opposing pawn is horizontally adjacent, 3) a fence is behind the opposing pawn, and 4) no fence in between
        player's pawn and opposing pawn."""
        # make sure cells checked are not out of bounds
        if pawn_coord[0] + value not in range(9):
            return False

        # check if move is left or right
        direc = pawn_coord[0] + value == coord[0]
        # check if opposing pawn orthogonally left or right and adjacent
        enemy_pawn = self._board.get_cell((pawn_coord[0] + value, pawn_coord[1])).get_pawn()
        # check if fence behind opposing pawn
        far_fence = self._board.get_cell((pawn_coord[0] + value, pawn_coord[1])).get_fence(side)
        # check if fence in the way in current player's pawn's cell
        adjacent_fence = not self._board.get_cell(pawn_coord).get_fence(side)

        return direc and enemy_pawn and far_fence and adjacent_fence

    def __check_win_condition(self, player):
        """Given an integer that represents the player, returns True if win conditions have been met. Otherwise returns
        False."""
        # if player 1, check if win conditions have been met
        if player == 1 and self._players[1].get_pawn_loc()[1] == 8:
            self._winner = 1
            return True

        # if player 2, check if win conditions have been met
        if player == 2 and self._players[2].get_pawn_loc()[1] == 0:
            self._winner = 2
            return True

        return False  # no winners yet

    def __check_initial_parameters(self, player, coord, orient=None):
        """Given an integer that represents the player, a tuple of the coordinate location of the attempted fence
        placement, and a character (v or h) that represents orientation (optional; default is None), returns False if:
        1) the game has been won, 2) it is not the player's turn, or 3) player or coord input is invalid (i.e., wrong
        data type, or not in the expected format). Otherwise returns True."""
        # check game status
        if self._winner is not None:
            return False  # game is over!

        # check if it's the player's turn
        if self._player_turn != player:
            return False

        # check if coord is a tuple and contains two integers
        if type(coord) is tuple:
            if len(coord) == 2:
                if type(coord[0]) is int and type(coord[1]) is int:
                    if coord[0] not in range(9) or coord[1] not in range(9):  # check if coord is inside board
                        return False  # out of bounds!

                else:
                    return False  # tuple elements not integers!

            else:
                return False  # tuple does not contain exactly two elements!

        else:
            return False  # not a tuple!

        # check if orient variable passed
        if orient is not None:
            if orient != 'v' and orient != 'h':  # check if v or h passed
                return False  # unexpected value!

        return True

    def __change_turn(self):
        """Takes no parameters. Changes the turn to the next player. Returns nothing."""
        # change to second player's turn if currently player one's turn
        if self._player_turn == 1:
            self._player_turn = 2

        # change to first player's turn if currently player two's turn
        else:
            self._player_turn = 1

    def print_board(self):
        """Prints the current state of the Quoridor game board. Used for testing purposes only."""
        # iterate through cols
        for row in range(9):
            for col in range(9):  # iterate through rows
                print(str(col) + str(row), end='')  # print cell coords in line

                # print fences, if any
                if self._board.get_cell((col, row)).get_fence("left"):
                    print("l", end='')  # print left fence in line
                if self._board.get_cell((col, row)).get_fence("right"):
                    print("r", end='')  # print right fence in line
                if self._board.get_cell((col, row)).get_fence("top"):
                    print("t", end='')  # print top fence in line
                if self._board.get_cell((col, row)).get_fence("bot"):
                    print("b", end='')  # print bottom fence in line
                # print pawn, if any
                if self._board.get_cell((col, row)).get_pawn():
                    print("P", end='')  # print pawn in line

                print(" ", end='')  # space after cell/fences/pawn
            print("\n")  # new line after each row

    def change_pawn_loc(self, p1, p2):
        """Given two tuples, one for player 1 and one for player 2, changes the player's pawn locations to the new
        tuple coordinates, respectively. Returns a string. Used for testing purposes only."""
        # remove pawns from board
        self._board.get_cell(self._players[1].get_pawn_loc()).set_pawn(False)
        self._board.get_cell(self._players[2].get_pawn_loc()).set_pawn(False)

        # change pawn location for each player
        self._players[1].set_pawn_loc(p1)
        self._players[2].set_pawn_loc(p2)

        # replace pawns on board
        self._board.get_cell(p1).set_pawn(True)
        self._board.get_cell(p2).set_pawn(True)

        return "Cheater."


# define main function
def main():
    """Play the Quoridor game here."""
    pass


# run main function if run as script
if __name__ == '__main__':
    main()
