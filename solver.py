"""A solver for Minesweeper."""

from collections import defaultdict, deque


class Solver():
    """A solver for an instance of minesweeper.Minesweeper."""

    def __init__(self, game):
        """Creates a new instance of a minesweeper solver.

        Args:
            game: an instance of minesweeper.Minesweeper
        """

        self.game = game
        self.rows = game.rows
        self.columns = game.columns
        self.mines = game.mines

        self.revealed = 0
        self.update_queue = deque()
        self.reveal_queue = deque()
        # self.probability = \
        #    defaultdict(lambda: game.mines / (game.rows * game.colums))
        self.probability = \
            [[game.mines / (game.rows * game.columns)
              for _ in range(game.rows)]
             for _ in range(game.columns)]

    def guess(self):
        """Reveals the cell with the lowest probability of being a mine."""

        def min(L):
            # TODO: make this more efficient
            minval = float("Inf")
            for i in range(len(L)):
                for j in range(len(L[i])):
                    if L[i][j] < minval:
                        minval = L[i][j]
                        coords = (i, j)
            return coords

        self.reveal_queue.appendleft(min(self.probability))

    def neighborhood(self, r, c):
        """Return a list of tuples adjacent to (r, c).

        Args:
            r: row of cell
            c: column of cell

        Returns:
            A list of tuples
        """

        return [(x, y)
                for x in {r - 1 if r > 0 else r, r,
                          r + 1 if r < self.rows - 1 else r}
                for y in {c - 1 if c > 0 else c, c,
                          c + 1 if c < self.columns - 1 else c}
                if (x, y) != (r, c)]

    def update(self, r, c):
        """Update the cell at (r, c), taking action as necesary.

        Args:
            r: row of cell to update
            c: column of cell to update
        """

        N = self.neighborhood(r, c)
        F = [C for C in N if self.game[C].flagged]
        U = [C for C in N if not self.game[C].revealed]

        undetected = set(N) - set(F)
        if len(undetected) == 0:
            self.reveal_queue.extendleft(U)
        elif len(undetected) == len(U):
            for C in U:
                self.game.flag(*C)
            self.update_queue.extendleftset((set(N) - set(F)) - set(U))
        else:
            for x, y in N:
                self.probability[x][y] = len(undetected) / len(U)

    def reveal(self, r, c):
        """Reveal the cell at (r, c), taking action as necesary.

        Args:
            r: row of cell to reveal
            c: column of cell to reveal
        """

        self.game.reveal(r, c)
        for D in self.neighborhood(r, c):
            #if self.game[D].revealed:
            self.update_queue.appendleft(D)

    def solve(self):
        """Attempt to solve the game."""

        steps = 0
        while not self.game.game_over():
            steps += 1
            if self.reveal_queue:
                print("rqueue")
                self.reveal(*self.reveal_queue.pop())
            elif self.update_queue:
                print("uqueue")
                self.update(*self.update_queue.pop())
            else:
                print("guessing")
                self.guess()
            print(steps)

        print("Terminated after {} steps.".format(steps))
        if self.game.result:
            print("Victory!")
        else:
            print("Solving failed.")
        print(self.game)
