# Multi Sudoku

# README is in progress!

* Easy sudoku generally have over 32 givens
* Medium sudoku have around 30–32 givens
* Hard sudoku have around 28–30 givens
* Very Hard sudoku have less than 28 givens

Note: The minimum of givens required to create a unique (with no multiple solutions) sudoku game is 17.

### Requiries

* must provide the proper (single) solution
* must determine if board is unsolvable (raise)
* must be capable of determining if a board has multiple solutions (raise)
* must distinguish invalid boards (raise)

## Views:

Checking the rules of the game is continuously needed to determine viable positions and the remaining candidates, when
efficiently employing backtracking & recursion. On that behalf, rows and columns are easily accessible; however, blocks
are more difficult in this regard; tedious indexing at every step along the way is the consequence, when numpy arrays
are not employed. Out of curiousity & to avoid such index-cluttering and some unecessary computation & object
generation, I build my own BlockView object. This object allows easy blockwise subscription of the underlying board. The
Blockview class emulates some of Numpy's ndarray view capability but works on lists. In fact, each block is a composite
of three ListSliceViews, that each share the 'pointers' to the board's underlying rows. Making the ListSliceViews
iterable allows to flatten the block into a single list - which is convenient for further computation.

just out of curiosity - and avoiding tedious indexing or iterations, getting an easily indexable & iterable block, and
column that always is only a view and not a copy. Block & Columns. basically emulates some of ndarray's view behaviour.
facilitates block related computation syntactically and reduces computation.

## Solving Strategy

The very essence of this strategy is backtracking and recursion with smart tracking and a continuation protocol that
sequentially reverts the board and continues forward recursively on the previously untried options for a position, until
a second solution is found.

Experiment.option & Experiment.blockindex (caching) , creates Blockview of problem finds zeros across the board and
moves the to a deque object that guides the recursive path

at end of recursion all remaining options for each recursive level are written out to Experiment.remaining_options,
which are used in the second run for continuation.

second run starts from the solved board and moves in the exact reverse order - at each step setting the current location
to 0 and popping an option from the respective position's untried ('remaining') options. From this state, the first
strategy is employed and recursively run forward. If this run fails, i.e. no other solution was found, the algorithm
moves further back.

This strategy is guaranteed to never find the same solution twice, since this set of options is no longer contained in
the remaining options

## (OPTIONAL) Finding all boards

Currently under construction. Finding all solutions to a board is trying all applicable options in the implied tree and
reverting early from a branch if a single error was made. To do this rather efficiently, the previously displayed
continuation protocol can be used relentlessly until all untried options are tested and removed from the tracking
mechanism.

## REFACTORINGS:

* to find multiple or all solutions of the board simply execute the recursive path once, in the base case create a
  deepcopy and revert this move --> this will continue the recursion. No Tracking and continuation protocol required.

* Blockview is a replacement for explicit index operations. Simply write a lambda, that given a blockindex returns a
  generator object that iterates over the blocks entries. Remember that a block is fully determined by its '
  basecoordeinate' e.g (0,0), (0,3), (0,6),... and can be expanded from there. 