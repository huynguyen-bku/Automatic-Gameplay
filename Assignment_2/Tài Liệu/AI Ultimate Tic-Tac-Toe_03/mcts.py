"""
MCTS player. Replaces the heuristic.
"""

import random
import time
import math

from engine.GameTree import GameTree

class Node:
    """
    Represents a node in the MCTS.
    """

    def __init__(self, state, parent=None):
        self.wins = 0 # number of wins
        self.losses = 0 # number of losses
        self.state = state # encapsulates the move to make
        self.parent = parent # parent node
        self.children = []

    def total_runs(self):
        return self.wins + self.losses

    def value(self):
        if self.total_runs() > 0:
            return self.wins / self.total_runs()
        else:
            return None

    def add(self, child):
        if child not in self.children:
            self.children.append(child)


def always_choose_random_state(node):
    """
    Makes a random move.
    """
    return random.randint(0, len(node.successors()) - 1)

# Root
root = None
max_duration = 3

def mcts_reset(mcts_time=3):
    global root
    global max_duration

    root = None
    max_duration = mcts_time

def mcts_player(last_state):
    """
    Given the last state, we have to pick the best successor.
    """
    global root
    global max_duration

    MCTS_TUNABLE = 0.3

    # Set initial root.
    if root is None:
        # Set last_state as root.
        root = Node(last_state, None)
    else:
        # Assign root of tree to the last move, so we can examine the children.
        # This logic means that mcts_player must ALWAYS be called (cannot be mixed with a
        # heuristic function for the same game).
        root = next(n for n in root.children if n.state == last_state)
        root.parent = None # for garbage collection

    for successor in root.state.successors():
        root.add(Node(successor, root))

    # Play each child up to duration_per_move.
    duration_per_move = max_duration / len(root.children)
    for move_node in root.children:
        start = time.time()
        runs = 0
        while runs == 0 or time.time() - start < duration_per_move:
            runs += 1
            if play_move(move_node, last_state.turn):
                move_node.wins += 1
                root.wins += 1
            else:
                move_node.losses += 1
                root.losses += 1

    # Pick child of root with the highest UCB
    best_move = None
    best_ucb = 0
    for move_node in root.children:
        if move_node.value() is None:
            raise "Move has no trials run."

        ucb = (move_node.value()) + (MCTS_TUNABLE * math.sqrt(math.log(root.total_runs())/move_node.total_runs()))
        if best_move is None or ucb > best_ucb:
            best_move = move_node
            best_ucb = ucb

    # Update root.
    root = best_move

    for successor in root.state.successors():
        root.add(Node(successor, root))

    root.parent = None # for garbage collection

    return root.state

def play_move(node, turn_id):
    """
    Play random moves until end game, updating nodes along the way.
    """

    # If terminal and if we won.
    if not node.state.successors():
        if node.state.is_winner(turn_id):
            node.wins += 1
            return True
        else:
            node.losses += 1
            return False

    # Non-terminal. Play randomly.
    # Obviously we can make this smarter by making smarter choices, such as
    # making a winning move if immediately possible. Since MCTS was an afterthought
    # to our project, we did not focus on it.
    move = Node(random.choice(node.state.successors()), node)
    node.add(move)
    if play_move(move, turn_id):
        move.wins += 1
        return True
    else:
        move.losses += 1
        return False
