# Skyscraper Solver

solution to:  
[7*7 Skyscraper: (kyu 1)](https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8, "7x7")  
[6*6 Skyscraper: (kyu 2)](https://www.codewars.com/kata/5679d5a3f2272011d700000d "6x6")  
[4*4 Skyscraper: (kyu 4)](https://www.codewars.com/kata/5671d975d81d6c1c87000022 "4x4")

### The Rules

The premise of the game is when touring in a city district like downtown New York that is neatly placed on a grid and
full of skyscrapers, looking at the city from different angles creates different views of it, as higher skyscrapers
cover lower ones behind them.

Consider the following row of skyscrapers, where each number indicates the number of stories of the building:

      1 3 2 4

Looking from the left, the building with three storeys is not visible, since the three storey building covers it from
this point of view. Hence, three buildings are visible. From the right, only the four storey building is visible as all
others are smaller. This information can be translated concisely into the following representation of visible buildings:

      (3) 1 3 2 4 (1)

A full 4 by 4 city grid could look like this, if every single row and column is a permutation of 1,2,3,4; i.e. there are
no same sized buildings in these respective directions:

      2 1 4 3
      3 4 1 2
      4 2 3 1
      1 3 2 4

Now consider, that partial information is available:

           1 2
       x x x x
       x x x x|2
     1|x x x x
       x x x x
           3

Given only this information, we can derive how the underlying city looks like. By convention, the clues above are read
clockwise, where no clue is marked by 0:

      0 0 1 2 0 2 0 0 0 3 0 0 0 1 0 0

The same concept carries over to the game sizes 6 by 6 and 7 by 7. There are however two things to consider when moving
to these game settings:

1) The larger the grid size, the more permutations per row / column are available to choose from, making it considerably
   more difficult to derive the board. Runtime and efficiency become increasingly important. Solutions that exceed
   codewars' 12000ms time limit on the test cases are dismissed.

2) The 7 by 7 case provides a single testcase, where by design, the clues are so sparse, that it leaves vast ambiguity,
   which can only be resolved by looking at the remaining possibilities (efficiently).

The aim of this implementation is to create a single solver that can solve all board sizes efficiently; in addition to
the original katas' individual requirements this solver is able to solve all board sizes in a single session and create
the board specific precomputations lazily. Furthermore, it is size independent; i.e. other board sizes are admissible.

### Solving Strategies

In contrast to most of the repository's solutions, this one takes a  
combinatorial approach, that in the first pillar seeks to efficiently weeds out the inapplicable combinations for the
rows and columns. The second pillar is solely aimed at the 7 by 7 ambiguous case which requires a new set of logic to
conquer it; Recursion and Stacks, or more concisely Backtracking. But before getting started with solving the problem,
some (lazy) preprocessing is required.

#### Preprocessing

When encountering a city block, all available information is contained in the line of clues. More specific, all the
information for a row or column is contained in the clues that are opposite of one another. The aim of parsing thus is
to get tuples of clues for each row ('rowclues') and for each column ('columnclues'). The above example reads as

      rowclues = [(0,0), (0,0), (1,3), (2,0)]
      columnclues = [(0,0), (0,2), (1,0), (0,0)]

When solving multiple problems of the same size, it becomes apparent that the analysis on the set of the buildings
permutations' visibility is required in every step to come up with viable candidates. To drastically ease the burden of
computation, all permutations are (lazily) precomputed once. Each of these permutations is analysed for their visibility
from the left using a deque object, that is left appended whenever a building is found that is larger than the currently
highest building. In turn the currently highest building is replaced for comparison. The length of the deque object now
is the number of visible buildings from the left. The same analysis can be made on the permutation's reverse, giving the
visibility from the right. With all these in place, the permutations can be sorted into a dictionary by their
(front, back) visibility ({(front, back) : list of combinations}). Considering that the clues are incomplete and parts
of the key are unknown, we can build supersets of the dictionaries values based on partial visibility:
(front, 0) and (0, back). As there are rows with no clue whatsoever all unique permutations are added as key (0,0). This
dictionary now holds all possible clue combinations, that can easily be queried and follow the format provided by the
parsed clues. By convention, this dictionary is refered to 'pclues' (permutation clues).

#### 1) Solving Unambigious

At the very heart of this solving strategy lie row- & columnclues in combination with pclues. Each city grid is
determined by its set of clues. These admissible combinations for each clue can be easily looked up in pclues and are
named downtown_row and downtown_col respectively. These dictionaries are keyed by the row-/columnindex and at initiation
copy the list of permutations for the respective clue combination. The crux lies in combining multiple clues together to
dismiss combinations in the set of permutations of each downtown_row and downtown_col to arrive at a single viable
solution. A side note regarding the 'uninformative' (0,0) cases; on their own, they are indeed uninformative, but they
reflect multiple 'interactions' of clues across the board. Dismissing them altogether does not necessarily solve the
board.

#### 2) Solving **Ambigious**

only necessary for 7x7 stacking & reverting the stack

Solution method is purely to sample problems

### Refactoring Ideas:

* Potential for increase in efficiency: the (0,0)s contain no information on their own. However, as they reflect
  information from 'intersections' of clues, they can become informative lateron to solve residual ambiguity. With lots
  of information available and in an umabigious setting, keeping track of the zeros' permutations is not efficient.
  Maybe start of with updating only those clues that are either partially or fully informative. Keep track of what
  updates are made to downtown_row and column. Should there remain any ambiguity across the board, sequentially create
  the necessary! (0,0) permutations and update them in accord with the track record until the residual ambiguity is
  resolved.
  

* Potential for increase in efficiency: reduce the number of permutations by half; each permutation has a mirrored
  example. Knowing one and analysing it on its visibility automatically reveals the reverse's. pclues could be filled
  with them by reversing the clue tuple and the permutation!


* Efficiency increase: most (all except one problem) do not need the stack of changes make it togglable by the user - or
  by the algorithm as well (provided it failed in the first run). This will increase the speed on all other test cases.