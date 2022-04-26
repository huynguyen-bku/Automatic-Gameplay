# system imports
import copy
import os
import random
import sys
import config

# pygame imports
import pygame
from pygame.locals import *

########################### CONSTANTS #########################

# Game window width and height
makeFullscreen = config.makeFullscreen

# Current Window coordinates
WINDOWWIDTH = 800
WINDOWHEIGHT = 700

FPS = 30  # The infinite loops runs 30 times in one second

# How big should be one small box
# when you modify this, also modify the MARK SIZE, as the X lives inside a box
BOXSIZE = 43  # Box where X lives
MARKSIZE = 41  # Size of X

SMALLFONTSIZE = 30  # For writing score

# Width of the line in pixels : This is the thing that actually separate the input small boxes
GAPSIZE = 2

# square board size
BOARDSIZE = 9
BIGBOXSIZE = 3

# Playing board width : How many small boxes needs to fit in the board
BOARDWIDTH = BOARDSIZE
BOARDHEIGHT = BOARDSIZE

# TEXT Markers to be drawn
XMARK = 'X'
OMARK = 'O'

'''
Board size = BOXSIZE + GAPSIZE
# The BOARD IS SQUARE. so same size in width and height.

remaining space on X axis = (Window width - Board size)
Margin on X axis = remaining space on X axis // 2

remaining space on Y axis = (Window height - Board size)
Margin on Y axis = remaining space on Y axis // 2

Note that these margins are coordinates
'''

XMARGIN = (WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) // 2
YMARGIN = (WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) // 2

# RGB COLOUR MODEL
#            R    G    B
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
COMBLUE = (233, 232, 255)

# GAME COLOR SCHEME

appBgColor = GRAY  # Background Color
winLineColor = YELLOW  # The line which joins 3 consecutive elements at the end
safeBoxColor = GREEN  # Color for box which are safe to move

