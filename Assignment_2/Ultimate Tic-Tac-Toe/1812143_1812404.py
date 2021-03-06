import numpy as np
import copy
import state

def select_move(cur_state, remain_time):
    valid_moves = cur_state.get_valid_moves
    if cur_state.previous_move == None:
       return state.UltimateTTT_Move(4,1,1,1)
    cur_state_new = copy.deepcopy(cur_state)
    all_moves = cur_state_new.get_valid_moves
    depth = 4
    if len(all_moves) != 0:
        return Minimax(cur_state_new,depth,True)[0]
    return None
def Minimax(cur_state,depth,player):
    valid_moves = cur_state.get_valid_moves
    if depth == 0 or len(valid_moves) == 0:
        return cur_state, evaluate(cur_state)
    if player:
        MaxValue = float('-inf')
        Best_cur_state = None
        for step in valid_moves:
            term_state = copy.deepcopy(cur_state)
            term_state.act_move(step)
            value = Minimax(term_state,depth-1,False)[1]
            MaxValue = max(MaxValue,value)
            if MaxValue == value:
                Best_cur_state =  step
        return Best_cur_state, MaxValue


    else:
        MinValue = float('inf')
        Best_cur_state = None
        for step in valid_moves:
            term_state = copy.deepcopy(cur_state)
            term_state.act_move(step)
            value = Minimax(term_state,depth-1,True)[1]
            MinValue = min(MinValue,value)
            if MinValue == value:
                Best_cur_state =  step
        return Best_cur_state, MinValue


def evaluate(cur_state):
    score = get_score(cur_state)
    return score

def empty_cells_small_boards(board):
    empty_cells = []
    for y,row in enumerate(board):
        for x,case in enumerate(row):
            if case == 0:
                empty_cells.append([x,y])

    return empty_cells

def get_score(cur_state):
    player = cur_state.player_to_move
    score = 0 
    result= cur_state.global_cells.reshape(3,3)

    for row in result: 
        score += count_score_glopal(row,player)

    for col in range(len(result)): 
        check = []
        for row in range(len(result)):
            check.append(result[row][col])
        score += count_score(check, player)

    diags = []
    for indx in range(len(result)):
        diags.append(result[indx][indx])
    score += count_score_glopal(diags, player)

    diags_2 = []
    for indx, rev_indx in enumerate(reversed(range(len(result)))):
        diags_2.append(result[indx][rev_indx])
    score += count_score_glopal(diags_2, player)

    for box in cur_state.blocks:
        score += eval_box(box,player)
    return score
    
    
def eval_box(box,player):
    score = 0
    for row in box: 
        score += count_score(row, player)

    for col in range(len(box)): 
        check = []
        for row in range(len(box)):
            check.append(box[row][col])
        score += count_score(check, player)

    diags = []
    for indx in range(len(box)):
        diags.append(box[indx][indx])
    score += count_score(diags, player)

    diags_2 = []
    for indx, rev_indx in enumerate(reversed(range(len(box)))):
        diags_2.append(box[indx][rev_indx])
    score += count_score(diags_2, player)

    if len(empty_cells_small_boards(box)) == 0:
        score += 1

    return score

def count_score(array, player):
    opp_player = -player
    score = 0
    count_1 = np.count_nonzero(array == player)
    count_2 = np.count_nonzero(array == opp_player)

    if count_1 == 3:
        score += 100
    elif count_1 == 2:
        score += 50
    elif count_1 == 1:
        score += 20    
    if count_2 == 3:
        score -= 100
    elif count_2 == 2:
        score -= 50
    if count_1 == 1 and count_2 == 2:
        score += 10

    return score

def count_score_glopal(array, player):
    opp_player = -player
    score = 0
    count_1 = np.count_nonzero(array == player)
    count_2 = np.count_nonzero(array == opp_player)
    if count_1 == 3:
        score += 300
    elif count_1 == 2:
        score += 150
    elif count_1 == 1:
        score += 60
    if count_2 == 3:
        score -= 300
    elif count_2 == 2:
        score -= 150
    if count_1 == 1 and count_2 == 2:
        score += 30

    return score