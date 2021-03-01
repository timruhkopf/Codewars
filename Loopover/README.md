# Loopover Puzzle Solver
### Soltuion to [kata][0]


Shifting behaviour:  
The board's shift method expects a literal consisting of a letter (L, R, D, U)
and an index number. The Letters L & R are shift directions for rows and D & U
are shift directions for columns (L:Left, R:Reight, D:Down, U:Up). 
The index number references the corresponding row / column. 
The subsequent illustrates this behaviour:

    A C D B E
    F G H I J
    K L M N O
    P Q R S T
    
    shift 'L0'

    C D B E A
    F G H I J
    K L M N O
    P Q R S T

Notice how 'R0' is the inverse operation.

    A C D B E
    F G H I J
    K L M N O
    P Q R S T

    shfit 'D3' 

    A C D S E
    F G H B J
    K L M I O
    P Q R N T

Notice how 'U3' is the inverse operation.

The goal of the game is to translate some arbitrary initial configuration into another, using only the allowed
instructions.

    initial configuration:

    P S H C O
    A L E D G
    J B N T R
    K M F Q I

    final configuration:

    A C D B E
    F G H I J
    K L M N O
    P Q R S T
    
    Notice, that the final config. is not a sorted one!

There are a few additions to this basic game:  
1) The board sizes are arbitrary (tested are up to 9x9) 
2) It has to work with arbitrary letters
3) The target configuration can be arbitrary
4) Among the tested configurations exist some unsolvables

## A playable Board

To ease debugging and allow for multiple modes of operation, the
**_Cyclic_shift_board_** class is conceived in a manner that indeed resembles the 
exact behaviour of the game. Emulating this behaviour allows to translate
any algorithm into code very easily and makes them read- and debuggable.
The implementation of the board can be found in
**_Nodes_**, **_Rows_**, **_Columns_** and **_Cyclic_shift_board_**.**_\_\_init\_\__**. 
There are two modes of operation, that differ only via their interface, namely

(1) **play-** or **debugmode**  
The board's instance can be **_.shift_**[ed] using the katas conventions.
This behaviour can be used to check if the **_solve_**'s solution produces the 
desired output.

(2) **solving**  
To produce a generic interface for the algorithms that can efficiently use 
multiple steps at once and avoid the clumsy and specific literal interface, the 
backend of the game; namely the **_Row_** and **_Column_**, **_shift_** with 
-1 and 1 for (L: -1, R: 1) and (D: -1, U: 1) respectively. Using these conventions
allows for readable Algorithms. 

## Nodes, Rows & Columns
At the very heart of the board's implementation are these three classes and the 
interplay of shared objects (**_Node_**), whose values are passed along using the 
**_collection_** object **_deque_**. On top of that, to track the location and ease the
lookup of a value's current position, **_Node_** carries a class attribute 
**_Node.current_**; a dictionary ( {value: position} ) that is updated at the 
end of a shift operation. This dictionary will come in very handy during  
solving. 

Shift implementation:  
**_Node_** consists of a value and a position attribute.

**_Row_** is an ordered collection of Nodes. In fact, **_Row_** is a **_list_** descendant, adding
a **_shift_** method, that makes use of **_deque_** objects. To track the shifts,
the Row can be made **_Context_** aware; that is, it is passed the reference to the containing
class. At the end of every shift, the method translates the operation (e.g. -1, 1, -5) 
into the appropriate Literal(s) and adds them to **_Context.solution_**. This 
simple shifting behaviour facilitates the entire algorithmic solution, as the 
algorithm need not keep track of what it is doing solution-wise.

**_Column_** is actually a subclass of **_Row_**, with the exact same behaviour. 
It is in place merely to make the convention of filling the column explicit: 
Bottom to Top values. The columns are filled with the exact same instances 
of **_Node_**[s] as **_Row_** is, but in a different ordering. 
This establishes the shared objects and the ability to shift easily.

## Solving Strategies

Before progressing to solve the board, the target configuration is translated 
to the same dictionary format as before ( {value:position} ) and placed 
into **_Node.target_**. This allows to easily obtain a value's target position.

Afterwards, up to three strategies are applied that have different focuses on the board. 
From an implementational point of view, the ['Strategy Design Pattern'][1]
is used for each of them. The board's solve method more or less merely delegates 
to these following Strategies. 

### (1) Liftshift

Task: sort from bottom to and including second row. e.g.
    
    initial configuration:

    C W M F J
    O R D B A
    N K G L Y
    P H S V E
    X T Q U I

    Liftshift's final configuration

    C A B D E
    F G H I J
    K L M N O
    P Q R S T
    U V W X Y

