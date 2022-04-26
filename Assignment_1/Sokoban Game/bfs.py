import collections
import copy

board = []
maxLength=0
boxRobot = []
wallsStorageSpaces = []
possibleMoves = {'Up':[-1,0], 'Right':[0,1],'Down':[1,0],'Left':[0,-1]}
maxRowLength = 0	
lines = 0

print ("Enter the board configuration:")
while(1):
	line = input()
	if line != "" :
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


## Making the board a rectangle even if the input is not one
for i in range(0,len(board)):
	if len(board[i]) < maxRowLength:
		for j in range(len(board[i]),maxRowLength):
			board[i] += 'O'


## Storing walls&storage spaces in one 2d array , boxes and robot in another 2d array
for i in range(0,len(board)):
	for j in range(0,maxRowLength):
		if board[i][j] == 'B' or board[i][j] == 'R':
			boxRobot[i][j]=board[i][j]
			wallsStorageSpaces[i][j] = ' '
		elif board[i][j] == 'S' or board[i][j] == 'O':
			wallsStorageSpaces[i][j] = board[i][j]
			boxRobot[i][j] = ' '
		elif board[i][j] == ' ':
			boxRobot[i][j] = ' '
			wallsStorageSpaces[i][j] = ' '
		elif board[i][j] == '*':
			boxRobot[i][j] = 'B'
			wallsStorageSpaces[i][j] = 'S'
		elif board[i][j] == '.':
			boxRobot[i][j] = 'R'
			wallsStorageSpaces[i][j] = 'S'

##BFS
print("Solving using BFS\n")

movesList = []
visitedMoves = []

## Adding source to queue
queue = collections.deque([])
source = [boxRobot,movesList]
if boxRobot not in visitedMoves:
	visitedMoves.append(boxRobot)
queue.append(source)
robot_x = -1
robot_y = -1
completed = 0
while len(queue) != 0 and completed == 0:

	# Popping first item from the queue
	temp = queue.popleft()
	curPosition = temp[0]
	movesTillNow = temp[1]

	for i in range(0,lines):
		for j in range(0,maxRowLength):
			if curPosition[i][j] == 'R':
				robot_y = j
				robot_x = i
				break
		else:
			continue
		break

	#Getting robot position of the popped element.
	for key in possibleMoves:
		# Checking for all the four directions
		robotNew_x = robot_x + possibleMoves[key][0]
		robotNew_y = robot_y + possibleMoves[key][1] 
		curPositionCopy = copy.deepcopy(curPosition)

		movesTillNowCopy = copy.deepcopy(movesTillNow)
		if curPositionCopy[robotNew_x][robotNew_y] == 'B':
			# If there is a box after robot makes a move
			boxNew_x = robotNew_x + possibleMoves[key][0]
			boxNew_y = robotNew_y + possibleMoves[key][1]
			if curPositionCopy[boxNew_x][boxNew_y] == 'B' or wallsStorageSpaces[boxNew_x][boxNew_y] == 'O':
				# if the cell after robot pushes the box is another box or wall, avoid further steps.
				continue
			else:
				# if the robot can push the block
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
						queue.append([curPositionCopy,movesTillNowCopy])
						visitedMoves.append(curPositionCopy)
		else:
			# if the robot moves into a wall
			if wallsStorageSpaces[robotNew_x][robotNew_y] == 'O': 
				continue
			else:
				# if the robot moves into empty space
				curPositionCopy[robotNew_x][robotNew_y] = 'R'
				curPositionCopy[robot_x][robot_y] = ' '
				if curPositionCopy not in visitedMoves:
					movesTillNowCopy.append(key)
					queue.append([curPositionCopy,movesTillNowCopy])
					visitedMoves.append(curPositionCopy)

if completed == 0:
	print("Can't make it")

time_end = time.process_time()
print("Run time: " + str(time_end - time_start))

result = []
for i in range(0,len(board)):
	row = []
	for j in range(0,maxRowLength):
		row.append(board[i][j])
	result.append(row)
print("--------------------------")
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
			print(result[i][j],sep = '',end = '')
		print()
print()
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
