from engine.GameTree import *
from UTTTState import *
from UTTTSpace import *

def heuristic_A(turn_id, node):

    grade = 0

    # The state with more child will get priority
    children = node.successors()
    if (node.turn == turn_id):
        grade += len(children)
        if node.is_winner(turn_id):
            return 100
    else:
        grade -= len(children)
        if node.is_winner(1 - turn_id):
            return -100

    # check whether the middle subgame is won by anyone
    if (node.space.N % 2 == 1):
        middle = 0
        for k in node.space.subgames:
            if (node.space.subgames[k] != None):
                if k == (node.space.N % 2, node.space.N % 2):
                    middle = 1

        mark = []
        if middle == 1:
            row_num = 1
            colum_num = 1
            row_one = []
            row_two = []
            for y in range(node.space.N * node.space.n):
                row_one.append(1)
                if y == colum_num:
                    row_two.append(2)
                    colum_num += 3
                else:
                    row_two.append(1)

            for y in range(node.space.N * node.space.n):
                if y == row_num:
                    mark.append(row_two)
                    row_num += 3
                else:
                    mark.append(row_one)

        else:
            row_num = 1
            colum_num = 1
            row_one = []
            row_two = []
            for y in range(node.space.N * node.space.n):
                row_one.append(1)
                if y == colum_num:
                    row_two.append(0)
                    colum_num += 3
                else:
                    row_two.append(1)

            for y in range(node.space.N * node.space.n):
                if y == row_num:
                    mark.append(row_two)
                    row_num += 3
                else:
                    mark.append(row_one)

        # More middle block in the subgame will earn more grade
        if (node.turn == turn_id):
            for y in range(node.space.N * node.space.n):
                for x in range(node.space.N * node.space.n):
                    cell = node.space.cells[(node.space.N * node.space.n * y) + x]
                    if cell == turn_id:
                        grade += mark[y][x]
        else:
            for y in range(node.space.N * node.space.n):
                for x in range(node.space.N * node.space.n):
                    cell = node.space.cells[(node.space.N * node.space.n * y) + x]
                    if cell == 1 - turn_id:
                        grade -= mark[y][x]

    # if the opponent already ocupy two connected block in a subgame, then don not choose that subgame again
    coord = []
    parent = node.parent

    for move in parent.possible_moves():
        (_, _, iX, iY) = move
        # Warning, a full copy of the space occurs here.
        child = UTTTState(1 - parent.turn, parent, (iX, iY))
        if(child.restriction == node.restriction ):
            coord = [iX, iY]

    # if in a sub game, two of mine nodes are connected, then it will have a higher gread
    if (node.restriction != None and node.turn == turn_id):
        #check colum
        for cx in range(node.space.n):
            opponent = 0
            mine = 0
            for cy in range(node.space.n):
               if node.space.get((coord[0], coord[1], cx, cy)) == 1 - turn_id:
                   opponent += 1
               elif node.space.get((coord[0], coord[1], cx, cy)) == turn_id:
                   mine += 1
            if mine == node.space.n - 1 and opponent == 0:
                grade += 1

        #check row
        for cy in range(node.space.n):
            opponent = 0
            mine = 0
            for cx in range(node.space.n):
               if node.space.get((coord[0], coord[1], cx, cy)) == 1 - turn_id:
                   opponent += 1
               elif node.space.get((coord[0], coord[1], cx, cy)) == turn_id:
                   mine += 1
            if mine == node.space.n - 1 and opponent == 0:
                grade += 1

        # check diagonals
        cx = 0
        cy = 0
        opponent = 0
        mine = 0
        while (cx < node.space.n and cy < node.space.n):
            if node.space.get((coord[0], coord[1], cx, cy)) == 1 - turn_id:
                opponent += 1
            elif node.space.get((coord[0], coord[1], cx, cy)) == turn_id:
                mine += 1
            cx += 1
            cy += 1
        if mine == node.space.n - 1 and opponent == 0:
            grade += 1

        cx = node.space.n - 1
        cy = node.space.n - 1
        opponent = 0
        mine = 0
        while (cx >= 0 and cy >= 0):
            if node.space.get((coord[0], coord[1], cx, cy)) == 1 - turn_id:
                opponent += 1
            elif node.space.get((coord[0], coord[1], cx, cy)) == turn_id:
                mine += 1
            cx -= 1
            cy -= 1
        if mine == node.space.n - 1 and opponent == 0:
            grade += 1


    #if two of opponent blockes are connected, then get lower gread
    if (node.restriction != None and node.turn == 1 - turn_id):
        #check colum
        for cx in range(node.space.n):
            opponent = 0
            mine = 0
            for cy in range(node.space.n):
               if node.space.get((coord[0], coord[1], cx, cy)) == turn_id:
                   opponent += 1
               elif node.space.get((coord[0], coord[1], cx, cy)) == 1 - turn_id:
                   mine += 1
            if opponent == node.space.n - 1 and mine == 0:
                grade -= 1

        #check row
        for cy in range(node.space.n):
            opponent = 0
            mine = 0
            for cx in range(node.space.n):
               if node.space.get((coord[0], coord[1], cx, cy)) == turn_id:
                   opponent += 1
               elif node.space.get((coord[0], coord[1], cx, cy)) == 1 - turn_id:
                   mine += 1
            if opponent == node.space.n - 1 and mine == 0:
                grade -= 1

        # check diagonals
        cx = 0
        cy = 0
        opponent = 0
        mine = 0
        while (cx < node.space.n and cy < node.space.n):
            if node.space.get((coord[0], coord[1], cx, cy)) == turn_id:
                opponent += 1
            elif node.space.get((coord[0], coord[1], cx, cy)) == 1 - turn_id:
                mine += 1
            cx += 1
            cy += 1
        if opponent == node.space.n - 1 and mine == 0:
            grade -= 1

        cx = node.space.n - 1
        cy = node.space.n - 1
        opponent = 0
        mine = 0
        while (cx >= 0 and cy >= 0):
            if node.space.get((coord[0], coord[1], cx, cy)) == turn_id:
                opponent += 1
            elif node.space.get((coord[0], coord[1], cx, cy)) == 1 - turn_id:
                mine += 1
            cx -= 1
            cy -= 1
        if opponent == node.space.n - 1 and mine == 0:
            grade -= 1


    return grade


