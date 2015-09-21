 # Daily Fantasy Sports (DFS) Optimization Tools

DFS sites like FanDuel and DraftKings require you to pick a team lineup with N number of players with postion restrictions under a max salary cap. A sample list of players might look like the below:

 | Name     | POS | Pts | Salary |
 |----------|-----|-----|--------|
 | Player A |  A  | 8.0 | $9,300 |
 | Player B |  A  | 3.4 | $3,500 |
 | Player C |  B  | 6.7 | $6,400 |
 | Player D |  B  | 1.7 | $2,000 |
 | Player E |  C  | 4.7 | $5,100 |
 | Player F |  C  | 6.7 | $6,400 |
 | Player G |  C  | 4.4 | $4,300 |

Max Salary: $20,000
Position Requirements: 1 x A, 1 x B, 1 x C

Our goal is to maximize the total points for the lineup, while meeting the constraints of remaining under the salary cap and filling all the team positions. For the above scenario an optimal algorithm would chose: Player A, C, and G. Yielding a team, which costs exactly $20,000 and has a projected point value of 19.1.

I aim to implement the below methods with Python and C, where efficiency and speed dictate.

***Disclaimer:*** *I am not responsible for any financial loss caused by the use of these utilities. Maximizing projected points for a lineup is not the only factor, which should be considered when constructing a fantasy team.*

## Methods
  * Random Generation
  * Knapsack Problem
  * Heuristic Approaches
      * Genetic Algorithm
      * Hill CLimbing
  * Integer Linear Programming

## Dependencies
- Python 2.7+ Standard Library

## Setup
##### Start fresh
```sh
$ git clone this repo
```
##### Usage
```sh
>>> import optimize, utils
>>>
>>> # Fetch Players from CSV file with headers
>>> players = utils.load_data('file-with-player-data.csv')
>>>
>>> # Prune down the search space for our algorithm
>>> players = filter(filter_function, players)
>>>
>>> # Group players by position to help out our optimizer
>>> players_by_pos = utils.groupby('position', players)
>>>
>>> # Use a random optimizer to generate teams, this is very slow
>>> teams = random_optimizer(players_by_pos, restrictions_mlb, 35000)
>>> best = teams[0]
>>> print best
Team(cost:$20,000  points:19.1)
```

## License
MIT
