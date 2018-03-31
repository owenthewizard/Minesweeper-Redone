"""A game of minesweeper."""

from enum import Enum
from random import randrange
from re import compile as regex_compile

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
        ZERO = "□"
        ONE = "①"
        TWO = "②"
        THREE = "③"
        FOUR = "④"
        FIVE = "⑤"
        SIX = "⑥"
        SEVEN = "⑦"
        EIGHT = "⑧"

        FLAG = "🚩"
        MINE = "💣"
        UNKNOWN = "�"
    else:
        ZERO = "0"
        ONE = "1"
        TWO = "2"
        THREE = "3"
        FOUR = "4"
        FIVE = "5"
        SIX = "6"
        SEVEN = "7"
        EIGHT = "8"

        FLAG = "F"
        MINE = "*"
        UNKNOWN = "?"


class Cell():
    """A representation of a cell in a game of minesweeper."""

    def __init__(self):
        """Create a new Cell."""

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

    def __repr__(self):
        if self.flagged:
            return "flagged"
        if not self.revealed:
            return "unknown"
        if self.has_mine:
            return "mine"

        return self.adjacent_mines


class Minesweeper():
    """An instance of the game."""

    def _test_bounds(self, r, c):
        """Check that (r, c) is within the board.

        Args:
            r: row of cell to test
            c: column of cell to test

        Raises:
            IndexError if (r, c) is not within the board
        """

        if (r < 0 or r >= self.rows) or (c < 0 or c >= self.columns):
            raise IndexError

    def _test_bounds_nonfatal(self, r, c):
        """Check that (r, c) is within the board.

        Args:
            r: row of cell to test
            c: column of cell to test

        Returns:
            True if cell is within the board
            False if cell is not within the board
        """

        return (r >= 0 and r < self.rows) and (c >= 0 and c < self.columns)

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
        self.generated = False
        self.board = [[Cell() for _ in range(rows)] for _ in range(columns)]
        self.flags_placed = 0
        self.mines_flagged = 0
        self.result = None

        if mines is not None:
            self.mines = mines
        else:
            self.mines = (rows * columns) // 3

    def __getitem__(self, coordinates):
        """Get the cell at coordinates.

        Args:
            coordinates: a tuple of the row and column to retrieve

        Returns:
            An instance of Cell()
        """

        r, c = coordinates
        self._test_bounds(r, c)
        return self.board[r][c]

    def flag(self, r, c):
        """Flag (r, c) as a mine.

        Args:
            r: row of cell to flag
            c: column of cell to flag
        """

        self._test_bounds(r, c)
        self[r, c].flagged = True
        self.flags_placed += 1
        if self[r, c].has_mine:
            self.mines_flagged += 1

        if self.flags_placed == self.mines \
                and self.mines_flagged == self.mines:
            self.result = True

    def unflag(self, r, c):
        """Remove a flag from (r, c).

        Args:
            r: row of cell to unflag
            c: column of cell to unflag
        """

        self._test_bounds(r, c)
        self[r, c].flagged = False
        self.flags_placed -= 1
        if not self[r, c].has_mine:
            self.mines_flagged -= 1

    def _count_adjacent_mines(self, r, c):
        """Count mined cells adjacent to (r, c).

        Args:
            r: row of cell
            c: column of cell
        """

        found_mines = 0
        for C in self._adjacents(r, c):
            if self[C].has_mine:
                found_mines += 1
        return found_mines

    def _adjacents(self, r, c):
        """Return a list of tuples adjacent to (r, c)

        Args:
            r: row of cell
            c: column of cell

        Returns:
            A list of tuples adjacent to (r, c)
        """

        # gross!
        return [(x, y)
                for x in {r - 1 if r > 0 else r, r,
                          r + 1 if r < self.rows - 1 else r}
                for y in {c - 1 if c > 0 else c, c,
                          c + 1 if c < self.columns - 1 else c}
                if (x, y) != (r, c)]

    def game_over(self) -> bool:
        """Is the game over?

        Returns:
            True if the game is over
            False otherwise
        """
        return self.result is not None

    def _place_mines(self, protected):
        """Place mines pseudo-randomly around the board, except for protected.

        Args:
            protected: a tuple of a row and column that will never receive a
                       mine
        """
        placed = 0
        while placed < self.mines:
            C = (randrange(self.rows), randrange(self.columns))
            if not self[C].has_mine and C != protected:
                self[C].has_mine = True
                placed += 1
                for D in self._adjacents(*C):
                    self[D].adjacent_mines += 1

    def reveal(self, r, c):
        """Reveal the cell at (r, c).

        Args:
            r: row of cell to reveal
            c: column of cell to reveal
        """

        self._test_bounds(r, c)

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
            return

        if self[(r, c)].adjacent_mines == 0:
            for C in self._adjacents(r, c):
                self.reveal(*C)

        if self.flags_placed == self.mines \
                and self.mines_flagged == self.mines:
            self.result = True

    def __str__(self):
        board = str()

        for R in self.board:
            for C in R:
                board += "{} ".format(C)
            board += "\n"

        # TODO: generate cheeky messages
        if self.game_over():
            board += "Nice job, you won!" \
                if self.result else "Sorry, you lost!"
        return board

    def play(self):
        """Start an interactive game."""

        def _get_sanitized_tup():
            """Internal use, get a sanitized tuple-ish."""

            S = "\0"
            # FIXME this doesn't work
            # compile(r"[0-{}],( ?)*[0-{}]".format(
            #    self.rows, self.columns))
            while not regex_compile(r"[0-9]*,( ?)*[0-9]").match(S):
                S = input("Enter the cell you want to operate on as a tuple, "
                          "without parentheses. For example `2, 3` or `2,3`: ")
            return map(int, S.split(","))

        while not self.game_over():
            print(self)
            cmd = str()
            while cmd not in {"f", "h", "r", "u"}:
                cmd = input("Enter a command, or h for help: ")

            if cmd == "r":
                self.reveal(*_get_sanitized_tup())
            elif cmd == "f":
                self.flag(*_get_sanitized_tup())
            elif cmd == "u":
                self.unflag(*_get_sanitized_tup())
            else:
                print("f: flag a cell\nh: show this help\nr: reveal a cell\n"
                      "u: unflag a cell.")
        else:
            print(self)

    def restart(self, rows=None, cols=None, mines=None):
        """Restart the game.

        Args:
            rows: number of rows for new game, none for no change
            cols: number of columns for new game, none for no change
            mines: number of mines for new game, none for no change
        """

        self.__init__(rows if rows is not None else self.rows,
                      cols if cols is not None else self.columns,
                      mines if mines is not None else self.mines)
