# Skyscraper Solver

solution to:  
[7*7 Skyscraper: (kyu 1)](https://www.codewars.com/kata/5917a2205ffc30ec3a0000a8, "7x7")  
[6*6 Skyscraper: (kyu 2)](https://www.codewars.com/kata/5679d5a3f2272011d700000d "6x6")  
[4*4 Skyscraper: (kyu 4)](https://www.codewars.com/kata/5671d975d81d6c1c87000022 "4x4")

## The Rules

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

## Solving Strategies

In contrast to most of the repository's solutions, this one takes a  
combinatorial approach, that in the first pillar seeks to efficiently weeds out the inapplicable combinations for the
rows and columns. The second pillar is solely aimed at the 7 by 7 ambiguous case which requires a new set of logic to
conquer it; Recursion and Stacks, or more concisely Backtracking. But before getting started with solving the problem,
some (lazy) preprocessing is required.

### Preprocessing

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

### 1) Solving Unambigious

At the very heart of this solving strategy lie row- & columnclues in combination with pclues. Each city grid is
determined by its set of clues. These admissible combinations for each clue can be easily looked up in pclues and placed
into two dictionaries named downtown_row and downtown_col respectively. These dictionaries are keyed by the
row-/columnindex and at initiation copy the list of admissible permutations for the respective clue combination. The
crux lies in combining multiple clues together to dismiss combinations in the set of permutations of each downtown_row
and downtown_col to arrive at a single viable solution. A side note regarding the 'uninformative' (0,0) cases; on their
own, they are indeed uninformative, but they reflect multiple 'interactions' of clues across the board. Dismissing them
altogether does not necessarily solve the board.

The basic idea of this solving strategy is the following deterministic 'cross' update between downtown_row and
downtown_col. Consider starting with the third row (index 2) for illustrative purposes:

    {rowindex: list of all applicable 'candidate' tuples for that row}
    downtown_row = {0: [...],
                    ...
                    2:[(2, 3, 4, 1),
                       (1, 2, 4, 3),
                       (1, 3, 4, 2)], ...}

    The columnsets across all the applicable tuples for row 3 (index 2):
    columnsets = [{1, 2}, {2, 3}, {4}, {1, 2, 3}]

Each of these sets provides information regarding the applicable tuples for the admissible permutations in downtown_col.
For instance, knowing that at index position (2, 1) only those tuples are applicable, that contain either {2, 3} helps
reduce the number of applicable tuples for the column 1 that are contained in downtown_col[1]. We can now safely remove
all those tuples in downtown_col[1], that do not have two or three at the index position 1
(A WARNING on behalf of the columnsets. regarding them individually without considering the other sets of their row may
be treacherous; consider an update procedure that intersects these sets, that correspond to a particular index position
with the exact same set derived from downtown_col. Removing for instance 3 from the set at (2, 1) ({2,3})
would - given all applicable permutations in downtown_row[2] also imply that both 1 and 2 are not applicable at this
row's last position (2,3) i.e. {1,2,3} should actually reduce by {1, 2}, when 3 is removed from (2,1). An intersection
of a position's sets does not capture this information and thus is not state-safe):

    downtown_col before update:
    downtown_col = {0: ... ,
                    1: [(1, 4, 2, 3), 
                        (2, 4, 1, 3), 
                        (3, 2, 4, 1), 
                        (2, 1, 4, 3), 
                        (3, 1, 4, 2), 
                        (3, 4, 1, 2)], ...}

    downtown_col after update:
    downtown_col = {... ,
                    1: [(1, 4, 2, 3)], ...}
    
    columnsets for column 2 (index 1):
    columnsets = [{1}, {4}, {2}, {3}]

In the above example, the state of column two is now known. Building all the columnsets of this 2nd!
column: [{1}, {4}, {2}, {3}] in the exact same manner allows to update all the lists of applicable tuples for the
downtown_row: All applicable tuples for the first row must contain a 1 at the 2nd index position. All applicable tuples
for the second row must contain a 4 at the 2nd index position - and so on and so forth.

As the example may already have conveyed, the 'cross' updates work both ways. Cycling through them with switched updater
and updatee relentlessly and executing all updates implied by the columnsets at each step, until no change in
downtown_col & downtown_row occurs is a state-safe update and, provided sufficient information is available will yield a
definitive solution. At the end both *_row & *_col contain only single element lists as values and one of them can be
used for parsing the solved board from it.

### 2) Solving **Ambigious** (Medved Case)

The 7x7 kata deliberately provides a 'medved' testcase, that despite the abundance of clues leaves ambigiouity in the
originally vast searchspace, since the available information is not as informative as its abundance suggests initially
This is the medved case:

        clues = [3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]
        solution =  [[2, 1, 4, 7, 6, 5, 3],
                     [6, 4, 7, 3, 5, 1, 2],
                     [1, 2, 3, 6, 4, 7, 5],
                     [5, 7, 6, 2, 3, 4, 1],
                     [4, 3, 5, 1, 2, 6, 7],
                     [7, 6, 2, 5, 1, 3, 4],
                     [3, 5, 1, 4, 7, 2, 6]]

After employing the CrossSolving Strategy relentlessly, these are the applicable remaining *_row permutations
(rest assured, that *_col is even larger):

    {
    0: [(2, 1, 3, 7, 6, 5, 4), 
        (2, 3, 1, 7, 6, 5, 4), 
        (2, 1, 4, 7, 6, 5, 3),
        (1, 3, 2, 7, 6, 5, 4), 
        (2, 1, 5, 7, 6, 4, 3)],
    1: [(6, 4, 7, 5, 1, 2, 3), 
        (6, 4, 7, 3, 5, 1, 2),
        (6, 4, 7, 2, 5, 1, 3),
        (6, 4, 7, 1, 5, 2, 3), 
        (6, 4, 7, 5, 2, 1, 3)],
    2: [(1, 2, 4, 6, 3, 7, 5), 
        (1, 2, 3, 6, 4, 7, 5), 
        (2, 3, 4, 6, 1, 7, 5), 
        (1, 3, 4, 6, 2, 7, 5)],
    3: [(5, 7, 6, 1, 2, 4, 3),
        (5, 7, 6, 1, 3, 4, 2), 
        (5, 7, 6, 3, 2, 4, 1), 
        (5, 7, 6, 3, 4, 1, 2), 
        (5, 7, 6, 2, 3, 4, 1), 
        (5, 7, 6, 2, 1, 4, 3), 
        (5, 7, 6, 1, 4, 2, 3), 
        (5, 7, 6, 2, 4, 1, 3), 
        (5, 7, 6, 4, 2, 1, 3), 
        (5, 7, 6, 4, 1, 2, 3), 
        (5, 7, 6, 3, 1, 4, 2)],
    4: [(4, 1, 3, 2, 5, 6, 7),
        (4, 2, 5, 3, 1, 6, 7),
        (3, 2, 5, 1, 4, 6, 7),
        (4, 3, 5, 2, 1, 6, 7), 
        (3, 2, 5, 4, 1, 6, 7), 
        (4, 3, 5, 1, 2, 6, 7), 
        (4, 2, 3, 1, 5, 6, 7), 
        (4, 1, 5, 2, 3, 6, 7), 
        (4, 2, 3, 5, 1, 6, 7), 
        (4, 2, 5, 1, 3, 6, 7), 
        (4, 1, 5, 3, 2, 6, 7), 
        (3, 1, 5, 2, 4, 6, 7), 
        (4, 1, 3, 5, 2, 6, 7), 
        (3, 1, 5, 4, 2, 6, 7)],
    5: [(7, 6, 2, 5, 1, 3, 4), 
        (7, 6, 4, 2, 3, 5, 1), 
        (7, 6, 2, 4, 3, 5, 1), 
        (7, 6, 4, 1, 3, 5, 2), 
        (7, 6, 3, 4, 2, 5, 1), 
        (7, 6, 3, 1, 4, 5, 2), 
        (7, 6, 4, 2, 1, 5, 3), 
        (7, 6, 3, 1, 2, 5, 4), 
        (7, 6, 4, 3, 1, 5, 2), 
        (7, 6, 2, 1, 5, 3, 4), 
        (7, 6, 2, 3, 4, 5, 1), 
        (7, 6, 2, 3, 1, 5, 4), 
        (7, 6, 3, 2, 1, 5, 4), 
        (7, 6, 4, 1, 2, 5, 3), 
        (7, 6, 3, 4, 1, 5, 2),
        (7, 6, 4, 3, 2, 5, 1), 
        (7, 6, 2, 1, 4, 5, 3), 
        (7, 6, 2, 4, 1, 5, 3), 
        (7, 6, 2, 1, 3, 5, 4), 
        (7, 6, 3, 2, 4, 5, 1)],
    6: [(4, 5, 2, 3, 7, 1, 6),
        (4, 5, 1, 2, 7, 3, 6), 
        (4, 5, 1, 3, 7, 2, 6), 
        (3, 5, 1, 4, 7, 2, 6), 
        (4, 5, 2, 1, 7, 3, 6), 
        (3, 5, 2, 4, 7, 1, 6)]
    }

From the first look it becomes apparent that some positions are already sufficiently, that is definitively described.
However, the columnsets of the row's permutations still have remaining ambiguity. This is the result of the lack of
information contained in each of the clues. Most of the clues are fairly vague in the sense of implying a vast amount of
applicable permutations. However, it is certain that for each of these respective lists of permutations contain the true
solution for that row. The solution to this case lies in recursively and successively trying out each of the most
informative tuples (here *_row[2] is the least ambigious by number of admissibles) to create a definitive and
informative state in order to remedy some ambiguity. Choosing eg. (1, 2, 4, 6, 3, 7, 5) for row 2 causes an update of
downtown_col just as in the prior strategy. After such an update, we can move down in the recursion hierarchy and select
from the next smallest list of permutations. Should a choice produce an empty list of permutations in *_cols, the entire
update must be reverted and the next candidate of the higher recursion level must be checked for applicability.

# TODO FIX THIS ISSUE

There is however a catch; progressively choosing in this manner on *_row alone does not ensure that the columns of the
board will also be the unique set of range(1, 8).

# WRITE ABOUT EARLY STOPPING AND STACK

## Sampling Boards

Solution method is purely to sample problems

## Refactoring Ideas & Scaleing Efficiency:

Notice, that the current solver is very fast already, but scaling up to larger boards with a vast amount of permutations
may lead to performance issues. In the light of larger problems, there are some key levers that can be adjusted to
drastically increase speed for such problems:

* Potential for increase in efficiency: the (0,0)s contain no information on their own. However, as they reflect
  information from 'intersections' of clues, they can become informative lateron to solve residual ambiguity. With lots
  of information available and large boards in an umabigiuous setting, keeping track of the zeros' permutations is not
  efficient. Maybe start of with updating only those clues that are either partially or fully informative. Keep track of
  what updates are made to downtown_row and column. Should there remain any ambiguity across the board, sequentially
  create the necessary! (0,0) permutations and update them in accord with the track record until the residual ambiguity
  is resolved.


* Potential for increase in efficiency: reduce the number of permutations by half; each permutation has a mirrored
  example. Knowing one and analysing it on its visibility automatically reveals the reverse's. pclues could be filled
  with them by reversing the clue tuple and the permutation!


* Potential for increase in efficiency: StrategyCrossSolving.execute relentlessly cycles through downtown_row & column
  as switched updatee & updater. However, it always executes each of these dict's columnsets entirely (but sorted by the
  length of remaining permutations.) There are two ways that can, if properly implemented boost the efficiency, but are
  not 'sorting safe' and do not necessarily guarantee the shortest solution path:
    1) find the most informative (i.e. shortest) lists of permutations ACROSS! both downtown_row & *_col and execute
       them first (as opposed to the current dogma; execute all of downtown_row's updates first, before
       executing_downtown_col). Ensure however that in every cycle, all columnsets of both *_row & *_col are considered
       to ensure state-safety. The disadvantage is that once a single update is carried out, this ordering is corrupted
       and does not reflect the most informative & not yet touched *_row & *_col. Simply sorting anew does not resolve
       this, since it may cause some updaters to be used multiple or indefinetly times (as they are always shortest and
       already communicated their entire information). This strategy requires keeping track of which updater was already
       used - and sort by length at each step the remaining updaters. All of this can be mostly implemented by a new
       StrategyCrossSolving.execute method.
    2) rather than relentlessly execute, similar to 1), keeping track of visited updaters and do a priority sorting at
       each step, but rather than executing all updaters in a "relentless-step"
       recursively do those updates; base case would be that a single solution for a row / column was found in that case
       communicate this update and remove this solved *_row/*_col from all possible higher level recursion sorting
       inquiries. Do so util one of the dicts is empty. This strategy can be waaay more efficient, but is also more
       difficult to implement.


* Efficiency: with increasing board sizes, the number of potential permutations increases very fast:
  7x7 already has 5040 permutations in the uninformative case (0,0). Making columnsets or updating this lengthy list of
  permutations is extremely time consuming and for the most part only keeping track of the updates from other *_row & *_
  col[s]. This is true even after a few update steps, that make this set somewhat more informative. it will prove
  beneficial to large scale (and thereby uninformative) clues to merely catch the update information during the updates
  and create the set of applicables based on the information contained in those update steps such as e.g.
  [{1, 2}, {1,2,3,4,5}, {3,4}, ...] already implies a severely limited subset of all the permutations. Creating these
  sets when they are needed, that is, the information of all the other *_row & *_col is exploited, may prove far more
  efficient. With very large problems, such as 10x10 with 3628800 permutations in (0,0), the entire precomputation part
  becomes obsolete and on demand computation takes absolute precedence.


* EXPERIMENTAL. The selection procedure for 'medved' can be modified; for those ambigious positions check the count of
  the 'columnset' candidates - and start selecting from those that have a smaller count (as they are more informative ).
  choosing the *_row index with the smallest ambigouity in this sense might help in some cases. to determine index
  positions, that in turn can help fixing the board. Consider from above:

        0: [(2, 1, 3, 7, 6, 5, 4), 
            (2, 3, 1, 7, 6, 5, 4), 
            (2, 1, 4, 7, 6, 5, 3),
            (1, 3, 2, 7, 6, 5, 4), 
            (2, 1, 5, 7, 6, 4, 3)]

  the first index position is undecided between 1 and 2 (columnset = [{1,2}])
  trying out the combination with 1 and returning falsely makes the {2} at this position definitive and the update can
  be communicated using CrossSolving. But be aware that the update must be revertible when called from the recursion!

  The efficiency gains of this strategy are unclear though and problem dependent.

* Notice how a failure of StrategyStack implies an unsolvable board (i.e. a set of contradictory clues) this can be used
  to check if a clue is implying a correct board during sampling_board.

[comment]: <> (# TODO CHECK if stack is build encessarily in Strategy2.update at all!)

[comment]: <> (* Efficiency increase: most &#40;all except one problem&#41; do not need the stack of changes; make it togglable by the user or)

[comment]: <> (  by the algorithm  &#40;provided it failed in the first run&#41;. This will increase the speed on all other test cases.)