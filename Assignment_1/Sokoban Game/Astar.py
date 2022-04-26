import collections
from queue import PriorityQueue
import copy

board = []
maxLength = 0
boxRobot = []
wallsStorageSpaces = []
possibleMoves = {'Up':[-1,0], 'Right':[0,1],'Down':[1,0],'Left':[0,-1]}
maxRowLength = 0	
lines = 0

print ("Enter the board configuration:")
while(1):	
	line = input()
	if line != "":
		lines += 1
		board.append(line)
		if len(line) > maxRowLength:
			maxRowLength = len(line)
	else:
		break	

import time
time_start = time.process_time()
for i in range(0,lines):
	boxRobot.append([])
	wallsStorageSpaces.append([])
	for j in range(0,maxRowLength):
		boxRobot[-1].append('-')
		wallsStorageSpaces[-1].append('-')

for i in range(0,len(board)):
	if len(board[i]) < maxRowLength:
		for j in range(len(board[i]),maxRowLength):
			board[i] += 'O'

for i in range(0,len(board)):
	for j in range(0,maxRowLength):
		if board[i][j] == 'B' or board[i][j] == 'R':
			boxRobot[i][j]=board[i][j]
			wallsStorageSpaces[i][j]=' '
		elif board[i][j] == 'S' or board[i][j] == 'O':
			wallsStorageSpaces[i][j] = board[i][j]
			boxRobot[i][j] = ' '
		elif board[i][j] == ' ':
			boxRobot[i][j] = ' '
			wallsStorageSpaces[i][j]=' '
		elif board[i][j] == '*':
			boxRobot[i][j] = 'B'
			wallsStorageSpaces[i][j] = 'S'
		elif board[i][j] == '.':
			boxRobot[i][j] = 'R'
			wallsStorageSpaces[i][j] = 'S'

storages = []
for i in range(0,lines):
	for j in range(0,maxRowLength):
		if wallsStorageSpaces[i][j] == 'S':
			storages.append([i,j])

boxRobtDistance = 99999999
boxes = []
storagesLeft = len(storages)
for i in range(0,lines):
	for j in range(0,maxRowLength):
		if boxRobot[i][j] == 'B':
			if wallsStorageSpaces[i][j] == 'S':
				print (i,j)
				storagesLeft -= 1
			boxes.append([i,j])

for i in range(0,lines):
	for j in range(0,maxRowLength):
		if boxRobot[i][j] == 'R':
			for k in boxes:
				if boxRobtDistance > abs(k[0]-i) + abs(k[1]-j):
					boxRobtDistance+=abs(k[0]-i) + abs(k[1]-j)


def manhattan(state):
	distance = 0
	for i in range(0,lines):
		for j in range(0,maxRowLength):
			if state[i][j] == 'B':
				temp= 9999999
				for storage in storages:
					distanceToNearest = abs(storage[0]-i) + abs(storage[1]-j)
					if temp > distanceToNearest:
						temp = distanceToNearest
				distance += temp
	return distance

movesList = []
visitedMoves = []

queue = PriorityQueue()
source = [boxRobot,movesList]
if boxRobot not in visitedMoves:
	visitedMoves.append(boxRobot)
queue.put((boxRobtDistance,source))

robot_x = -1
robot_y = -1
completed = 0

while not queue.empty() and completed == 0:
	temp = queue.get()
	curPosition = temp[1][0]
	movesTillNow = temp[1][1]
	stepsTillNow = len(movesTillNow)

	for i in range(0,lines):
		for j in range(0,maxRowLength):
			if curPosition[i][j] == 'R':
				robot_y = j
				robot_x = i
				break
		else:
			continue
		break

	for key in possibleMoves:
		robotNew_x = robot_x + possibleMoves[key][0]
		robotNew_y = robot_y + possibleMoves[key][1] 
		curPositionCopy = copy.deepcopy(curPosition)
		movesTillNowCopy = copy.deepcopy(movesTillNow)

		if curPositionCopy[robotNew_x][robotNew_y] == 'B':
			boxNew_x = robotNew_x + possibleMoves[key][0]
			boxNew_y = robotNew_y + possibleMoves[key][1]
			if curPositionCopy[boxNew_x][boxNew_y] == 'B' or wallsStorageSpaces[boxNew_x][boxNew_y] == 'O':
				continue
			else:
				curPositionCopy[boxNew_x][boxNew_y] = 'B'
				curPositionCopy[robotNew_x][robotNew_y] = 'R'
				curPositionCopy[robot_x][robot_y] = ' '
				if curPositionCopy not in visitedMoves:
					matches = 0
					for k in range(0,lines):
						for l in range(0,maxRowLength):
							if wallsStorageSpaces[k][l] == 'S':
								if curPositionCopy[k][l] != 'B':
									matches = 1
					movesTillNowCopy.append(key)

					if matches == 0:
						completed = 1
						save = []
						save += movesTillNowCopy
						print(movesTillNowCopy)

					else:
						boxRobtDistance = 999999
						boxes=[]
						storagesLeft = len(storages)
						for i in range(0,lines):
							for j in range(0,maxRowLength):
								if curPositionCopy[i][j] == 'B':
									if wallsStorageSpaces[i][j] == 'S':
						
										storagesLeft -= 1
									boxes.append([i,j])
	
						for i in range(0,lines):
							for j in range(0,maxRowLength):
								if curPositionCopy[i][j] == 'R':
									for k in boxes:
										if boxRobtDistance > abs(k[0]-i) + abs(k[1]-j):
											boxRobtDistance = abs(k[0]-i) + abs(k[1]-j)

						storagesLeft = 0
						queue.put((manhattan(curPositionCopy) + boxRobtDistance+storagesLeft*2+stepsTillNow,[curPositionCopy,movesTillNowCopy]))
						visitedMoves.append(curPositionCopy)
		else:
			if wallsStorageSpaces[robotNew_x][robotNew_y] == 'O' or curPositionCopy[robotNew_x][robotNew_y] != ' ':
				continue
			else:
				curPositionCopy[robotNew_x][robotNew_y] = 'R'
				curPositionCopy[robot_x][robot_y] = ' '
				if curPositionCopy not in visitedMoves:
					movesTillNowCopy.append(key)
					boxRobtDistance = 999999
					boxes = []
					storagesLeft = len(storages)
					for i in range(0,lines):
						for j in range(0,maxRowLength):
							if curPositionCopy[i][j] == 'B':
								if wallsStorageSpaces[i][j] == 'S':
									storagesLeft -= 1
								boxes.append([i,j])

					for i in range(0,lines):
						for j in range(0,maxRowLength):
							if curPositionCopy[i][j] == 'R':
								for k in boxes:
									if boxRobtDistance > abs(k[0]-i) + abs(k[1]-j):
										boxRobtDistance = abs(k[0]-i) + abs(k[1]-j)
					storagesLeft = 0
					queue.put((manhattan(curPositionCopy) + boxRobtDistance + storagesLeft*2 + stepsTillNow,[curPositionCopy,movesTillNowCopy]))
					visitedMoves.append(curPositionCopy)

