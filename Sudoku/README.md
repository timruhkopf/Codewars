# Multi Sudoku

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

Experiment.option & Experiment.blockindex (caching)
Strategy works on a deepcopy of the problem

## (OPTIONAL) Finding all boards

Currently under construction. Finding all solutions to a board is trying all applicable options in the implied tree and
reverting early from a branch if a single error was made. To do this rather efficiently, the previously displayed
continuation protocol can be used relentlessly until all untried options are tested and removed from the tracking
mechanism.