mainFontPath = "assets/Raleway-Regular.ttf"
smallFontPath = "assets/Raleway-Regular.ttf"


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller

    :param relative_path: Simply pass the relative path
    :return: Absolute path
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main(level, mode):
    # Initialise pygame to access all video modules
    pygame.init()

    global FPSCLOCK, DISPLAYSURFACE, winner_records

    # Hold the clock as a variable - to tick later : controls the loop iterations per second.
    FPSCLOCK = pygame.time.Clock()

    # The Surface over which everything will be drawn - Window width and height
    if (makeFullscreen):
        # Get user's screen resolution
        user_info = pygame.display.Info()
        DISPLAYSURFACE = pygame.display.set_mode(
            (user_info.current_w, user_info.current_h), pygame.FULLSCREEN)
    else:
        DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    # Modification required : Remove magic number & put something relative to box
    mainFont = pygame.font.Font(resource_path(mainFontPath), MARKSIZE)
    # smallFont : draws the score box and the end game credits
    smallFont = pygame.font.Font(resource_path(smallFontPath), SMALLFONTSIZE)

    # Caption of window
    pygame.display.set_caption('Ultimate Tic-Tac-Toe')

    # Initialise Mouse coordinates
    mousex = 0
    mousey = 0

    # Initialise score board variables
    playerScore = 0
    computerScore = 0
    tieScore = 0

    # Sound Clips

    # sound of Player 1 move
    BEEP1 = pygame.mixer.Sound(resource_path("assets/beep2.ogg"))

    # sound of Player 2 move
    BEEP2 = pygame.mixer.Sound(resource_path("assets/beep3.ogg"))

    # Winning sound of any player
    BEEP3 = pygame.mixer.Sound(resource_path("assets/beep1.ogg"))

    # computer voice at the end of game
    COMPUTERVOICE = pygame.mixer.Sound(
        resource_path("assets/wargamesclip.ogg"))

    '''
    Defines the major data structure 
    The whole Board is a list of list.  [ [col1], [col2], [col3] ]
    The function makeEachBoxFalse() returns a list of all false boxes
    '''
    # Main board variable
    # change its name to initialise....
    mainBoard, winner_records = initialise_new_game(False)
    # Initially used boxes
    # usedBoxes = makeEachBoxFalse(False)

    # Paint the surface black
    DISPLAYSURFACE.fill(appBgColor)

    # Draw all the required lines
    drawLines()

    # The GRAND game loop

    # Player turn : bool variable
    game_turn = 'player'
    expected_row = None
    expected_column = None

    game_done = False

    while True:

        # set mouseClick as False
        mouseClicked = False

        # did the player move
        moved = False
        mousex, mousey = None, None
        row, column, box_row, box_column = (None, None, None, None)

        # Check for events for event queue
        for event in pygame.event.get():

            # For Game exiting
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # For resya
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    main(config.level, config.mode)
                    print("pressed: CTRL + A")

            # If mouse is moving, update the location
            # elif event.type == MOUSEMOTION:
            #     mousex, mousey = event.pos

            # If mouse button just came up, it means the button is clicked
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

            if game_done is True:
                # not required because user can also win sometimes
                # warGameEnding(smallFont, COMPUTERVOICE)
                # pygame.time.wait(500)
                # sys.exit()
                mouseClicked = False

        '''
        @:purpose : when mouse is clicked, we need to put X or O at the correct box
        So to obtain the exact box where the mouse is clicked, this function is used.
        @:returns: The box coordinates, where mouse is clicked
        '''
        if mousex is not None and mousey is not None:
            row, column, box_row, box_column = getBoxAtPixel(mousex, mousey)

        # correct here, perfect
        # print(row, column, box_row, box_column)

        # Firstmost turn

        # This code just highlights
        # actual law enforcement must be done

        # insert AI move here
        if game_done == False and mode == "AI" and game_turn == "computer":
            pygame.time.wait(500)
            row, column, box_row, box_column = computerTurnWithAI(mainBoard,
                                                                  winner_records,
                                                                  expected_row,
                                                                  expected_column)
            mouseClicked = True

        # mouse is clicked + not first time
        if mouseClicked and expected_column is not None and expected_row is not None \
                and row is not None and column is not None:

            if expected_row == 'any' and expected_column == 'any':
                if winner_records[row][column][0]['winner'] is not None:
                    row = None
                    column = None

            # + row does not match expected
            elif row != expected_row or column != expected_column:
                row = None
                column = None
                pygame.display.update()
                highlight(mainBoard, expected_row,
                          expected_column, safeBoxColor)

                # print(row, column)

        # If Inside the board, move forward, else ignore
        if row is not None and column is not None and box_row is not None and box_column is not None:

            if mainBoard[row][column][box_row][box_column] is False and mouseClicked:

                MARK, BEEP = None, None

                if game_turn == 'player':
                    MARK = XMARK
                    BEEP = BEEP1
                    game_turn = 'computer'

                elif game_turn == 'computer':
                    MARK = OMARK
                    BEEP = BEEP2
                    game_turn = 'player'

                markBox(row, column, box_row, box_column, mainFont, MARK)
                mainBoard[row][column][box_row][box_column] = MARK
                moved = True
                pygame.display.update()
                BEEP.play()
                # Player turn done

                expected_row = box_row
                expected_column = box_column

                # remove green color
                # dehighlight(mainBoard, row, column)
                # In case of any, i gotta dehighlight everything..... focus
                for i in range(3):
                    for j in range(3):
                        dehighlight(mainBoard, i, j)

                pygame.display.update()

                if moved is True:

                    if winner_records[row][column][0]['winner'] is None:
                        winner, b1, b2, b3 = smallGameWon(
                            mainBoard, row, column)
                    else:
                        winner = winner_records[row][column][0]['winner']
                        b1 = winner_records[row][column][0]['winner_tuple'][0]
                        b2 = winner_records[row][column][0]['winner_tuple'][1]
                        b3 = winner_records[row][column][0]['winner_tuple'][2]

                    # If player won, highlight the boxes, play sound, reset board for next turn
                    # print(winner, row, column, b1, b2, b3)
                    # Returned when no more space left
                    if winner is 'tie':
                        tieScore += 1
                        winner_records[row][column][0]['winner'] = 'tie'
                        winner_records[row][column][0]['winner_tuple'] = (
                            b1, b2, b3)
                        # in case of tie, b1 is none >>> handle later

                    elif winner is 'player':
                        playerScore += 1
                        pygame.time.wait(500)
                        highlightWin(mainBoard, row, column, b1, b2, b3)
                        BEEP3.play()
                        winner_records[row][column][0]['winner'] = XMARK
                        winner_records[row][column][0]['winner_tuple'] = (
                            b1, b2, b3)
                        # print(winner_records[row][column][0]['winner_tuple'])
                        pygame.display.update()

                    elif winner is 'computer':
                        computerScore += 1
                        pygame.time.wait(500)
                        highlightWin(mainBoard, row, column, b1, b2, b3)
                        BEEP3.play()
                        winner_records[row][column][0]['winner'] = OMARK
                        winner_records[row][column][0]['winner_tuple'] = (
                            b1, b2, b3)
                        # print(winner_records[row][column][0]['winner_tuple'])
                        pygame.display.update()

                        # No reset required in our case.
                        # mainBoard, playerTurnDone, playerWins, computerWins = boardReset(mainBoard, playerTurnDone, playerWins, computerWins)
                        # DISPLAYSURFACE.fill(appBgColor)
                        # drawLines()

                pygame.display.update()
                # highlight(mainBoard, expected_row, expected_column, safeBoxColor)

                if winner_records[expected_row][expected_column][0]['winner'] is not None:
                    expected_row = 'any'
                    expected_column = 'any'

                if expected_row == 'any' and expected_column == 'any':
                    # highlight all valid boxes
                    for i in range(3):
                        for j in range(3):
                            if winner_records[i][j][0]['winner'] is None:
                                highlight(mainBoard, i, j, safeBoxColor)
                                # else:
                                #     dehighlight(mainBoard, i, j)

                else:
                    # just green color
                    highlight(mainBoard, expected_row,
                              expected_column, safeBoxColor)

                pygame.time.wait(500)
                # pygame.display.update()

        drawScoreBoard(smallFont, playerScore, computerScore, tieScore)

        # Render the updated graphics on screen
        pygame.display.update()

        # start here for MAJOR Line

        if level == "easy":
            mega_winner = checkMegaWinEasy(mainBoard, winner_records)

            if mega_winner is not None:
                game_done = True
                drawWinner(smallFont, mega_winner)
                if mega_winner == 'tie':
                    # fill bg black and etc display
                    # tie display on screen
                    game_done = True

                else:
                    for row in range(3):
                        for col in range(3):
                            if winner_records[row][col][0]['winner'] == mega_winner:
                                highlight(mainBoard, row, col, RED)
                            else:
                                dehighlight(mainBoard, row, col)

        elif level == "smart":
            mega_winner, mb1, mb2, mb3 = checkMegaWinHeadOn(
                mainBoard, winner_records)

            if mega_winner is not None:
                game_done = True
                drawWinner(smallFont, mega_winner)
                if mega_winner == 'tie':
                    # fill bg black and etc display
                    # tie display on screen
                    game_done = True
                    # pass
                else:
                    highlightMegaWin(mainBoard, mega_winner, mb1, mb2, mb3)
                    game_done = True

        # Render the updated graphics on screen
        pygame.display.update()

        # Tick the CLOCK
        FPSCLOCK.tick(FPS)


