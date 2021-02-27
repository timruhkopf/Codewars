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

just out of curiousity - and avoiding tedious indexing or iterations, getting an easily indexable & iterable block, and
column that always is only a view and not a copy. Block & Columns. basically emulates some of ndarray's view behaviour.
facilitates block related computation syntactically.

## Solving Strategy

Backtracking.