**_Liftshift_** consists of three small substrategies, that are dependent on the relative position of a value's current
to its target position (same row, same column or neither?) that leave the already solved in their place after execution.
For the details of these minor and comprehensible strategies, please consult the source code.

### (2) Toprow - A Graph Approach.

Task: sort the first row of the puzzle & determine if there is any viable solution at all.

This strategy is very verbose about the observations underlying it. The basic idea of this algorithm is the following:

#### (A) Determine the sorting graph:

To sort the following board

        A B D E C
        F G H I J
        K L M N O
        P Q R S T
        U V W X Y

from an intuitive stand point, the toprow can be solved using a graph

    D --> E, E --> C, C --> D 

which translates to D must move to E's current position, E must move to C's current position and C must move to D's
current position.

#### (B) Graph execution.

1) Initialisation (two steps:= number of up and down moves of first column)

        D -- > E
    
        A B D E C
        F G H I J
        K L M N O
        P Q R S T
        U V W X Y
        
        shift D (start) to the leftmost
    
        D E C A B
        F G H I J
        K L M N O
        P Q R S T
        U V W X Y
    
        shift D up
    
        F E C A B
        K G H I J
        P L M N O
        U Q R S T
        D V W X Y
    
        F is "wildcard", i.e. placeholder in the first row, that does not belong here
        shift E (the target) leftmost
    
        E C A B F
        K G H I J
        P L M N O
        U Q R S T
        D V W X Y
    
        shift E down. D is now at its correct relative position to A. Note how 
        the wildcard F is still in that row!
        
        D C A B F
        E G H I J
        K L M N O
        P Q R S T
        U V W X Y

2) Continuation (single step)

        E --> C: shift C leftmost
        C A B F D
        E G H I J
        K L M N O
        P Q R S T
        U V W X Y
        
        push column up

        E A B F D
        K G H I J
        P L M N O
        U Q R S T
        C V W X Y
        
        C --> D Be aware that the original's D position is where F now is!

        F D E A B
        K G H I J
        P L M N O
        U Q R S T
        C V W X Y

        C D E A B
        F G H I J
        K L M N O
        P Q R S T
        U V W X Y

        Notice how the wildcard F is pushed back into place.

now merely the toprow needs to shifted left 3 times and the board is solved.

#### Details.

Now that there is a basic intuition for the strategy, there are a few details, that are needed to get a full and
comprehensive idea of the strategy. Crucial to the success of the above example is that the number of sortings in the
graph is uneven. This way, with the initialisation stage requiring 2 steps, the total number of steps is again even and
the wildcard moves back in place at the end.

Step (A)'s graph from above is computed in **_find_sort_graphs_**. The latter takes the toprow and looks at all its
rotations and compares them (start) against the target row's position (target)

    rotations of [A, B, D, E, C] and their implied sorting graph
    to target row [A, B, C, D, E]

    ['A', 'B', 'D', 'E', 'C'] > {'C': 'D', 'D': 'E', 'E': 'C'} # compare with example above
    ['B', 'D', 'E', 'C', 'A'] > {'A': 'B', 'B': 'D', 'C': 'E', 'D': 'C', 'E': 'A'}
    ['D', 'E', 'C', 'A', 'B'] > {'A': 'D', 'B': 'E', 'D': 'A', 'E': 'B'}
    ['E', 'C', 'A', 'B', 'D'] > {'A': 'E', 'B': 'C', 'C': 'A', 'D': 'B', 'E': 'D'}
    ['C', 'A', 'B', 'D', 'E'] > {'A': 'C', 'B': 'A', 'C': 'B'}

    Notice how the third example actually implies two closed sorting graphs:
    ['D', 'E', 'C', 'A', 'B'] > [{'E': 'B', 'B': 'E'}, {'D': 'A', 'A': 'D'}]

Looking at the two closed subgraphs (that are found using recursive traversal of the graph in **_split_subgraphs_**) of
the third example, it becomes apparent that we need to execute both subgraphs to complete this sorting strategy. The
consecutive execution of multiple subgraphs may come with a catch.

