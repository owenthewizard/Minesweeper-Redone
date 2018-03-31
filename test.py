#!/usr/bin/env python3

from minesweeper import Minesweeper
from solver import Solver
from code import interact

game = Minesweeper(10, 10)
solver = Solver(game)
interact(local=locals())
