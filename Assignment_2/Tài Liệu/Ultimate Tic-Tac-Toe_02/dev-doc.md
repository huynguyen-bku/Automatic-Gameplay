# Dev Doc

- use `python -m pydoc -w tic_tac_toe` to generate documentation if required

## Versions

- [x] easy level - maximum score - just compare score and give answer - implementation done
- [x] smart level - winner if 3 in a row - game needs to be early over - Implementation done

## Task List

- [x] Rename to Ultimate Tic tac toe
- [x] Add a 3x3 [prototype](https://github.com/jatin69/ultimate-tic-tac-toe/tree/prototype)
- [x] Document the prototype
- [x] Refer books, gain more pygame knowledge
- [x] Define rules for new extended version
- [x] Define data structure
- [x] Start coding
- [x] Implement User
- [x] Graphics prototype
- [x] small box win
- [x] winning Line graphics
- [x] Big win implementation
- [ ] ~~Big win line~~ Big Win color
- [x] Tie Detection
- [x] difficulty - easy and smart
- [x] Handle Key Presses
  - Press `Esc` to quit the application
  - Press `ctrl + N` to restart the game
- [x] modify score card
  - Player 1 ( X )
  - Player 2 ( O )
  - Tie
  - Winner is Player 1 ( X )
  - Winner is Player 2 ( O )
  - Font change maybe
  - space out a little
- [x] Implement computer move
  - [x] random
  - [x] AI
- [x] Refactor 'O' to Omark & 'X' to Xmark at all places
- [ ] Setup Proper color scheme
- [ ] Make more screens
  - [ ] Welcome screen
  - [ ] Choose Single Player (against AI) or Two Player
  - [ ] single game ~~vs tournament (keeping track of multiple games)~~
  - [ ] win streak
  - [ ] Exit bye bye screeen
- [ ] Document code ( check out sphinx ) & clean up comments & Brush up code PEP8 style
- [ ] Document complete game loop
- [ ] Bundle up for release
- [ ] Upload to pygame store

## Bugs

- In scoreboard, with each win, `tie = 0` becomes `tie = 0))` . IDK why, gotta inspect

## Additional points

- ALso a possible data structure,, but will need to redefine my entire logic of finding coordinates,

```python
theBoard = {'top-L': 'O', 'top-M': 'O', 'top-R': 'O',
            'mid-L': 'X', 'mid-M': 'X', 'mid-R': ' ',
            'low-L': ' ', 'low-M': ' ', 'low-R': 'X'}
```
