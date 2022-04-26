"""
Ultimate Tic Tac Toe implementation of the space.
"""

class UTTTSpace():
    """
    Represents the NxN grid composing the game board.
    Each NxN grid is divided into nxn subboards.
    """

    def __init__(self, parent=None, N=3, n=3):
        self.cells = None
        self.N = N # dim of main board
        self.n = n # dim of subboard

        self.winner = None
        self.subgames = {}

        if parent is None:
            # Board is root node. Creating empty board.
            # Keeping the cells in a single dimensional list allows for
            # valid "shallow" copying.
            self.cells = [None for c in range((n*N) ** 2)]
        else:
            # We inherit N and n from the parent if defined.
            self.N = parent.N
            self.n = parent.n
            self.cells = list(parent.cells)
            self.winner = parent.winner
            self.subgames = dict(parent.subgames)

    def __str__(self):
        s = ""
        for y in range(self.N * self.n):
            for x in range(self.N * self.n):
                cell = self.cells[(self.N * self.n * y) + x]
                s += ('{0: <4}'.format('[ ]' if cell is None else '['+str(cell)+']'))
            s += '\n'
        return s

    def get(self, coord):
        """
        Gets the value at (iX, iY) in subboard (sX, sY).
        """

        (sX, sY, iX, iY) = coord

        x = (sX * self.N) + iX
        y = (sY * self.N) + iY
        return self.cells[(self.N * self.n * y) + x]

    def set(self, coord, val):
        """
        Sets the value at (iX, iY) in subboard (sX, sY) to val.
        """

        (sX, sY, iX, iY) = coord

        x = (sX * self.N) + iX
        y = (sY * self.N) + iY
        self.cells[(self.N * self.n * y) + x] = val

        self.update_win(coord, val)

    def update_win(self, coord, val):
        """
        Updates win stats.

        Note: This may be computationally expensive even though it's O(N + n).
        """
        (sX, sY, iX, iY) = coord

        # maintain self.subgames, indicating subgame wins.
        # check if subgame is won by the latest move
        cond_row = all(self.get((sX, sY, cx, iY)) == val for cx in range(self.n))
        cond_col = all(self.get((sX, sY, iX, cy)) == val for cy in range(self.n))
        if cond_row or cond_col:
            self.subgames[(sX, sY)] = val
        elif iX == iY or iX == self.n - iY - 1:
            # Check diagonals
            diag_left = all(self.get((sX, sY, c, c)) == val for c in range(self.n))
            diag_right = all(self.get((sX, sY, c, self.n - c - 1)) == val for c in range(self.n))
            if diag_left or diag_right:
                self.subgames[(sX, sY)] = val

        # check if outer game is won by the latest move
        if self.subgames.get((sX, sY), None) is not None:
            subwinner = self.subgames[(sX, sY)]
            cond_row = all(self.subgames.get((cx, sY), None) == subwinner for cx in range(self.N))
            cond_col = all(self.subgames.get((sX, cy), None) == subwinner for cy in range(self.N))
            if cond_row or cond_col:
                self.winner = subwinner
            elif sX == sY or sX == self.N - sY - 1:
                # Check diagonals
                diag_left = all(self.subgames.get((c, c), None) == subwinner for c in range(self.N))
                diag_right = all(self.subgames.get((c, self.N - c - 1), None) == subwinner for c in range(self.N))
                if diag_left or diag_right:
                    self.winner = subwinner

    def is_winner(self, player_id):
        """
        Given a player_id, determines if this state
        is a terminal state in which that player wins.

        Args:
            player_id: 0 or 1

        Returns: boolean
        """

        return self.winner == player_id