###### Functions to set up the board  #########

"""
:objective: highlight the mega win
"""


def highlightMegaWin(mainBoard, mega_winner, mb1, mb2, mb3):
    """

    :param mainBoard:
    :param mega_winner:
    :param mb1:
    :param mb2:
    :param mb3:
    :return:
    """
    for row in range(3):
        for col in range(3):
            dehighlight(mainBoard, row, col)

    highlight(mainBoard, mb1[0], mb1[1], RED)
    highlight(mainBoard, mb2[0], mb2[1], RED)
    highlight(mainBoard, mb3[0], mb3[1], RED)


def checkMegaWinEasy(mainBoard, winner_records):
    """

    :param mainBoard:
    :param winner_records:
    :return:
    """
    mega_winner = None
    player, computer, tie = 0, 0, 0

    for row in range(3):
        for col in range(3):
            boxStatus = winner_records[row][col][0]['winner']

            if boxStatus is None:
                return mega_winner

            if boxStatus == XMARK:
                player += 1
            elif boxStatus == OMARK:
                computer += 1
            elif boxStatus == 'tie':
                tie += 1

    if player == computer:
        mega_winner = 'tie'
    elif player > computer:
        mega_winner = XMARK
    elif computer > player:
        mega_winner = OMARK

    return mega_winner


"""
@objective : returns true if game cannot continue
"""


def checkMegaWinHeadOn(mainBoard, winner_records):
    """

    :param mainBoard:
    :param winner_records:
    :return:
    """
    mega_winner, mb1, mb2, mb3 = None, None, None, None

    possible_cases = [
        # rows
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

        # columns
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

        # diagnoals
        ((0, 0), (1, 1), (2, 2)),
        ((0, 2), (1, 1), (2, 0))

    ]

    for ((i1, j1), (i2, j2), (i3, j3)) in possible_cases:

        if XMARK == winner_records[i1][j1][0]['winner'] \
                == winner_records[i2][j2][0]['winner'] \
                == winner_records[i3][j3][0]['winner']:
            mega_winner = XMARK
            mb1 = (i1, j1)
            mb2 = (i2, j2)
            mb3 = (i3, j3)
            break

        elif OMARK == winner_records[i1][j1][0]['winner'] \
                == winner_records[i2][j2][0]['winner'] \
                == winner_records[i3][j3][0]['winner']:
            mega_winner = OMARK
            mb1 = (i1, j1)
            mb2 = (i2, j2)
            mb3 = (i3, j3)
            break

    return mega_winner, mb1, mb2, mb3


'''
@objective : draw the lines that appear in the main board
@usage     : This function will be used to draw 9 lines
'''