Consider the following new, even-row-sized example:

    C E A B D F  # even sized row
    G H I J K L
    M N O P Q R
    
    a valid graph is:
    {'E': 'D', 'D': 'B', 'B': 'E', 'C': 'A', 'A': 'C'}

    implying two closed subgraphs
    [{'E': 'D', 'D': 'B', 'B': 'E'}, {'C': 'A', 'A': 'C'}

Here, the first subgraph produces (incl. init) 4 steps and ends with down (by coincidence). The next subgraph must start
of with up, because the last step was down. however, this subgraph produces (incl. init) only 3 steps. The total number
of steps is uneven and the wildcard 'G' will not return to its designated place. The first column is scrambled. To even
the number of steps a full turnover subgraph A --> B, B --> C, ... F --> A is added. This turnover subgraph has (incl.
init)
an uneven number of steps, since the row is even-sized. In total, the number of steps is even now and it is a valid
solution. These details are accounted for in **_choose_sort_strategy_** and  **_sort_by_subgraph_**.

If there is no single graph, that can produce an even total of steps, there is no solution to this toprow.

Currently, there is an effort (**_Toprow_short_**) to use all the knowledge that went into **_Toprow_**'s construction
and use **_sort_by_subgraph_** execution as basis for a far less verbose solution, avoiding the explicit computation of
the subgraphs and choice of strategy.

### (3) Transposed solving

It would seem that the board should be solved by now - or deemed unsolvable. However, a minor corner case is not covered
yet; following executing the strategies above for a board that has an uneven row and an even column length may yield no
valid sorting graph for the toprow (that is the overall number of steps across subgraphs is uneven) and hence deemed
unsolvable. Since the column dimension is even, the transposed board with its even toprow would be guaranteed to be
solvable
(as are all boards with an even sized toprow, since we always could do a total turnover: A --> B, B --> C, C --> D, ...
--> A that adds an uneven amount to the total steps and evens out any uneven (sub-)graph(s)). The trick in this case is
to actually transpose the board, solve it, transpose it back and translate the solution. This little optional D-Tour is
implemented as method decorator to the solve method that leverages the optional StrategyTranspose. The unsolvables are
unaffected from this strategy, as both their dimensions must be uneven.

### Use Case

    c = Cyclic_shift_board(
        [['C', 'W', 'M', 'F', 'J'], 
         ['O', 'R', 'D', 'B', 'A'], 
         ['N', 'K', 'G', 'L', 'Y'], 
         ['P', 'H', 'S', 'V', 'E'], 
         ['X', 'T', 'Q', 'U', 'I']])

    c.solve(
        [['A', 'B', 'C', 'D', 'E'], 
         ['F', 'G', 'H', 'I', 'J'], 
         ['K', 'L', 'M', 'N', 'O'], 
         ['P', 'Q', 'R', 'S', 'T'], 
         ['U', 'V', 'W', 'X', 'Y']])
    
    c.solution
    ['L2', 'U4', 'U4', 'R2', 'D4', 'D4', 'U0', 'U3', 'L3', 'L3', 'D0', 'D3', 
     'U2', 'U2', 'U2', 'U2', 'R0', 'D2', 'D2', 'D2', 'D2', 'U1', 'L3', 'L3', 
     'D1', 'U0', 'L3', 'D0', 'U3', 'U4', 'R2', 'D3', 'D4', 'U3', 'L2', 'L2', 
     'D3', 'U2', 'U2', 'R1', 'D2', 'D2', 'U1', 'U1', 'U1', 'L0', 'L0', 'D1', 
     'D1', 'D1', 'U0', 'U0', 'R1', 'R1', 'D0', 'D0', 'U4', 'R1', 'D4', 'U2', 
     'U3', 'R1', 'D2', 'D3', 'U2', 'U2', 'R0', 'R0', 'D2', 'D2', 'U1', 'R1', 
     'R1', 'D1', 'U4', 'L0', 'D4', 'U1', 'U3', 'R0', 'R0', 'D1', 'D3', 'L0', 
     'U2', 'R0', 'D2', 'U1', 'R0', 'D1', 'U0', 'L0', 'D0', 'L0', 'L0', 'L0', 
     'U0', 'L0', 'D0', 'L0', 'U0', 'R0', 'R0', 'D0', 'R0', 'R0']        

### Refactoring Ideas

(*) make the entire Toprow graph selection process generators.

(*) There must be a less verbose solution based on the very same insights from the graph approach. A good place to start
is StrategyToprow_short: specific solution to avoid the subgraph & choose strategy calculation. This strategy takes a
single graph - that may consist of closed subgraphs and moves according to it. In this variant, care must be taken to
ensure once the closed subgraph is traversed, the last u is countered with a starting d or vice versa. Also, if the
graph is executed and an uneven number of steps were used (== the board is not solved yet), do a full turnover. If it is
not solved by then, it is unsolvable. Are all graphs valid alternatives? only with an even row (or column)
length?

[0] https://www.codewars.com/kata/5c1d796370fee68b1e000611/train/python  
[1] https://refactoring.guru/design-patterns/strategy/python/example