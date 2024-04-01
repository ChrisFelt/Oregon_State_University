# Author: Christopher Felt
# Date: 5/31/2021
#
# Description: Program that contains a class for defining an OrthokonBoard object, which contains the current state
# and a list of lists representing a 4 x 4 space board.
#
# The class contains the following methods that handle rules concerning the game board:
#
# 1) A get method that returns the game state, "UNFINISHED", "RED_WON", or "YELLOW_WON".
#
# 2) Eight methods for movement either orthogonally or diagonally; one each for up, down, left, right, up and right,
# up and left, down and right, and down and left. The methods first check if the move is legal, i.e. the piece was
# moved as far as it could be until it touched another piece, and was not moved off the board or into a non-empty space.
#
# 3) A method for flipping orthogonally adjacent pieces of the opposing color.
#
# 4) A method for checking if the victory condition has been met by either the red or yellow player. This method checks
# if all pieces on the board belong to a single player, and changes the game state accordingly.
#
# 5) Finally, a method for making moves that determines which method for movement will be used, and ensures that pieces
# are flipped and the game state is updated after each move. Also determines the generic legality of the move, such as
# whether the space selected is empty, the destination is the same as the origin, the destination is on the board, and
# the move is either orthogonal or diagonal. This move takes 4 non-negative integers as arguments in the following
# order: from row, from column, to row, to column.

