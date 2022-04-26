"""
Compares Ultimate Tic Tac Toe game tree heuristics.
"""

import random
import time
import argparse

from engine.GameTree import GameTree
from UTTTState import UTTTState
from UTTTSpace import UTTTSpace
from heuristic import heuristic_A, heuristic_B
from mcts import mcts_player, mcts_reset

TRACE = False
DICTATE = False

def always_choose_random_state(node):
    """
    Makes a random move.
    """
    return random.randint(0, len(node.successors()) - 1)


def trace(*args):
    global TRACE
    if TRACE:
        print(*args)

def against_random(trials, depths, heuristics):
    """
    Tests each heuristic against a random player.
    """

    global DICTATE

    print("=== Heuristic against Random ===")

    # Testing for standard UTTT board.
    print("{:<12}{:<15}{:<8}{:<15}{:<13}{:<15}".format("# Trials", "Heuristic", "Depth", "Avg Runtime", "Win Rate", "Player 0"))

    for hName, hFunc in sorted(heuristics.items()):
        trace("[Heuristic {}]".format(hName))

        all_time = 0
        all_wins = 0

        for d in depths:
            trace("[Heuristic {}; Depth: {}]".format(hName, d))

            all_order_time = 0
            all_order_wins = 0

            for opponent_first in [True, False]:
                player_zero = ("Opponent" if opponent_first else "AI")

                trace("[Heuristic {}; Depth: {}; Player Zero: {}]".format(hName, d, player_zero))

                # Force AI to be Player with id 0 always.
                initial_state = UTTTState(1 if opponent_first else 0, None, None, UTTTSpace(None, 3, 3))

                i_time = 0
                i_wins = 0

                for t in range(trials):
                    trace("[Heuristic {}; Depth: {}; Player Zero: {}; Trial: {}]".format(hName, d, player_zero, t))

                    # Instantiate the game tree.
                    game = GameTree(initial_state, opponent_first, d)

                    game.DICTATE = DICTATE

                    # Test against random.
                    game.attach_turn_handler(always_choose_random_state)

                    if hName.upper() == "MCTS":
                        hFunc = None
                        mcts_reset()
                        game.attach_tester_handler(mcts_player)

                    start = time.time()
                    win = game.play(hFunc)
                    i_time += time.time() - start
                    i_wins += 1 if win else 0

                avg_time = i_time / trials
                percent_win = i_wins / trials

                print("{:<12}{:<15}{:<8}{:<15.3f}{:<13.3f}{:<15}".format(trials, hName, d, avg_time, percent_win, player_zero))

                all_order_time += avg_time
                all_order_wins += percent_win

            # Average over opponent starting vs. AI starting.
            avg_time = all_order_time / 2.0
            percent_win = all_order_wins / 2.0

            print("{:<12}{:<15}{:<8}{:<15.3f}{:<13.3f}{:<15}".format(trials * 2, hName, d, avg_time, percent_win, 'Both'))

            all_time += avg_time
            all_wins += percent_win

        # Average over opponent starting vs. AI starting.
        avg_time = all_time / float(len(depths) + 1)
        percent_win = all_wins / float(len(depths) + 1)

        print("{:<12}{:<15}{:<8}{:<15.3f}{:<13.3f}{:<15}".format(trials * 2 * (range(depths) + 1), hName, 'All', avg_time, percent_win, 'Both'))


def baseline():
    """
    Pits random against random.
    """

    global DICTATE

    print("== Random against Random ==")

    # Testing for standard UTTT board.
    print("{:<12}{:<15}{:<13}{:<15}".format("# Trials", "Avg Runtime", "Win Rate", "Player 0"))

    trials = 50
    all_time = 0
    all_wins = 0

    for opponent_first in [True, False]:
        player_zero = ("Opponent" if opponent_first else "AI")

        trace("Player Zero: {}]".format(player_zero))

        # Force AI to be Player with id 0 always.
        initial_state = UTTTState(1 if opponent_first else 0, None, None, UTTTSpace(None, 3, 3))

        i_time = 0
        i_wins = 0

        for t in range(trials):
            trace("[Player Zero: {}; Trial: {}]".format(player_zero, t))

            # Instantiate the game tree.
            game = GameTree(initial_state, opponent_first)

            # Test against random.
            game.attach_turn_handler(always_choose_random_state)
            game.attach_tester_handler(always_choose_random_state)

            game.DICTATE = DICTATE

            start = time.time()
            win = game.play()
            i_time += time.time() - start
            i_wins += 1 if win else 0

        avg_time = i_time / trials
        percent_win = i_wins / trials

        print("{:<12}{:<15.3f}{:<13.3f}{:<15}".format(trials, avg_time, percent_win, player_zero))

        all_time += avg_time
        all_wins += percent_win

    # Average over opponent starting vs. AI starting.
    avg_time = all_time / 2.0
    percent_win = all_wins / 2.0

    print("{:<12}{:<15.3f}{:<13.3f}{:<15}".format(trials * 2, avg_time, percent_win, 'Both'))

"""
Entry point for Ultimate Tic Tac Toe game tree demo.
"""
def main():
    """
    Collects win and runtime stats on each heuristic at differing depths.
    """
    trials = 5
    depths = [1, 2, 3]
    heuristics = { 'A': heuristic_A, 'B': heuristic_B, 'MCTS': mcts_player }

    print("===")
    print("Performing tests...")
    print("===")
    print("")

    baseline()
    print("")
    against_random(trials, depths, heuristics)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compares heuristics.')
    parser.add_argument('--trace', dest='TRACE', action='store_true', help='Enables minimal tracing.')
    parser.add_argument('--dictate', dest='DICTATE', action='store_true', help='Enables move dictation.')
    args = parser.parse_args()

    TRACE = args.TRACE
    DICTATE = args.DICTATE

    main()