# experimental
# Does not interfere with new data structure
def drawLines():
    '''
    Works fine. But we need more sophisticated graphics.
    :return:
    '''
    BIGBOXSIZE = (BOXSIZE + GAPSIZE) * BOARDWIDTH
    BIGBOARDSIZE = BOARDSIZE // 3
    left = XMARGIN
    top = YMARGIN

    ########HORIZONTAL LINES ##########
    # Length of horizontal line
    width = (BOXSIZE + GAPSIZE) * BOARDWIDTH
    # height of line
    height = GAPSIZE

    # DRAW 3 lines of BIG BOARD
    for line_no in range(3, BOARDSIZE, 3):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(
            left, top + line_no * (BOXSIZE + GAPSIZE), width, height)
        pygame.draw.rect(DISPLAYSURFACE, safeBoxColor, horizRect1, 5)

    # DRAW 8 lines
    # for boundaries - change to range(0, BOARDSIZE+1)
    for line_no in range(0, BOARDSIZE + 1):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(
            left, top + line_no * (BOXSIZE + GAPSIZE), width, height)
        pygame.draw.rect(DISPLAYSURFACE, WHITE, horizRect1)

    #######VERTICAL LINES########

    # swap because, they both are opposite for horizontal and vertical lines
    width, height = height, width

    # DRAW 3 lines of BIG BOARD
    for line_no in range(3, BOARDSIZE, 3):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(
            left + line_no * (BOXSIZE + GAPSIZE), top, width, height)
        pygame.draw.rect(DISPLAYSURFACE, safeBoxColor, horizRect1, 5)

    # DRAW 8 lines
    for line_no in range(0, BOARDSIZE + 1):
        #  horizontal rectangle needs to be drawn from top
        horizRect1 = pygame.Rect(
            left + line_no * (BOXSIZE + GAPSIZE), top, width, height)
        pygame.draw.rect(DISPLAYSURFACE, WHITE, horizRect1)


'''
@Objective : converts each box in the Board to FALSE
@Approach  : each each element of row, make all the boxes in its column FALSE
@Note : The Box is list of lists. 
For each Row one sublist, one sublist represents columns
'''


def initialise_new_game(val):
    """
    :param val:
    :return:
    """

    # convert it to looping structure
    board_structure = [
        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ],  # big row zero

        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ],  # big row one

        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ]  # big row two
    ]
    winner_records_structure = [
        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                },
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ],  # big row zero

        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ],  # big row one

        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ]  # big row two
    ]

    # convert it to looping structure

    # Test case ->
    """
    usedBoxes = [
        [
            [
                ['X', False, False],  # small box row 0
                [False, 'X', False],  # small box row 1
                [False, False, 'X']  # small box row 2
            ],  # small box 0

            [
                [False, False, 'O'],  # small box row 0
                [False, False, 'O'],  # small box row 1
                [False, False, 'O']  # small box row 2
            ],  # small box 1

            [
                ['O', False, False],  # small box row 0
                [False, 'O', False],  # small box row 1
                [False, False, 'O']  # small box row 2
            ]  # small box 2
        ],  # big row zero

        [
            [
                ['X', False, False],  # small box row 0
                [False, 'X', False],  # small box row 1
                [False, False, 'X']  # small box row 2
            ],  # small box 0

            [
                [False, False, 'O'],  # small box row 0
                [False, False, 'O'],  # small box row 1
                [False, False, 'O']  # small box row 2
            ],  # small box 1

            [
                ['O', False, False],  # small box row 0
                [False, 'O', False],  # small box row 1
                [False, False, 'O']  # small box row 2
            ]  # small box 2
        ],  # big row zero
        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 0
        ]  # big row zero
    ]
    winner_records = [
        [
            [
                {
                    'winner': 'X',
                    'winner_tuple': [[0, 0], [1, 1], [2, 2]]
                },
            ],  # small box 0

            [
                {
                    'winner': 'O',
                    'winner_tuple': [[0, 2], [1, 2], [2, 2]]

                }
            ],  # small box 1

            [
                {
                    'winner': 'O',
                    'winner_tuple': [[0, 0], [1, 1], [2, 2]]

                }
            ]  # small box 2
        ],  # big row zero
        [
            [
                {
                    'winner': 'X',
                    'winner_tuple': [[0, 0], [1, 1], [2, 2]]
                },
            ],  # small box 0

            [
                {
                    'winner': 'O',
                    'winner_tuple': [[0, 2], [1, 2], [2, 2]]

                }
            ],  # small box 1

            [
                {
                    'winner': 'O',
                    'winner_tuple': [[0, 0], [1, 1], [2, 2]]

                }
            ]  # small box 2
        ],  # big row zero
        [
            [
                {
                    'winner': None,
                    'winner_tuple': None
                },
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None
                },
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None
                },
            ]  # small box 0
        ]  # big row zero
    ]
    """

    usedBoxes = [
        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ],  # big row zero

        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ],  # big row one

        [
            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 0

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ],  # small box 1

            [
                [False, False, False],  # small box row 0
                [False, False, False],  # small box row 1
                [False, False, False]  # small box row 2
            ]  # small box 2
        ]  # big row two
    ]
    winner_records = [
        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                },
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ],  # big row zero

        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ],  # big row one

        [
            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 0

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ],  # small box 1

            [
                {
                    'winner': None,
                    'winner_tuple': None

                }
            ]  # small box 2
        ]  # big row two
    ]

    return usedBoxes, winner_records