if completed == 0:
	print ("Can't make it")

time_end = time.process_time()
print ("Run time: "+str(time_end - time_start))

result = []
for i in range(0,len(board)):
	row = []
	for j in range(0,maxRowLength):
		row.append(board[i][j])
	result.append(row)
print("--------------------------")
print("Initial State")
print()
for i in range(0,len(board)):
		for j in range(0,maxRowLength):
			print(result[i][j],sep='',end='')
		print()
print()
print("--------------------------")
result = []
for i in range(0,len(board)):
	row = []
	for j in range(0,maxRowLength):
		row.append(board[i][j])
	result.append(row)
print("--------------------------")
for step in save:
	for i in range(0,len(result)):
		done = 0
		for j in range(0,maxRowLength):	
			if result[i][j] == 'R' or result[i][j] == 'X':
				if result[i][j] == 'X' :
					result[i][j] = 'S'
				elif result[i][j] == 'R':
					result[i][j] = ' '
				if step == 'Up':
					if i-1 > -1:
						if result[i-1][j] == 'B':
							if result[i-2][j] == 'S': result[i-2][j] = '*'
							else: result[i-2][j] = 'B'
							result[i-1][j] = 'R'
						elif result[i-1][j] == '*': 
							if result[i-2][j] == 'S': result[i-2][j] = '*'
							else: result[i-2][j] = 'B'
							result[i-1][j] = 'X'
						elif result[i-1][j] == ' ':
							result[i-1][j] = 'R' 
						elif result[i-1][j] == 'S':
							result[i-1][j] = 'X' 
						done = 1
						break
				elif step == 'Down':
					if i+1 < len(result):
						if result[i+1][j] == 'B':
							if result[i+2][j] == 'S': result[i+2][j] = '*'
							else: result[i+2][j] = 'B'
							result[i+1][j] = 'R'
						elif result[i+1][j] == '*':
							if result[i+2][j] == 'S': result[i+2][j] = '*'
							else: result[i+2][j] = 'B'
							result[i+1][j] = 'X'
						elif result[i+1][j] == ' ':
							result[i+1][j] = 'R' 
						elif result[i+1][j] == 'S':
							result[i+1][j] = 'X' 
						done = 1
						break
				elif step == 'Right':
					if result[i][j+1] == 'B':
						if result[i][j+2] == 'S': result[i][j+2] = '*'
						else: result[i][j+2] = 'B'
						result[i][j+1] = 'R'
					elif result[i][j+1] == '*':
						if result[i][j+2] == 'S': result[i][j+2] = '*'
						else: result[i][j+2] = 'B'
						result[i][j+1] = 'X'
					elif result[i][j+1] == ' ':
						result[i][j+1] = 'R' 
					elif result[i][j+1] == 'S':
						result[i][j+1] = 'X' 
					done = 1
					break
				elif step == 'Left':
					if result[i][j-1] == 'B':
						if result[i][j-2] == 'S': result[i][j-2] = '*'
						else: result[i][j-2] = 'B'
						result[i][j-1] = 'R'
					elif result[i][j-1] == '*':
						if result[i][j-2] == 'S': result[i][j-2] = '*'
						else: result[i][j-2] = 'B'
						result[i][j-1] = 'X'
					elif result[i][j-1] == ' ':
						result[i][j-1] = 'R' 
					elif result[i][j-1] == 'S':
						result[i][j-1] = 'X' 
					done = 1
					break
    			
		if done == 1: break	
	print()	
	print("=> Action was",end = ' ') 
	print(step)
	print()
	for a in range(0,len(board)):
		for b in range(0,maxRowLength):
			print(result[a][b],sep = '',end = '')
		print()
	print("--------------------------")
