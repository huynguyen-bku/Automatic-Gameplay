# AI Ultimate Tic Tac Toe!

Play against an AI bot or pit them against each other!

## About

This python program implements [Monte Carlo Tree Search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) to play [Ultimate Tic Tac Toe](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/) against other bots or humans.

## Running this application
*Requires Python 3 with scipy and numpy packages installed*

### Available bots/players
1. **random_bot** Selects completely random legal application
2. **rollout_bot** = Simulates x games for each possible next move and play the move with highest win percentage
3. **mcts_vanilla** = Uses Monte Carlo Tree Search to select the next best possible move
4. **mcts_modified** = Same as mcts_vanilla except with added hueristic of prioritizing selecting middle spaces
5. **human** = you or maybe a human opponent

### To play a single visualized game
1. Navigate to ```/AI-TICTACTOE/src``` folder in your terminal
2. Run **p3_play.py** and 2 bots/players by typing ``` python p3_play.py [bot1/player1] [bot2/player2]```
3. For example, if you want to play against the MCTS vanilla bot then type ``` python p3_play.py human mcts_vanilla```

### To simulate multiple games with bots
1. Navigate to ```/AI-TICTACTOE/src``` folder in your terminal
2. Run **p3_play.py** and 2 bots by typing ``` python p3_sim.py [bot1] [bot2]```
3. For example, if you want to play the random bot against the MCTS vanilla bot then type ``` python p3_sim.py random_bot mcts_vanilla```


## Parameters that can be changed
1. Number of simulations can be adjusted as ```num_nodes = x ``` where ```x > 0``` on line 7 of both ```mcts_vanilla.py``` and ```mcts_modified.py```
2. [Exploration Parameter](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search#Exploration_and_exploitation) can be adjusted as ```explore_faction = x``` where ```x = ~(1.4)``` on line 8 of both ```mcts_vanilla.py``` and ```mcts_modified.py```.
3. Number of simulations in ```p3_sim.py``` can be adjusted as ```rounds = x``` where ```x > 1``` on line 35 of ```p3_sim.py```.


## Testing results
![100 simulations vs x simulations](https://github.com/chipmunkboi/AI-TicTacToe/blob/master/background/Experiment_1_plot.png?raw=true)

#### Analysis
The attached Experiment_1_plot.png shows the plot of games
won by MCTS_vanilla at 10, 50, 100, 200, 400, 600, 800, and 1000
simulations per turn verses MCTS vanilla at a fixed 100 simulations per turn.
Since less simulations is closer to random_bot because there will be less reliable
data, it is assumed that any value below 100 will result in a overall loss. 
That was correct,as 10 and 50 only won between 10-26% of games. 
With both at 100 simulations per turn, the bot won 50 games, 
or 50% of 100 total games. As the bot continued upwards, we started 
seeing less and less improvement. At 600 simulations and more
the win ratio remained pretty steady at around 90% which means that
it is at the most optimal for computational time verses wins compared 
to MCTS_vanilla at 100 simulations per turn.