def smallGameWon(mainBoard, row, column):
    '''

    :param mainBoard:
    :param row:
    :param column:
    :return:
    '''

    possible_cases = [
        # rows
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),

        # columns
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),

        # diagnoals
        ((0, 0), (1, 1), (2, 2)),
        ((0, 2), (1, 1), (2, 0))

    ]

    winner = 'tie'
    box1 = ()
    box2 = ()
    box3 = ()

    for ((i1, j1), (i2, j2), (i3, j3)) in possible_cases:
        if mainBoard[row][column][i1][j1] == mainBoard[row][column][i2][j2] == mainBoard[row][column][i3][j3]:

            if mainBoard[row][column][i1][j1] == XMARK:
                winner = 'player'
                box1 = (i1, j1)
                box2 = (i2, j2)
                box3 = (i3, j3)
                return winner, box1, box2, box3

            elif mainBoard[row][column][i1][j1] == OMARK:
                winner = 'computer'
                box1 = (i1, j1)
                box2 = (i2, j2)
                box3 = (i3, j3)
                return winner, box1, box2, box3

    # if atleast one space is left, no one is winner
    for i in range(0, 3):
        for j in range(0, 3):
            if mainBoard[row][column][i][j] is False:
                winner = None
                return winner, box1, box2, box3

    # else, tie
    return winner, box1, box2, box3


def dehighlight(mainBoard, row, column):
    '''
    De highlight stuff
    :param mainBoard:
    :param row:
    :param column:
    :return:
    '''
    # BOX decides top and left  and width and height
    top = YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)
    left = XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)

    width = 3 * (BOXSIZE + GAPSIZE)
    height = 3 * (BOXSIZE + GAPSIZE)

    horizRect1 = pygame.Rect(left, top, width, height)

    # highlight
    pygame.draw.rect(DISPLAYSURFACE, BLACK, horizRect1)
    # redraw lines
    drawLines()
    # redraw symbols
    redraw(mainBoard, row, column)
    # for now, come back after its safe
    if winner_records[row][column][0]['winner'] is not None and winner_records[row][column][0]['winner'] != 'tie':
        highlightWin(mainBoard, row, column,
                     winner_records[row][column][0]['winner_tuple'][0],
                     winner_records[row][column][0]['winner_tuple'][1],
                     winner_records[row][column][0]['winner_tuple'][2])


def highlight(mainBoard, row, column, color):
    '''

    :param color:
    :param mainBoard: the entire board, updates will happen here
    :param box_no: which box to highlight
    :return:
    '''
    # row = box_no // 3
    # column = box_no % 3

    # highlight_small_box = board[row][column]

    highlight_box_color = color

    # BOX decides top and left  and width and height
    top = YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)
    left = XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)

    width = 3 * (BOXSIZE + GAPSIZE)
    height = 3 * (BOXSIZE + GAPSIZE)

    # highlight_box_color = (140, 255, 26)
    horizRect1 = pygame.Rect(left, top, width, height)

    # highlight
    pygame.draw.rect(DISPLAYSURFACE, highlight_box_color, horizRect1, 0)

    # redraw lines
    drawLines()
    # redraw symbols
    redraw(mainBoard, row, column)
    # for now, come back after its safe
    if winner_records[row][column][0]['winner'] is not None:
        highlightWin(mainBoard, row, column,
                     winner_records[row][column][0]['winner_tuple'][0],
                     winner_records[row][column][0]['winner_tuple'][1],
                     winner_records[row][column][0]['winner_tuple'][2])


def redraw(board, row, column):
    '''
    AIM: To redraw lost symbols
    :param board:
    :param row:
    :param column:
    :return:
    '''
    mainFont = pygame.font.Font(resource_path(mainFontPath), MARKSIZE)
    for boxx in range(3):
        for boxy in range(3):
            mark = board[row][column][boxx][boxy]
            if mark is not False:
                markBox(row, column, boxx, boxy, mainFont, mark)
                # done


def drawWinner(smallFont, mega_winner):
    """

    :param mega_winner:
    :return:
    """
    message = ""
    if mega_winner == 'tie':
        message = smallFont.render(
            'The Game resulted in a TIE', True, COMBLUE, appBgColor)

    elif mega_winner == XMARK:
        message = smallFont.render(
            'Winner is Player 1 ( X )', True, COMBLUE, appBgColor)

    elif mega_winner == OMARK:
        message = smallFont.render(
            'Winner is Player 2 ( O )', True, COMBLUE, appBgColor)

    messageRect = message.get_rect()

    messageRect.x = BOXSIZE * 5 - 10 + BOXSIZE
    messageRect.y = BOXSIZE - 5 + BOXSIZE + 15
    DISPLAYSURFACE.blit(message, messageRect)


