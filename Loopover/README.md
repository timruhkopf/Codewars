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


<!--explain the game's aim-->
The aim of the game is to translate some arbitrary initial configuration into 
another, using only the allowed instructions. 

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

**_Liftshift_** consists of three small substrategies, that are dependent on the 
relative position of a values current to its target position (same row, same 
col or neither?) that leave the already solved in their place after execution.
For the details of these minor and comprehensible strategies, please consult the source code.


### (2) Toprow - A Graph Approach.

Task: sort the first row of the puzzle & determine if there is any viable solution at all.

Currently under construction.
allows to analyse all possible sorings on their applicability - and thus if their 
are any viable solutions.

    rotations of [A, B, D, E, C] and their implied sorting graph

    ['A', 'B', 'D', 'E', 'C'] > {'C': 'D', 'D': 'E', 'E': 'C'}
    ['B', 'D', 'E', 'C', 'A'] > {'A': 'B', 'B': 'D', 'C': 'E', 'D': 'C', 'E': 'A'}
    ['D', 'E', 'C', 'A', 'B'] > {'A': 'D', 'B': 'E', 'D': 'A', 'E': 'B'}
    ['E', 'C', 'A', 'B', 'D'] > {'A': 'E', 'B': 'C', 'C': 'A', 'D': 'B', 'E': 'D'}
    ['C', 'A', 'B', 'D', 'E'] > {'A': 'C', 'B': 'A', 'C': 'B'}

    Notice how the third example actually implies two closed sorting graphs:
    ['D', 'E', 'C', 'A', 'B'] > [{'E': 'B', 'B': 'E'}, {'D': 'A', 'A': 'D'}]

<!-- elaborate Graph approach: what is the graph, elaborate on simple solution 
single connected uneven graph. checking connectivity, the general solution. 
point out, that all available sorting graphs are lazily? searched through and currently
the shortest course of actions is selected (is not necessarily true: shortest graph
currently can be a even graph, however, when selected, a full turnraound might be 
added to ensure even count of ups and downs -->

Initialisation of the algorithm. & wildcards  
Criteria for a solve graph (and what does not suffice)

### (3) Transposed solving

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

[0] https://www.codewars.com/kata/5c1d796370fee68b1e000611/train/python  
[1] https://refactoring.guru/design-patterns/strategy/python/example