# define OrthokonBoard class
class OrthokonBoard:

    # Docstring description
    """Represents a game board for two players, red and yellow, to move game pieces orthogonally or diagonally, with
    methods for controlling movement, flipping opposing orthogonally adjacent pieces after each move, and updating the
    game state if a move resulted in one player controlling all pieces on the board. Movement is controlled by the
    make_move method, which takes four non-negative integers as arguments: the from row, from column, to row, and to
    column, in that order."""

    # ===========================================================================================================
    # initialize data members
    def __init__(self):

        # define initial board
        # list of rows in each column, column/row number corresponds to list number
        # R = red, E = empty, Y = yellow
        self._board = [["R", "E", "E", "Y"],  # column 0
                       ["R", "E", "E", "Y"],  # column 1
                       ["R", "E", "E", "Y"],  # column 2
                       ["R", "E", "E", "Y"]]  # column 3

        self._current_state = "UNFINISHED"  # initialize game state

    # ===========================================================================================================
    # get method returning current game state
    def get_current_state(self):

        return self._current_state

    # ===========================================================================================================
    # method that moves a piece orthogonally upwards
    def __move_up(self, from_col, from_row, to_row):

        # first check if any pieces are in the way
        for i in range(abs(from_row - to_row)):  # loop number of spaces moved

            if self._board[from_col][from_row - (i + 1)] != "E":

                return False

        # check the next space up after moving to make sure it isn't empty
        # check if the next space up is inside the board
        if to_row - 1 in range(4):

            # next space up after moving
            if self._board[from_col][to_row - 1] == "E":

                return False  # didn't move far enough

        # loop for number of spaces moved
        for i in range(abs(from_row - to_row)):

            # check if new space is empty
            if self._board[from_col][from_row - (i + 1)] == "E":

                # replace new space with piece from last space
                self._board[from_col][from_row - (i + 1)] = self._board[from_col][from_row - i]

                # mark last space as empty
                self._board[from_col][from_row - i] = "E"

        return True

    # ===========================================================================================================
    # method that moves a piece orthogonally downwards
    def __move_down(self, from_col, from_row, to_row):

        # first check if any pieces are in the way
        for i in range(abs(from_row - to_row)):  # loop number of spaces moved

            if self._board[from_col][from_row + (i + 1)] != "E":

                return False

        # check the next space down after moving to make sure it isn't empty
        # check if the next space down is inside the board
        if to_row + 1 in range(4):

            # next space down after moving
            if self._board[from_col][to_row + 1] == "E":

                return False  # didn't move far enough

        # loop for number of spaces moved
        for i in range(abs(from_row - to_row)):

            # check if new space is empty
            if self._board[from_col][from_row + (i + 1)] == "E":

                # replace new space with piece from last space
                self._board[from_col][from_row + (i + 1)] = self._board[from_col][from_row + i]

                # mark last space as empty
                self._board[from_col][from_row + i] = "E"

        return True

    # ===========================================================================================================
    # method that moves a piece orthogonally rightwards
    def __move_right(self, from_col, from_row, to_col):

        # first check if any pieces are in the way
        for i in range(abs(from_col - to_col)):  # loop number of spaces moved

            if self._board[from_col + (i + 1)][from_row] != "E":

                return False

        # check the next space right after moving to make sure it isn't empty
        # check if the next space right is inside the board
        if to_col + 1 in range(4):

            # next space right after moving
            if self._board[to_col + 1][from_row] == "E":

                return False  # didn't move far enough

        # loop for number of spaces moved
        for i in range(abs(from_col - to_col)):

            # check if new space is empty
            if self._board[from_col + (i + 1)][from_row] == "E":

                # replace new space with piece from last space
                self._board[from_col + (i + 1)][from_row] = self._board[from_col + i][from_row]

                # mark last space as empty
                self._board[from_col + i][from_row] = "E"

        return True

    # ===========================================================================================================
    # method that moves a piece orthogonally leftwards
    def __move_left(self, from_col, from_row, to_col):

        # first check if any pieces are in the way
        for i in range(abs(from_col - to_col)):  # loop number of spaces moved

            if self._board[from_col - (i + 1)][from_row] != "E":

                return False

        # check the space left after moving to make sure it isn't empty
        # check if the next space left is inside the board
        if to_col - 1 in range(4):

            # next space left after moving
            if self._board[to_col - 1][from_row] == "E":

                return False  # didn't move far enough

        # loop for number of spaces moved
        for i in range(abs(from_col - to_col)):

            # check if new space is empty
            if self._board[from_col - (i + 1)][from_row] == "E":
                # replace new space with piece from last space
                self._board[from_col - (i + 1)][from_row] = self._board[from_col - i][from_row]

                # mark last space as empty
                self._board[from_col - i][from_row] = "E"

        return True

    # ===========================================================================================================
    # method for moving diagonally up and rightwards
    def __move_up_and_right(self, from_col, from_row, to_col, to_row):

        # first check if any pieces are in the way
        # assumes destination is exactly 45 degrees from origin
        for i in range(abs(from_row - to_row)):  # loop number of spaces moved

            if self._board[from_col + (i + 1)][from_row - (i + 1)] != "E":

                return False

        # check the space up and right after moving to make sure it isn't empty
        # check if the next space up and right is inside the board
        if to_col + 1 in range(4) and to_row - 1 in range(4):

            # next space up and right after moving
            if self._board[to_col + 1][to_row - 1] == "E":

                return False  # didn't move far enough

        # loop for number of spaces moved
        for i in range(abs(from_row - to_row)):

            # check if new space is empty
            if self._board[from_col + (i + 1)][from_row - (i + 1)] == "E":

                # replace new space with piece from last space
                self._board[from_col + (i + 1)][from_row - (i + 1)] = self._board[from_col + i][from_row - i]

                # mark last space as empty
                self._board[from_col + i][from_row - i] = "E"

        return True

    # ===========================================================================================================
    # method for moving diagonally up and leftwards
    def __move_up_and_left(self, from_col, from_row, to_col, to_row):

        # first check if any pieces are in the way
        # assumes destination is exactly 45 degrees from origin
        for i in range(abs(from_row - to_row)):  # loop number of spaces moved

            if self._board[from_col - (i + 1)][from_row - (i + 1)] != "E":

                return False

        # check the space up and left after moving to make sure it isn't empty
        # check if the next space up and left is inside the board
        if to_col - 1 in range(4) and to_row - 1 in range(4):

            # next space up and left after moving
            if self._board[to_col - 1][to_row - 1] == "E":

                return False  # didn't move far enough

        # loop for number of spaces moved
        for i in range(abs(from_row - to_row)):

            # check if new space is empty
            if self._board[from_col - (i + 1)][from_row - (i + 1)] == "E":

                # replace new space with piece from last space
                self._board[from_col - (i + 1)][from_row - (i + 1)] = self._board[from_col - i][from_row - i]

                # mark last space as empty
                self._board[from_col - i][from_row - i] = "E"

        return True

    # ===========================================================================================================
    # method for moving diagonally down and rightwards
    def __move_down_and_right(self, from_col, from_row, to_col, to_row):

        # first check if any pieces are in the way
        # assumes destination is exactly 45 degrees from origin
        for i in range(abs(from_row - to_row)):  # loop number of spaces moved

            if self._board[from_col + (i + 1)][from_row + (i + 1)] != "E":

                return False

        # check the space down and right after moving to make sure it isn't empty
        # check if the next space down and right is inside the board
        if to_col + 1 in range(4) and to_row + 1 in range(4):

            # next space down and right after moving
            if self._board[to_col + 1][to_row + 1] == "E":

                return False  # didn't move far enough

        # loop for number of spaces moved
        for i in range(abs(from_row - to_row)):

            # check if new space is empty
            if self._board[from_col + (i + 1)][from_row + (i + 1)] == "E":

                # replace new space with piece from last space
                self._board[from_col + (i + 1)][from_row + (i + 1)] = self._board[from_col + i][from_row + i]

                # mark last space as empty
                self._board[from_col + i][from_row + i] = "E"

        return True

    # ===========================================================================================================
    # method for moving diagonally down and leftwards
    def __move_down_and_left(self, from_col, from_row, to_col, to_row):

        # first check if any pieces are in the way
        # assumes destination is exactly 45 degrees from origin
        for i in range(abs(from_row - to_row)):  # loop number of spaces moved

            if self._board[from_col - (i + 1)][from_row + (i + 1)] != "E":

                return False

        # check the space down and left after moving to make sure it isn't empty
        # check if the next space down and left is inside the board
        if to_col - 1 in range(4) and to_row + 1 in range(4):

            # next space down and left after moving
            if self._board[to_col - 1][to_row + 1] == "E":

                return False  # didn't move far enough

        # loop for number of spaces moved
        for i in range(abs(from_row - to_row)):

            # check if new space is empty
            if self._board[from_col - (i + 1)][from_row + (i + 1)] == "E":
                # replace new space with piece from last space
                self._board[from_col - (i + 1)][from_row + (i + 1)] = self._board[from_col - i][from_row + i]

                # mark last space as empty
                self._board[from_col - i][from_row + i] = "E"

        return True

    # ===========================================================================================================
    # method that flips pieces that are orthogonally adjacent after a move
    def __subvert_piece(self, col, row):

        # check spaces in adjacent rows
        for i in range(-1, 2):

            # exclude positions outside the board
            if row + i in range(4):

                # check if opposing piece present
                if self._board[col][row + i] != "E" and self._board[col][row + i] != self._board[col][row]:

                    # flip the piece!
                    self._board[col][row + i] = self._board[col][row]

        # check spaces in adjacent columns
        for i in range(-1, 2):

            # exclude positions outside the board
            if col + i in range(4):

                # check if opposing piece present
                if self._board[col + i][row] != "E" and self._board[col + i][row] != self._board[col][row]:

                    # flip the piece!
                    self._board[col + i][row] = self._board[col][row]

    # ===========================================================================================================
    # method for checking the state of the board and declaring a winner
    def __check_win(self):

        # check if no red pieces remain
        if "R" not in self._board[0] and "R" not in self._board[1] and \
                "R" not in self._board[2] and "R" not in self._board[3]:

            # yellow wins
            self._current_state = "YELLOW_WON"
            return True  # exit method

        # check if no yellow pieces remain
        elif "Y" not in self._board[0] and "Y" not in self._board[1] and \
                "Y" not in self._board[2] and "Y" not in self._board[3]:

            # red wins
            self._current_state = "RED_WON"
            return True  # exit method

        # -----------------------------------------------------------------------------------------
        # check if either player has no pieces that can be legally moved
        # set counters
        red_pieces = 0
        yellow_pieces = 0
        unmovable_red_pieces = 0
        unmovable_yellow_pieces = 0

        # loop through columns
        for i in range(4):

            for j in range(4):  # loop through rows

                if self._board[i][j] == "R":  # count current space if red

                    red_pieces += 1

                elif self._board[i][j] == "Y":  # count current space if yellow

                    yellow_pieces += 1

                # list for recording checks of adjacent spaces
                list_spaces_adjacent = ["X", "X", "X", "X"]  # refresh list before each check

                # check spaces on the edge of the board. this approach seems really clunky.
                # could collapse into loops similar to those in the if statements in __subvert_piece method, but loop
                # counters would be confusing
                if i + 1 not in range(4) or i - 1 not in range(4) or j + 1 not in range(4) or j - 1 not in range(4):

                    # check if column above not on board
                    if i + 1 not in range(4):

                        list_spaces_adjacent[0] = "O"  # record if true

                    # check if column above on board
                    if i + 1 in range(4):

                        # check if space is empty
                        if self._board[i + 1][j] != "E":

                            list_spaces_adjacent[0] = "O"  # record if true

                    # check if column below not on board
                    if i - 1 not in range(4):

                        list_spaces_adjacent[1] = "O"  # record if true

                    # check if column below on board
                    if i - 1 in range(4):

                        # check if space is empty
                        if self._board[i - 1][j] != "E":

                            list_spaces_adjacent[1] = "O"  # record if true

                    # check if row above not on board
                    if j + 1 not in range(4):

                        list_spaces_adjacent[2] = "O"  # record if true

                    # check if row above on board
                    if j + 1 in range(4):

                        # check if space is empty
                        if self._board[i][j + 1] != "E":

                            list_spaces_adjacent[2] = "O"  # record if true

                    # check if row below is not on board
                    if j - 1 not in range(4):

                        list_spaces_adjacent[3] = "O"  # record if true

                    # check if row below is on board
                    if j - 1 in range(4):

                        # check if space is empty
                        if self._board[i][j - 1] != "E":

                            list_spaces_adjacent[3] = "O"  # record if true

                    # check if all orthogonally adjacent spaces are either empty or off board
                    if "X" not in list_spaces_adjacent:

                        # if current space contains red piece, unmovable red counter goes up
                        if self._board[i][j] == "R":

                            unmovable_red_pieces += 1

                        # if current space contains yellow piece, unmovable yellow counter goes up
                        elif self._board[i][j] == "Y":

                            unmovable_yellow_pieces += 1

                # check spaces for which all adjacent spaces are within the board
                if i + 1 in range(4) and i - 1 in range(4) and j + 1 in range(4) and j - 1 in range(4):

                    # check all orthogonally adjacent spaces
                    if self._board[i + 1][j] != "E" and self._board[i - 1][j] != "E" and \
                            self._board[i][j + 1] != "E" and self._board[i][j - 1] != "E":

                        # if current space contains red piece, unmovable red counter goes up
                        if self._board[i][j] == "R":

                            unmovable_red_pieces += 1

                        # if current space contains yellow piece, unmovable yellow counter goes up
                        elif self._board[i][j] == "Y":

                            unmovable_yellow_pieces += 1

        # if no red pieces can move, yellow wins
        if unmovable_red_pieces / red_pieces == 1.0:

            # yellow wins
            self._current_state = "YELLOW_WON"
            return True  # exit method

        # if no yellow pieces can move, red wins
        elif unmovable_yellow_pieces / yellow_pieces == 1.0:

            # red wins
            self._current_state = "RED_WON"
            return True  # exit method

    # ===========================================================================================================
    # method for handling piece movement on the board
    def make_move(self, from_row, from_col, to_row, to_col):

        # -----------------------------------------------------------------------------------------
        # check if a player has won yet
        if self._current_state != "UNFINISHED":

            return False  # winner already decided

        # -----------------------------------------------------------------------------------------
        # check if piece was moved to same location as origin
        if from_col == to_col and from_row == to_row:

            return False  # can't move to origin from origin!

        # -----------------------------------------------------------------------------------------
        # check if destination is within the board
        elif from_col > 3 or from_row > 3 or to_col > 3 or to_row > 3:

            return False  # out of bounds!

        # -----------------------------------------------------------------------------------------
        # check if space is empty
        elif self._board[from_col][from_row] == "E":

            return False  # nothing to move!

        # -----------------------------------------------------------------------------------------
        # check if the move is orthogonal
        elif from_col == to_col or from_row == to_row:

            # check if move is vertical
            if from_col == to_col:

                # check if moving up
                if from_row > to_row:

                    # check if move is legal using __move_up method
                    # moves piece if True
                    if self.__move_up(from_col, from_row, to_row):

                        # flip opponent's adjacent pieces
                        self.__subvert_piece(to_col, to_row)

                        # check if this move resulted in a win condition
                        self.__check_win()
                        return True

                    else:

                        return False  # illegal move!

                # check if moving down
                if from_row < to_row:

                    # check if move is legal using __move_down method
                    # moves piece if True
                    if self.__move_down(from_col, from_row, to_row):

                        # flip opponent's adjacent pieces
                        self.__subvert_piece(to_col, to_row)

                        # check if this move resulted in a win condition
                        self.__check_win()
                        return True

                    else:

                        return False  # illegal move!

            # check if move is horizontal
            if from_row == to_row:

                # check if moving right
                if from_col < to_col:

                    # check if move is legal using __move_right method
                    # moves piece if True
                    if self.__move_right(from_col, from_row, to_col):

                        # flip opponent's adjacent pieces
                        self.__subvert_piece(to_col, to_row)

                        # check if this move resulted in a win condition
                        self.__check_win()
                        return True

                    else:

                        return False  # illegal move!

                # check if moving left
                if from_col > to_col:

                    # check if move is legal using __move_left method
                    # moves piece if True
                    if self.__move_left(from_col, from_row, to_col):

                        # flip opponent's adjacent pieces
                        self.__subvert_piece(to_col, to_row)

                        # check if this move resulted in a win condition
                        self.__check_win()
                        return True

                    else:

                        return False  # illegal move!

        # -----------------------------------------------------------------------------------------
        # check if move is diagonal
        elif abs(from_col - to_col) / abs(from_row - to_row) == 1.0:

            # check if moving rightwards
            if from_col < to_col:

                # check if moving up
                if from_row > to_row:

                    # check if move is legal using __move_up_and_right method
                    # moves piece if True
                    if self.__move_up_and_right(from_col, from_row, to_col, to_row):

                        # flip opponent's adjacent pieces
                        self.__subvert_piece(to_col, to_row)

                        # check if this move resulted in a win condition
                        self.__check_win()
                        return True

                    else:

                        return False  # illegal move!

                # check if moving down
                if from_row < to_row:

                    # check if move is legal using __move_up_and_right method
                    # moves piece if True
                    if self.__move_down_and_right(from_col, from_row, to_col, to_row):

                        # flip opponent's adjacent pieces
                        self.__subvert_piece(to_col, to_row)

                        # check if this move resulted in a win condition
                        self.__check_win()
                        return True

                    else:

                        return False  # illegal move!

            # check if moving leftwards
            if from_col > to_col:

                # check if moving up
                if from_row > to_row:

                    # check if move is legal using __move_up_and_left method
                    # moves piece if True
                    if self.__move_up_and_left(from_col, from_row, to_col, to_row):

                        # flip opponent's adjacent pieces
                        self.__subvert_piece(to_col, to_row)

                        # check if this move resulted in a win condition
                        self.__check_win()
                        return True

                    else:

                        return False  # illegal move!

                # check if moving down
                if from_row < to_row:

                    # check if move is legal using __move_down_and_left method
                    # moves piece if True
                    if self.__move_down_and_left(from_col, from_row, to_col, to_row):

                        # flip opponent's adjacent pieces
                        self.__subvert_piece(to_col, to_row)

                        # check if this move resulted in a win condition
                        self.__check_win()
                        return True

                    else:

                        return False  # illegal move!

        # -----------------------------------------------------------------------------------------
        # all other moves (i.e. not perfectly diagonal, etc.) are illegal
        else:

            return False