def drawScoreBoard(smallFont, playerScore, computerScore, tieScore):
    """

    :param smallFont:
    :param playerScore:
    :param computerScore:
    :param tieScore:
    :return:
    """

    scoreBoardMessage = 'Player 1 ( X ) : ' + str(playerScore) + '        ' + \
                        'Player 2 ( O ) : ' + str(computerScore) + '        ' + \
                        'Tie : ' + str(tieScore) + ''
    scoreBoard = smallFont.render(scoreBoardMessage, True, COMBLUE, appBgColor)

    scoreBoardRect = scoreBoard.get_rect()
    scoreBoardRect.x = BOXSIZE * 2 + 15
    scoreBoardRect.y = BOXSIZE - 5
    DISPLAYSURFACE.blit(scoreBoard, scoreBoardRect)


##### Coordinate Functions #####

'''
@function name : getBoxAtPixel
@purpose : Return the box where pixel(x,y) lie
@approach : Iterate over each possible SMALL BOX, derive its top left coordinates
'''


def getBoxAtPixel(x, y):
    """

    :param x:
    :param y:
    :return:
    """

    if x is None or y is None:
        return (None, None, None, None)

    for row in range(BIGBOXSIZE):
        for column in range(BIGBOXSIZE):
            for box_row in range(BIGBOXSIZE):
                for box_column in range(BIGBOXSIZE):

                    # left, top = leftTopCoordsOfBox(row, column, box_row, box_column)

                    # Reach BIG BOX + reach specific box inside it
                    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + \
                        (box_row * (BOXSIZE + GAPSIZE))
                    left = (XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)
                            ) + (box_column * (BOXSIZE + GAPSIZE))

                    boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
                    if boxRect.collidepoint(x, y):
                        return (row, column, box_row, box_column)

    return (None, None, None, None)


'''
@:function : centerxAndCenteryOfBox
@:returns : center coordinates of a Small BOX
@:approach : find the top left, then add half the box from both sides
Minor note : a little extra on y side, because i want the X/O a lil down
'''


def centerxAndCenteryOfBox(boxx, boxy):
    centerx = boxx * (BOXSIZE + GAPSIZE) + XMARGIN + (BOXSIZE / 2)
    centery = boxy * (BOXSIZE + GAPSIZE) + YMARGIN + (BOXSIZE / 2) + 5
    return centerx, centery


##### Functions dealing with computer and player moves ######

'''
Functions to mark X and O in the main board
approach : 
1. render the mark surface from X
2. Obtain its rectangle 
3. relocate the rectangle to correct small box
4. BLIT the original mark over this relocated rectangle
'''


def markBox(row, column, box_row, box_column, mainFont, MARK):
    '''
    This creates a new Surface with the specified text rendered on it. 
    pygame provides no way to directly draw text on an existing Surface:
    instead you must use Font.render() to create an image (Surface) of the text, 
    then blit this image onto another Surface.
    '''
    # Use Main Font to - render Xmark on a new surface
    mark = mainFont.render(MARK, True, WHITE)
    '''
    Surfaces don't have a position, so you have to store the blit position in the rect. 
    When you call the get_rect method of a pygame.Surface, Pygame creates a new rect
    with the size of the surface with coordinates (x,y)=(0,0). 
    '''
    # Obtain the rectangle object of surface.
    markRect = mark.get_rect()

    # find center of small box
    # Reach BIG BOX + reach specific box inside it
    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + \
        (box_row * (BOXSIZE + GAPSIZE))
    left = (XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)) + \
        (box_column * (BOXSIZE + GAPSIZE))

    # then go to center of box
    centerx = left + (BOXSIZE + GAPSIZE) // 2
    centery = top + (BOXSIZE + GAPSIZE) // 2

    # centerx, centery = centerxAndCenteryOfBox(boxx, boxy)

    # update the center = to center of the current box, so that TEXT appears inside box
    # Interesting Note : pygame re calculates the top and left automatically, when i change the center
    markRect.centerx = centerx
    markRect.centery = centery

    # BLIT(source,destination)
    DISPLAYSURFACE.blit(mark, markRect)


'''
@:Function : computerTurnWithAI
@: Objective : The smart AI
@: approach : 
1. check if AI can win with this move
2. check if Player can win with his next move, block that move
- IF BOTH SAFE, PROCEED -
3. Occupy center
4. Check if there is a fork ( a probable path leading to 2 winning situations )
5. occupy corners
6. occupy sides

'''