# selection of more useful heuristic from function heuristic_A
def heuristic_B(turn_id, node):
    grade = 0

    # The state with more child will get priority
    children = node.successors()
    if (node.turn == turn_id):
        grade += len(children)
        if node.is_winner(turn_id):
            return 100
    else:
        grade -= len(children)
        if node.is_winner(1 - turn_id):
            return -100


    # check whether the middle subgame is won by anyone
    if (node.space.N % 2 == 1):
        middle = 0
        for k in node.space.subgames:
            if (node.space.subgames[k] != None):
                if k == (node.space.N % 2, node.space.N % 2):
                    middle = 1

        mark = []
        if middle == 1:
            row_num = 1
            colum_num = 1
            row_one = []
            row_two = []
            for y in range(node.space.N * node.space.n):
                row_one.append(1)
                if y == colum_num:
                    row_two.append(2)
                    colum_num += 3
                else:
                    row_two.append(1)

            for y in range(node.space.N * node.space.n):
                if y == row_num:
                    mark.append(row_two)
                    row_num += 3
                else:
                    mark.append(row_one)

        else:
            row_num = 1
            colum_num = 1
            row_one = []
            row_two = []
            for y in range(node.space.N * node.space.n):
                row_one.append(1)
                if y == colum_num:
                    row_two.append(0)
                    colum_num += 3
                else:
                    row_two.append(1)

            for y in range(node.space.N * node.space.n):
                if y == row_num:
                    mark.append(row_two)
                    row_num += 3
                else:
                    mark.append(row_one)

        # More middle block in the subgame will earn more grade
        if (node.turn == turn_id):
            for y in range(node.space.N * node.space.n):
                for x in range(node.space.N * node.space.n):
                    cell = node.space.cells[(node.space.N * node.space.n * y) + x]
                    if cell == turn_id:
                        grade += mark[y][x]

        else:
            for y in range(node.space.N * node.space.n):
                for x in range(node.space.N * node.space.n):
                    cell = node.space.cells[(node.space.N * node.space.n * y) + x]
                    if cell == 1 - turn_id:
                        grade -= mark[y][x]

    return grade
