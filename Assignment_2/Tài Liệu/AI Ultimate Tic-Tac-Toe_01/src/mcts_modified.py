from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 600
explore_faction = 1.4

# Given a node returns the confidence interval
def find_confidence_num(node):
    return (node.wins/node.visits) + explore_faction * sqrt((log(node.parent.visits))/node.visits)


def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    # Uses upper confidence bound to either exploit or explore new nodes
    # Traverse down tree with biasing choice for child nodes until leaf node and return
    
    maxNumber = 0
    maxNode = node

    for childNode in node.child_nodes.values():
        if find_confidence_num(childNode) > maxNumber and childNode.visits > 0:
            maxNumber = find_confidence_num(childNode)
            maxNode = childNode

    return maxNode
    
    # Hint: return leaf_node

    # if move == "q":
    # 	exit(2)
    # action = board.pack_action(move)
    # if board.is_legal(state, action):


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """

    # Create new node (random state) and return the node

    # Check to see if node is terminating
    next_move = choice(node.untried_actions)
    node.untried_actions.remove(next_move)
    # newState = board.next_state(state, next_move)
    new_node = MCTSNode(node, next_move, node.untried_actions) #Since we removed the action to untried action it consists of the rest of possible board actions
    node.child_nodes[next_move] = new_node # Set action to new node
    return new_node

    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    # Play a random games and check win or lose in think()
    # action = (1, 2, 3, 4) --> list[i]; action[2] = 3, action[3] = 4
    
    while board.is_ended(state) == False:
        betterAction = False
        actions = board.legal_actions(state)
        for currAction in actions:
            if(currAction[2] == 1 and currAction[3] == 1):
                state = board.next_state(state, currAction)
                betterAction = True
        
        if(betterAction == False):
            state = board.next_state(state, choice(actions))

    return board.points_values(state)


    


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    # Go back up to the root node (starting state) while updating win/visit values of every node along path
    while node != None:
        if won == 1:
            node.wins = node.wins + 1
        node.visits = node.visits + 1
        node = node.parent

def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    # Passes in the current state of game with the action list 

    # Iterates through number of playthroughs(?)
    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state
        # Start at root
        node = root_node
        # Do MCTS - This is all you!
        #print("ONE FOR LOOP FOR ONE SIMULATION")
        
        # Selection process
        # While node that has untried actions and no child nodes call traverse and update sampled game
        # and traverse one level towards most promising child node
        while not node.untried_actions and node.child_nodes:
            #print("Traversing\n")
            node.visits = node.visits + 1
            node = traverse_nodes(node, board, sampled_game, identity_of_bot)
            # If parent_action of the leaf node exists then update state
            if node.parent_action:
                sampled_game = board.next_state(sampled_game, node.parent_action)


        # Expansion process 
        # To add a new child node to the leaf node to run a random playout from there
        if node.untried_actions:
            #print("Expanding\n")
            node = expand_leaf(node, board, sampled_game)
            #print("Parent node is: " + str(node.parent_action) + "\n")
            # node = traverse_nodes(node, board, sampled_game, identity_of_bot)
            sampled_game = board.next_state(sampled_game, node.parent_action)


        # Rollout process
        # result = board.points_values(state) # {1:-1, 2: 1} player 1 loses and player 2 win
        result = rollout(board, sampled_game)
        #print("result of playout is "+str(result))
        if identity_of_bot == 1:
            win_state = result[1]
        elif identity_of_bot == 2:
            win_state = result[2]


        # Backpropagagate process
        backpropagate(node, win_state)


    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.

    bestScore = 0
    bestMove = choice(board.legal_actions(state))
    for child in root_node.child_nodes.values():
        if (child.wins/child.visits) > bestScore:
            bestScore = child.wins/child.visits
            bestMove = child.parent_action
    return bestMove
