#!/usr/bin/python3

from code import interact
from random import randrange

#from minesweeper import *
import minesweeper as ms

c = ms.Cell()
c.revealed = True
c.adjacent_mines = randrange(9)

interact(local=locals())
