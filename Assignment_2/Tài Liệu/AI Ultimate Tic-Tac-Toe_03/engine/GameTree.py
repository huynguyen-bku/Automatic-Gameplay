"""
Game Tree
"""

import numbers

class GameTree:
    """
    The 2-player game tree via a depth limited heuristic based MinMax.
    """
    def __init__(self, initial_state, opponent_first=False, depth_limit=1):
        """
        Args:
            initial_state: State.
            opponent_first: Boolean, indicates if the opponent makes the
                            first move.
        """

        self.TRACE = False
        self.DICTATE = True

        self.current = initial_state
        self.custom_heuristic = None
        self.turn_handler = None
        self.tester_handler = None

        self.turn_id = initial_state.turn
        if opponent_first:
            self.turn_id = 1 - initial_state.turn

        self.alpha = float("-inf")
        self.beta = float("inf")
        self.depth_limit = depth_limit


    def trace(self, *text):
        """
        Invokes print if trace is enabled.
        """

        if self.TRACE:
            print(*text)

    def dictate(self, *text):
        """
        Invokes print if trace is enabled.
        """

        if self.DICTATE:
            print(*text)

    def attach_turn_handler(self, handler):
        """
        Attaches a turn handler which is invoked when it is the
        opponents turn. The handler should return the value of
        the next state, or optionally an integer representing
        the index into the current node's successor's list.

        Args:
            handler: A function invoked when it is the opponents turn.
        """
        self.turn_handler = handler

    def attach_tester_handler(self, handler):
        """
        Attaches a turn handler which is invoked when it is the "AIs"
        turn. The handler should return the value of
        the next state, or optionally an integer representing
        the index into the current node's successor's list.

        Args:
            handler: A function invoked when it is the "AIs" turn.
        """
        self.tester_handler = handler

    def prompt_opponent(self, node):
        """
        Prompts the opponent for their next move and returns that move.
        The move is "validated". If an invalid move is supplied, the opponent
        is prompted again.

        Args:
            node: The current State.

        Returns: a State instance.
        """

        if not self.turn_handler:
            raise "No turn handler defined."

        # Keep asking for their move until a valid move is made.
        valid_moves = node.successors()

        opponents_move = None
        while opponents_move not in valid_moves:
            try:
                opponents_move = self.turn_handler(node)
                if isinstance(opponents_move, numbers.Number):
                    # Allow the handler to return an index into the successors list.
                    opponents_move = valid_moves[opponents_move]
            except:
                continue

        return opponents_move

    def prompt_tester(self, node):
        """
        Prompts a tester for their next move and returns that move.
        The move is "validated". If an invalid move is supplied, the tester
        is prompted again.

        Args:
            node: The current State.

        Returns: a State instance.
        """

        if not self.tester_handler:
            raise "No turn handler defined."

        # Keep asking for their move until a valid move is made.
        valid_moves = node.successors()

        our_move = None
        while our_move not in valid_moves:
            try:
                our_move = self.tester_handler(node)
                if isinstance(our_move, numbers.Number):
                    # Allow the handler to return an index into the successors list.
                    our_move = valid_moves[our_move]
            except:
                continue

        return our_move

    def dictate_move(self, state):
        """
        Prints information about the current state.

        Args:
            state: The state to dictate.
        """

        self.dictate(str(state))

    def play(self, custom_heuristic=None):
        """
        Plays the game.

        Args:
            custom_heuristic: Function, an optional custom heuristic to
                              be applied for the depth limited MinMax.

        Returns: True if the opponent loses.
        """

        self.custom_heuristic = custom_heuristic

        while True:
            children = self.current.successors()
            if not children:
                # If we reach a terminal node, then game is over.
                # Return True if we win.
                return self.current.is_winner(self.turn_id)

            # Opponents turn.
            if self.current.turn != self.turn_id:
                opponents_move = self.prompt_opponent(self.current)

                # Print out the final choice of the opponent
                self.dictate_move(opponents_move)

                self.current = opponents_move
                continue

            # Our turn.
            our_move = None
            if self.tester_handler:
                # Allows for a "tester" to mock the move computation.
                our_move = self.prompt_tester(self.current)
            else:
                our_move = self.compute_best_move(self.current)

            # Tell opponent what we are doing.
            self.dictate_move(our_move)

            self.current = our_move


    def eval_heuristic(self, node):
        """
        Computes and returns the heuristic function applied to the node.

        Args:
            node: The node (State) to evaluate.

        Returns: h(node)
        """

        if self.custom_heuristic:
            return self.custom_heuristic(self.turn_id, node)

        # Otherwise use some default heuristic.
        self.trace("No heuristic configured.")
        return 0

    def utility(self, node):
        """
        Computes the utility value of the game tree node (State),
        by invoking the heuristic evaluation function.

        Args:
            node: The node to apply the utility function to.

        Returns the utility value of the node.
        """

        # Apply heuristic.
        return self.eval_heuristic(node)


    def compute_best_move(self, node):
        """
        Returns the best next move (in the form of a state) for
        the player whose turn it is (as defined by node.turn).

        Args:
            node: The node on which to branch, i.e. usually the current State.

        Returns: The best successor node for the player whose turn it is.
        """

        best_node = None
        best_gamma = None

        for c in node.successors():
            gamma = self.df_alpha_beta(c, float('-inf'), float('inf'))

            if node.turn == self.turn_id:
                # gamma == alpha; maximize alpha
                if best_node is None or best_gamma < gamma:
                    best_node = c
                    best_gamma = gamma
            else:
                # gamma == beta; minimize beta
                if best_node is None or best_gamma > gamma:
                    best_node = c
                    best_gamma = gamma

        return best_node

    def df_alpha_beta(self, node, alpha, beta, depth=None):
        """
        Applies alpha beta pruning in a depth limited fashion to the
        game tree.

        Args:
            node: The current node to explore.
            alpha: From the alpha-beta algorithm.
            beta: From the alpha-beta algorithm.

        Returns: The utility value (possibly approximated via an heuristic)
                 of the terminal node of the DFS.
        """

        if depth is None:
            depth = self.depth_limit

        children = node.successors()

        if not children or depth == 0:
            # Terminal
            return self.utility(node)

        if node.turn == self.turn_id:
            # Maximize self.
            for c in children:
                alpha = max(alpha, self.df_alpha_beta(c, alpha, beta, depth - 1))
                if beta <= alpha:
                    break
            return alpha
        else:
            # Minimize opponent.
            for c in children:
                beta = min(beta, self.df_alpha_beta(c, alpha, beta, depth - 1))
                if beta <= alpha:
                    break
            return beta
