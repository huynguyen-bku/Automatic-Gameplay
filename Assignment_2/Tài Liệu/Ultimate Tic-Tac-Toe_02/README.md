# Ultimate Tic Tac Toe

A pygame implementation of the ultimate tic tac toe.

[Ultimate Tic Tac Toe](https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe) or the extended tic tac toe is an extension of the standard 3x3 tic tac toe which is composed of nine tic-tac-toe boards arranged in a 3-by-3 grid.

## Playing the game

- For windows - Simply, download the game exe file from [github releases](https://github.com/jatin69/ultimate-tic-tac-toe/releases). The exe can be run independently in windows.
- For Linux systems - Checkout the [Dev section](https://github.com/jatin69/ultimate-tic-tac-toe/#dev) to see how to run the project.

## About the current implementation

By default the game plays in `smart level` and `single player mode` against computer. To change modes see the `src/config.py`

- In terms of game difficulty, two levels have been implemented.
  - **Easy Level**. The first player to win a maximum tiles.
  - **Smart Leve**. The first player to win 3 tiles in a row wins.
- In terms of number of players, there's two modes.
  - **Single player mode**. Here the user plays against the computer.
  - **Two player mode**. Here two users play against each other.

## Game Controls

- use `ESC` key to close the application
- use `ctrl + N` at any time to start a new game
- use mouse to play the game

## Rules of the ultimate tic tac toe

- Each small 3-by-3 tic-tac-toe board is referred to as a local board, and the larger 3-by-3 board is referred to as the global board.
- The game starts with X playing wherever they want in any of the 81 empty spots. This move 'sends' their opponent to its relative location. For example, if X played in the top right square of their local board, then O needs to play next in the local board at the top right of the global board. O can then play in any one of the nine available spots in that local board, each move sending X to a different local board.
- If a move is played so that it is to win a local board by the rules of normal tic-tac-toe, then the entire local board is marked as a victory for the player in the global board.
- Once a local board is won by a player or it is filled completely, no more moves may be played in that board. If a player is sent to such a board, then that player may play in any other board.
- Game play ends when either a player wins the global board or there are no legal moves remaining, in which case the game is a draw

## Dev

### Running the project

- Make sure you have python 3.6+
- Install pipenv and get familiar
- Clone/download this repo
- Run `pipenv shell` in project root, then `pipenv install`
- This will setup all the required dependencies in a virtual env in python
- go to `src` folder.
- see the `src/config.py`. change levels, modes as required
- Run `python tic_tac_toe.py`

### Packaging

- We'll use this wonderful pyinstaller wrapper app [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe). Follow the instructions and make this app working in your local machine
- once you get the app started
- browse location for script `tic_tac_toe.py` in src folder
- choose `single file` and `Window Based Mode`
- provide a `ico` file if you wish
- In additional files, add folder, and browse to the `assets` folder
- Add this folder and your entry path `tic_tac_toe.py`
- In advanced options, choose `output directory` and provide any location
- Then simply press convert
- This will create a single exe file which can be run independently
- Try and run and test the exe, if something went wrong, debug using FAQs from the app repo
- The initial release has been made and added to github releases.

### code development

- The code was written in 2017 and is messy
- Formatting was done using `pep8`
- Tasks were written down to further extend the project.
- Have a look at the [developer doc](./dev-doc.md) to know about tasks in detail.

## Game Loop

### Performing a single move

- We'll see what goes into a single move
- While TRUE :
  - user wants to quit if eascape key comes up or window is closed
  - if mouse is clicked (mouse button just came up)
    - set mouse pointer coordinates = current pixel locations
  - else
    - coordinates = None
  - if coordinate is not None
    - obtain the exact local board number (row, column, box_r, box_c ) at that pixel coordinate
  - if this local board has already been won OR already marked/tied
    - set current local board variable = None
  - if inside a valid local board ( exact box,coordinates is not None)
    - ready to make a move -> X or O ( either player or computer)
    - make X/O move, then make entry in Data Structure
    - sound Beep1/Beep2 as per move
- You have now performed one move

### Getting ready for next move

- set `expected row/Column` for next move based on the move that just happened
- As soon a move is done, we have to do some steps to be ready for next move.
- `De-highlight` all the boxes (1 in most move/ many in free move case aka "any case")
- check who won the current box with this move
- `if won/tie`
  - make entry in win records
  - put in winner tuples
  - also hold Winner
- `if someone won`
  - increment the winner player's score
  - `pygame.time.wait(500)` for a delay efect
  - then `highlightWin` by drawing a line over won tuples
  - also play the `BEEP3`
- if `expected row/Column` is already won (Recheck global records)
  - set expected = `"any"`
- Now `highlight` all the expected boxes (1 or "any")
- Board got changed because of this, Screen needs update, perform `pygame.display.update()`
- 3 major functions
  - `highlightWin` draws a gaint line in a local board
  - `highlight` glows up a local board
  - `dehighlight` takes away the glow of a local board box
- once highlighted or dehighlighted, all its members need to be redrawn as well- In our case, everything needs to be redrawn, because we keep updating highlighted boxes and stuff.
