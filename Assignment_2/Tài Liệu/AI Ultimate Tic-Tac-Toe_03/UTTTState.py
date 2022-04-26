"""
Ultimate Tic Tac Toe State implementation.
"""

from engine import NonTerminalError
from UTTTSpace import UTTTSpace

class UTTTState():
    """
    A representation of game state.
    """
    def __init__(self, turn=0, parent=None, restriction=None, space=None):
        """
        Args:
            turn: 0 or 1, indicating which player decides the successor state.
            parent: Parent state.
            restriction: the coordinate of the subboard successors are derived from.
            space: a NxN grid with each cell holding a value of 0, 1, or None.
        """
        self.turn = turn
        self.parent = parent
        self.restriction = restriction
        self.cached_successors = None

        self.space = space
        if not self.space and self.parent:
            self.space = UTTTSpace(self.parent.space)


    def possible_moves(self, subboard=None):
        """
        Returns a list of all possible moves using the current space
        configuration in the form (sX, sY, iX, iY).
        """

        if self.space.winner is not None:
            # Game is over.
            return

        if not subboard:
            subboard = self.restriction
            if self.space.subgames.get(subboard, None) is not None:
                # Bad restriction. Open up to whole board.
                # This can happen if a subboard has already been won.
                subboard = None

        if not subboard:
            for sX in range(self.space.N):
                for sY in range(self.space.N):
                    yield from self.possible_moves((sX, sY))
        elif self.space.subgames.get(subboard, None) is None:
            (sX, sY) = subboard
            for iX in range(self.space.n):
                for iY in range(self.space.n):
                    coord = (sX, sY, iX, iY)
                    if self.space.get(coord) is None:
                        yield coord

    def successors(self):
        """
        Returns a list of successor states.
        """

        if self.cached_successors is None:
            children = []
            for move in self.possible_moves():
                (_, _, iX, iY) = move
                # Warning, a full copy of the space occurs here.
                child = UTTTState(1 - self.turn, self, (iX, iY))
                child.space.set(move, self.turn)

                if child:
                    children.append(child)

            self.cached_successors = children

        return self.cached_successors


    def is_winner(self, player_id):
        """
        Given a player_id, determines if this state
        is a terminal state in which that player wins.

        Args:
            player_id: 0 or 1

        Returns: boolean
        """

        return self.space.is_winner(player_id)

    def __str__(self):
        """
        Returns the string representation of this state.
        """

        return "Turn: {0}; Last move made by: {1}\n{2}".format(str(self.turn), str(1 - self.turn), str(self.space))