def computerTurnWithAI(mainBoard, winner_records, expected_row, expected_column):
    '''

    :param usedBoxes: a list of currently used boxes
    :param mainBoard: The main board
    :return: the AI move
    :approach: For each un-used box, play the AI move(O), and see if we can win

    Challenge :
    When expected is "any"
    I can work on only one of them, how to find the move with highest priority in them ?
    Doable ??? Yess
    '''
    # return 2,2,1,1
    # pass

    possibleBoxes = []

    # Find possible boxes list
    if expected_row == "any" and expected_column == "any":
        for row in range(BIGBOXSIZE):
            for column in range(BIGBOXSIZE):
                if winner_records[row][column][0]['winner'] == None:
                    possibleBoxes.append([row, column])
    else:
        possibleBoxes.append([expected_row, expected_column])

    if not possibleBoxes:
        return None, None, None, None

    # Shuffle it up
    random.shuffle(possibleBoxes)

    # For each item in the list, perform the 6 step process

    # Step 1 : Win : Can AI win with this move?
    for [row, column] in possibleBoxes:
        for box_row in range(BIGBOXSIZE):
            for box_column in range(BIGBOXSIZE):
                dummyBoard = copy.deepcopy(mainBoard)
                if dummyBoard[row][column][box_row][box_column] is False:
                    dummyBoard[row][column][box_row][box_column] = OMARK
                    winner, b1, b2, b3 = smallGameWon(dummyBoard, row, column)
                    if winner == 'computer':
                        return row, column, box_row, box_column

    # Step 2 : Block : Block opponent's win
    for [row, column] in possibleBoxes:
        for box_row in range(BIGBOXSIZE):
            for box_column in range(BIGBOXSIZE):
                dummyBoard = copy.deepcopy(mainBoard)
                if dummyBoard[row][column][box_row][box_column] is False:
                    dummyBoard[row][column][box_row][box_column] = XMARK
                    winner, b1, b2, b3 = smallGameWon(dummyBoard, row, column)
                    if winner == 'player':
                        return row, column, box_row, box_column

    possibleMoves = [

        ################### 1 Distance fork #############

        # Top Left combination
        [(1, 0), (0, 1), (0, 0)],

        # Bottom Left combination
        [(1, 0), (2, 1), (2, 0)],

        # Top Right combination
        [(0, 1), (1, 2), (0, 2)],

        # Bottom Right combination
        [(2, 1), (1, 2), (2, 2)],

        ################### 2 Distance fork #############

        # Opposite corners : pair 1 (top left, bottom right)
        [(0, 0), (1, 2), (0, 1)],
        [(0, 0), (2, 1), (1, 0)],

        [(2, 2), (0, 1), (1, 2)],
        [(2, 2), (1, 0), (2, 1)],

        [(0, 0), (2, 2), (1, 2)],

        # Opposite corners : pair 2 (top right, bottom left)
        [(0, 2), (1, 0), (0, 1)],
        [(0, 2), (2, 1), (1, 2)],

        [(2, 0), (0, 1), (1, 0)],
        [(2, 0), (1, 2), (2, 1)],

        [(0, 2), (2, 0), (1, 2)],

    ]

    # Step 3a : Create Forks
    for [row, column] in possibleBoxes:
        for [(i1, j1), (i2, j2), (i3, j3)] in possibleMoves:
            if mainBoard[row][column][i1][j1] is OMARK and mainBoard[row][column][i2][j2] is OMARK:
                if mainBoard[row][column][i3][j3] is False:
                    return row, column, i3, j3

    # Step 3b : Block Forks
    for [row, column] in possibleBoxes:
        for [(i1, j1), (i2, j2), (i3, j3)] in possibleMoves:
            if mainBoard[row][column][i1][j1] is XMARK and mainBoard[row][column][i2][j2] is XMARK:
                if mainBoard[row][column][i3][j3] is False:
                    return row, column, i3, j3

    # Step 4 : Occupy center block if possible
    possibleMoves = [[1, 1]]
    for [row, column] in possibleBoxes:
        for [box_row, box_column] in possibleMoves:
            if mainBoard[row][column][box_row][box_column] is False:
                return row, column, box_row, box_column

    # Step 5a : Occupy opposite corners
    possibleMoves = [
        [(0, 0), (2, 2)],
        [(2, 2), (0, 0)],
        [(0, 2), (2, 0)],
        [(2, 0), (0, 2)]
    ]

    for [row, column] in possibleBoxes:
        for [(i1, j1), (i2, j2)] in possibleMoves:
            if mainBoard[row][column][i1][j1] is XMARK:
                if mainBoard[row][column][i2][j2] is False:
                    return row, column, i2, j2

    # Step 5b : Occupy other corners
    possibleMoves = [[0, 0], [0, 2], [2, 0], [2, 2]]
    for [row, column] in possibleBoxes:
        for [box_row, box_column] in possibleMoves:
            if mainBoard[row][column][box_row][box_column] is False:
                return row, column, box_row, box_column

    # Step 6 : Occupy Sides
    possibleMoves = [[0, 1], [1, 0], [1, 2], [2, 1]]
    for [row, column] in possibleBoxes:
        for [box_row, box_column] in possibleMoves:
            if mainBoard[row][column][box_row][box_column] is False:
                return row, column, box_row, box_column


