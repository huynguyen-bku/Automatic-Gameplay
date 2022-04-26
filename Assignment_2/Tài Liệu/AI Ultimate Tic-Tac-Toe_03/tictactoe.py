"""
Ultimate Tic Tac Toe game tree solver.
"""

import random
import argparse
import time

from engine.GameTree import GameTree
from UTTTState import UTTTState
from UTTTSpace import UTTTSpace
from heuristic import heuristic_A, heuristic_B
from mcts import mcts_player, mcts_reset

TRACE_CHILDREN = True

def user_turn_handler(node):
    """
    Turn handler which retrieves input from a human player.
    """
    global TRACE_CHILDREN

    sc = node.successors()
    if TRACE_CHILDREN:
        for i in range(len(sc)):
            print("#" + str(i), str(sc[i]))

    while True:
        try:
            index = int(input("Enter the move id ({} - {}): ".format(0, len(sc) - 1)))
            if index < 0 or index >= len(sc):
                print("Out of bounds.")
                continue
            return index
        except:
            print("Unable to read as integer.")
            pass

    return None

def always_choose_random_state(node):
    """
    Makes a random move.
    """
    return random.randint(0, len(node.successors()) - 1)

def always_choose_first_state(node):
    return 0

def always_choose_last_state(node):
    sc = node.successors()
    length = len(sc) - 1
    return length

"""
Entry point for Ultimate Tic Tac Toe game tree demo.
"""
def main():
    global TRACE_CHILDREN

    non_interactive = {
        'random': always_choose_random_state,
        'first': always_choose_first_state,
        'last': always_choose_last_state
    }
    heuristics = { 'a': heuristic_A, 'b': heuristic_B }

    parser = argparse.ArgumentParser(description='Runs the game engine.')
    parser.add_argument('--no-trace', dest='TRACE_CHILDREN', action='store_false', help='Disables full tracing of successor states.')
    parser.add_argument('--computer-first', dest='COMPUTER_FIRST', action='store_true', help='Makes the AI go first.')
    parser.add_argument('--heuristic', default='a', type=str.lower, dest='heuristic', choices=(list(sorted(heuristics.keys())) + ['mcts']), help='Selects a heuristic for the AI to move.')
    parser.add_argument('--depth', default=2, type=int, dest='depth', help='Depth limit for game tree.')
    parser.add_argument('--non-interactive', dest='noninteractive', type=str.lower, choices=sorted(non_interactive.keys()), help='Use a non-interactive turn handler.')
    parser.add_argument('--rtrials', default=0, dest='rtrials', type=int, help='Number of random trials to conduct. Forces non-interactive=random.')
    parser.add_argument('--mcts-time', dest='mcts_time', default=3, type=int, help='Maximum time (seconds) to run MCTS simulations per move decision.')
    args = parser.parse_args()

    if args.depth <= 0:
        raise 'Depth must be positive.'

    TRACE_CHILDREN = args.TRACE_CHILDREN

    if args.heuristic == "mcts":
        print("Using heuristic '{}'. Ignoring depth.".format(args.heuristic))
    else:
        print("Using heuristic '{}' with depth '{}'.".format(args.heuristic, args.depth))

    # Force AI to be Player with id 0 always.
    initial_state = UTTTState(0 if args.COMPUTER_FIRST else 1, None, None, UTTTSpace(None, 3, 3))

    if args.rtrials > 0:
        args.noninteractive = 'random'
    else:
        args.rtrials = 1

    if args.noninteractive is not None:
        print("Using non-interactive turn handler: {}".format(args.noninteractive))
    else:
        print("Using a human-input user turn handler.")

    total_time = 0
    total_wins = 0
    for t in range(args.rtrials):
        # Instantiates a game tree.
        game = GameTree(initial_state, not args.COMPUTER_FIRST, args.depth)

        if args.noninteractive is not None:
            game.attach_turn_handler(non_interactive[args.noninteractive])
        else:
            game.attach_turn_handler(user_turn_handler)

        start = time.time()

        i_won = False
        if args.heuristic == 'mcts':
            mcts_reset(args.mcts_time)
            game.attach_tester_handler(mcts_player)
            i_won = game.play()
        else:
            i_won = game.play(heuristics[args.heuristic])

        runtime = time.time() - start
        total_time += runtime

        player = args.heuristic.upper()
        opponent = args.noninteractive.upper() if args.noninteractive is not None else "Human"

        if i_won:
            total_wins += 1
            print("[Trial {}] {} won. {} lost.".format(t, player, opponent))
        else:
            print("[Trial {}] {} lost. {} won.".format(t, player, opponent))

        print("[Trial {}] Runtime: {:6.3f}".format(t, runtime))

    print("Avg Runtime Over {} trials: {:6.3f}; Win Rate: {:6.3f}".format(args.rtrials, total_time / args.rtrials, total_wins / args.rtrials))


if __name__ == "__main__":
    main()
