#!/usr/bin/python3

from collections import namedtuple

# TODO: move this somewhere else
# TODO: autodetect this

# Do we want to use unicode icons?
USE_UNICODE = True

class _Symbols():
    """Conveniance class for using getattr()."""
    def __init__(self):
        if USE_UNICODE:
            self.ZERO    = "□"
            self.ONE     = "①"
            self.TWO     = "②"
            self.THREE   = "③"
            self.FOUR    = "④"
            self.FIVE    = "⑤"
            self.SIX     = "⑥"
            self.SEVEN   = "⑦"
            self.EIGHT   = "⑧"
            
            self.FLAG    = "🚩"
            self.MINE    = "💣"
            self.UNKNOWN = "�"
        else:
            self.ZERO    = "0"
            self.ONE     = "1"
            self.TWO     = "2"
            self.THREE   = "3"
            self.FOUR    = "4"
            self.FIVE    = "5"
            self.SIX     = "6"
            self.SEVEN   = "7"
            self.EIGHT   = "8"

            self.FLAG    = "F"
            self.MINE    = "*"
            self.UNKNOWN = "?"

class Cell():
    """A representation of a cell in a game of minesweeper."""

    @staticmethod
    def num2eng(num):
        """Return an English string representation of num.
        Args:
            num: number to translate, 0 <= num <= 8
            
        Raises:
            IndexError: if num is out of bounds"""
        if num > 8 or num < 0:
            raise IndexError
        else:
            return {
                    0: "zero",
                    1: "one",
                    2: "two",
                    3: "three",
                    4: "four",
                    5: "five",
                    6: "six",
                    7: "seven",
                    8: "eight"
                   }[num]

    #@classmethod
    #def __new__(cls):
        #"""Wrapper around collections.namedtuple."""
        #self = super(Cell, cls).__new__(cls, "Cell", "row", "column")
        #return self

    def __init__(self):
        #FIXME
        """TBD"""
        self.adjacent_mines = 0
        self.flagged = False
        self.has_mine = False
        self.revealed = False

    def __str__(self):

        if self.flagged:
            return FLAG
        if self.has_mine:
            return MINE
        if not self.revealed:
            return UNKNOWN
        else:
            # disgusting
            return getattr(_Symbols(), self.num2eng(self.adjacent_mines).upper())

    def __repr__(self):

        if self.revealed:
            return str(self.adjacent_mines)
        else:
            return ""

    def status(self):
        """Alias to self.__str__()."""
        return self.__str___()