##### Functions dealing with an end of game ########


'''
@:Function : gameOver
@:purpose: checks is the game is over - no space left to move
@:approach : If any one the boxes from used boxes is false, it means its not has been used.
Means, Board has still space left, return false to game over

If no space left, it is a game over
'''


def gameOver(mainBoard):
    for row in range(BIGBOXSIZE):
        for column in range(BIGBOXSIZE):
            for box_row in range(BIGBOXSIZE):
                for box_column in range(BIGBOXSIZE):
                    if mainBoard[row][column][box_row][box_column] is False:
                        return False

    return True


'''
Resets the game
'''


def boardReset(mainBoard, playerTurnDone, playerWins, computerWins):
    pygame.time.wait(1000)
    mainBoard, winner_records = initialise_new_game(False)
    playerTurnDone = False
    playerWins = computerWins = False


def highlightWin(mainBoard, row, column, b1, b2, b3):
    '''

    :param mainBoard: Highlights the winning situation
    :return:

    #Note: Can be highly optimised if i pass around the winning boxes
    '''

    # The three boxes needed are b1,b2,b3

    # startPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + (BOXSIZE / 2))
    # endPos = (XMARGIN + (BOXSIZE / 2), YMARGIN + BOXSIZE + GAPSIZE + BOXSIZE + GAPSIZE + (BOXSIZE / 2))

    # find center of small box
    # calculate start postion of line

    box_row = b1[0]
    box_column = b1[1]
    # Reach BIG BOX + reach specific box inside it + middle of it
    left = (XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)) + \
           (box_column * (BOXSIZE + GAPSIZE)) + \
           ((BOXSIZE) // 2)

    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + \
          (box_row * (BOXSIZE + GAPSIZE)) + \
          ((BOXSIZE) // 2)

    startPos = (left, top)

    box_row = b3[0]
    box_column = b3[1]
    # Reach BIG BOX + reach specific box inside it + middle of it
    left = (XMARGIN + (3 * column) * (BOXSIZE + GAPSIZE)) + \
           (box_column * (BOXSIZE + GAPSIZE)) + \
           ((BOXSIZE) // 2)
    top = (YMARGIN + (3 * row) * (BOXSIZE + GAPSIZE)) + \
        (box_row * (BOXSIZE + GAPSIZE)) + ((BOXSIZE) // 2)

    endPos = (left, top)

    # print(startPos)
    # print(endPos)
    pygame.draw.line(DISPLAYSURFACE, winLineColor, startPos, endPos, 5)

    # return startPos, endPos

    # In the small box mainBoard[row][column], boxes b1, b2, b3 needs to be highlighted


def warGameEnding(smallFont, COMPUTERVOICE):
    COMPUTERVOICE.play()
    surfRect = DISPLAYSURFACE.get_rect()
    DISPLAYSURFACE.fill(appBgColor)

    # Render text
    computerMessage1 = smallFont.render(
        'A strange game...', True, COMBLUE, appBgColor)
    # Shift its rectangle to the position where you want the text
    computerMessage1Rect = computerMessage1.get_rect()
    computerMessage1Rect.x = XMARGIN / 3
    computerMessage1Rect.y = YMARGIN * 2

    # uncover the words - draw computerMessage1 inside rectangle computerMessage1Rect
    uncoverWords(computerMessage1, computerMessage1Rect)
    pygame.time.wait(1000)

    computerMessage2 = smallFont.render(
        'The only winning move is not to play.', True, COMBLUE, appBgColor)
    computerMessage2Rect = computerMessage2.get_rect()
    computerMessage2Rect.x = XMARGIN / 3
    computerMessage2Rect.centery = (YMARGIN * 2) + 50

    uncoverWords(computerMessage2, computerMessage2Rect)
    pygame.time.wait(3000)


def uncoverWords(text, textRect):
    # Copy the rectangle
    textRectCopy = copy.deepcopy(textRect)

    # Un necessary -- made copy because changes made while reveal speed
    blackRect = textRectCopy

    # Text is as wide as rectangle width ( of a rectangle which was originally derived from this text only )
    textLength = textRect.width

    # Revealing speed for text
    revealSpeed = 1

    # steps required to reveal whole text
    for i in range((textLength // revealSpeed) + 1):
        # draw text
        DISPLAYSURFACE.blit(text, textRect)
        # Draw a black rectangle over text
        pygame.draw.rect(DISPLAYSURFACE, appBgColor, blackRect)
        pygame.display.update()
        # Move the black triangle slowly away
        blackRect.x += revealSpeed
        blackRect.width -= revealSpeed


if __name__ == '__main__':
    main(config.level, config.mode)
