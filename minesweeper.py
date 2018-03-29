from enum import Enum
from random import randrange

# TODO: move this somewhere else
# TODO: autodetect this

# Do we want to use unicode icons?
USE_UNICODE = False

_ENGLISH = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight"
}

class Symbols(Enum):
    """Symbols used to denote cells."""

    if USE_UNICODE:
        ZERO    = "□"
        ONE     = "①"
        TWO     = "②"
        THREE   = "③"
        FOUR    = "④"
        FIVE    = "⑤"
        SIX     = "⑥"
        SEVEN   = "⑦"
        EIGHT   = "⑧"
        
        FLAG    = "🚩"
        MINE    = "💣"
        UNKNOWN = "�"
    else:
        ZERO    = "0"
        ONE     = "1"
        TWO     = "2"
        THREE   = "3"
        FOUR    = "4"
        FIVE    = "5"
        SIX     = "6"
        SEVEN   = "7"
        EIGHT   = "8"

        FLAG    = "F"
        MINE    = "*"
        UNKNOWN = "?"

class Cell():
    """A representation of a cell in a game of minesweeper."""

    def __init__(self):
        #FIXME
        """TBD"""
        self.adjacent_mines = 0
        self.flagged = False
        self.has_mine = False
        self.revealed = False

    def __str__(self):

        if self.flagged:
            return Symbols.FLAG.value
        if not self.revealed:
            return Symbols.UNKNOWN.value
        if self.has_mine:
            return Symbols.MINE.value
        # disgusting
        return getattr(Symbols, _ENGLISH[self.adjacent_mines].upper()).value

#    def __repr__(self):
#
#        if self.revealed:
#            return str(self.adjacent_mines)
#        else:
#            return ""

    # Because assignments aren't allowed in lambdas
    def _mine(self):
        self.has_mine = True

    def status(self):
        """Alias to self.__str__()."""

        return self.__str__()

class Minesweeper():
    """An instance of the game."""

    def _test_bounds(self, r, c):
        """Check that (r, c) is within the board."""

        if r < 0 or r >= self.rows:
            raise IndexError
        if c < 0 or c >= self.columns:
            raise IndexError

    def _test_bounds_nonfatal(self, r, c):
        """Check that (r, c) is within the board."""

        if r < 0 or r >= self.rows:
            return False
        if c < 0 or r >= self.columns:
            return False
        return True
    
    def __init__(self, rows, columns, mines=None):
        """Creates a new instance of a Minesweeper game.
        
        Args:
            rows: the number of rows on the board
            columns: the number of columns on the board
            mines: the number of mines on the board
        """
        
        if rows <= 0:
            raise IndexError("Rows must be greater than zero")
        if columns <= 0:
            raise IndexError("Columns must be greater than zero")
        if mines is not None and mines >= rows * columns:
            raise IndexError("Mines must be less than rows * columns")
        
        self.rows = rows
        self.columns = columns
        if mines is not None:
            self.mines = mines
        else:
            self.mines = (rows * columns) // 3
        self.generated = False
        
        self.board = [[Cell() for _ in range(rows)] for _ in range(columns)]

        self.flags_placed = 0
        self.mines_flagged = 0
        self.result = None
        
    def __getitem__(self, coordinates):
        
        r, c = coordinates
        self._test_bounds(r, c)
        return self.board[r][c]

#    def __setitem__(self, coordinates, value):
#        
#        r, c = coordinates
#        self._test_bounds(r, c)
#        self.board[r][c] = value

    def flag(self, r, c):
        """Flag (r, c) as a mine."""

        self._test_bounds(r, c)
        self[r, c].flagged = True
        self.flags_placed += 1
        if self[r, c].has_mine:
            self.mines_flagged += 1

        if self.flags_placed == self.mines and self.mines_flagged == self.mines:
            self.result = True

    def unflag(self, r, c):
        """Remove a flag from (r, c)."""

        self._test_bounds(r, c)
        self[r, c].flagged = False
        self.flags_placed -= 1
        if not self[r, c].has_mine:
            self.mines_flagged -= 1
    
    def _count_adjacent_mines(self, r, c):
        """Count mined cells adjacent to (r, c)."""

        found_mines = 0
        # gross!
        for C in self._adjacents(r, c):
            if self[C].has_mine:
                found_mines += 1
        return found_mines

    def _adjacents(self, r, c):

        return set((x, y) for x in {r - 1 if r > 0 else r, r, r + 1 if r < self.rows - 1 else r} for y in {c - 1 if c > 0 else c, c, c + 1 if c < self.columns - 1 else c} if (x, y) != (r, c))

    
    def game_over(self) -> bool:
        """Is the game over?"""

        return self.result is not None

    def _place_mines(self, protected):

        placed = 0
        while placed < self.mines:
            C = (randrange(self.rows), randrange(self.columns))
            if not self[C].has_mine and C != protected:
                self[C].has_mine = True
                placed += 1
                for D in self._adjacents(*C):
                    self[D].adjacent_mines += 1

    def reveal(self, r, c):
        """Reveal the cell at (r, c)."""

        if not self.generated:
            self._place_mines((r, c))
            self.generated = True
            self.reveal(r, c)
            return

        if self[r, c].flagged or self[r, c].revealed:
            return

        self[(r, c)].revealed = True

        if self[(r, c)].has_mine:
            for i in range(self.rows):
                for j in range(self.columns):
                    if self[(i, j)].has_mine:
                        self[(i, j)].flagged = False
                        self.reveal(i, j)
            self.result = False

        if self[(r, c)].adjacent_mines == 0:
            for C in self._adjacents(r, c):
                    self.reveal(*C)

        if self.flags_placed == self.mines and self.mines_flagged == self.mines:
            self.result = True

    def __str__(self):

        board = str()

        for R in self.board:
            for C in R:
                board += "{} ".format(C)
            board += "\n"

        # TODO: generate cheeky messages
        if self.game_over():
            board += "Nice job, you won!" if self.result else "Sorry, you lost!"
        return board
