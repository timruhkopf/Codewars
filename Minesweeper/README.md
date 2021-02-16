# Minesweeper Solver

#### A communication approach.

This package implements the submitted and successful solution to [Codewar's Minesweeper][0] kyu 1 kata.


<!--- explain the boards & games conventions in this kata.-->

        result = """
        0 0 0 0 0 0 0 0 0 0 0
        0 0 0 1 2 3 3 2 1 0 0
        0 0 1 3 x x x x 1 0 0
        0 0 2 x x 6 x 5 2 0 0
        0 0 3 x 4 4 x x 2 0 0
        0 0 3 x 5 5 x x 2 0 0
        0 0 2 x x x x 3 1 0 0
        0 0 1 2 3 3 2 1 0 0 0
        0 0 0 0 0 0 0 0 0 0 0
        """

       gamemap = """
        0 0 0 0 0 0 0 0 0 0 0
        0 0 0 ? ? ? ? ? ? 0 0
        0 0 ? ? ? ? ? ? ? 0 0
        0 0 ? ? ? ? ? ? ? 0 0
        0 0 ? ? ? ? ? ? ? 0 0
        0 0 ? ? ? ? ? ? ? 0 0
        0 0 ? ? ? ? ? ? ? 0 0
        0 0 ? ? ? ? ? ? 0 0 0
        0 0 0 0 0 0 0 0 0 0 0
        """

Unsolvables:
A side note on solvability: not all boards are solvable, as the next example illustrates:

      result 
      0 1 x
      0 1 1

      gamemap 
      0 1 ?
      0 1 ?

There simply is not enough information in this board to remove all ambiguity in it. This board cannot be solved
definitively, but merely by chance. The solver is required to distinguish such cases and correctly.

### Key Concepts

Before delving into the solving strategies, let's get started with the basic set-up:
The original kata provided a 'gamemap' and a count of bombs. To allow the solver to inquire a positions value, the build
in **_open_** function was overloaded. Using the provided test cases and assertation set up forces a nasty interface, in
which the solver is aware of the solution. Both of which are usually considered bad practice. So instead, this package
provides a different interface; A **_Solution_** class, that is used in debugging only, parses the result map and places
it into a private attribute, accessible from within its scope only. An **_open_** method is added, that provides an
interface allowing single positions to be inquired from out of the class' scope. This method is called upon from within
the Solver, as the Solver is initialized with a reference to the optional
**_Solution_** object. Thereby, the Solver is completely unaware of the Solution and starts off with nothing but 0s and
questionmarks. This tidys up the Solver's interface. Furthermore, **_Solution_** implements a **_sample_board_** method,
that using the **_Game_** class, can create random boards easily and allows to create test examples to derive and test
the Algorithms.

The heart of the Solver consists of **_Node_**[s] and **_Game_**. The **_Game_**
class is mostly an aggregate dictionary {(row,column): **_Node_**[s]}, and each **_Node_** describes a positions
complete set of information and state including the clue ('?', 0, int ranging from 1 to 8), its immediate neighbours (
up to 8), the set of questionmark instances in its neighbours and the current **_state_**. The **_state_** property is a
concept that is crucial to the recursive communication strategy, that we will delve into more detailed in the '
Determinstic by state' subchapter. For the matter of readability, Nodes are set behaviour enabled, such that rather than
keeping track of index tuples in the questionmarks and neighb_inst attributes, each node indeed has the references to
the underlying objects. This renders lookups of the objects rather obsolete. Lastly, the Nodes are initialised with a
reference to the board, such that they can access the **_open_** method to inquire about themselves or their
questionmarks and to access the **_mark_bomb_** method to communicate to the board if it has found a bomb. The **_
open_**, **_mark_bomb_** and the **_state.setter_** methods are tightly intertwined and hardwired into the board. This
way __any__ (!) information obtained is immediately and automatically recursively communiciated accross the board.

### Intertwined Solving Strategies

Once the communication structure is in place, information must be generated. There are three strategies applied here:

<!--- MARKDOWN COMMENT: explain relentless decorator-->

1) **Determinstic by state**. The board starts off with 0's, whose neighbours are safe to **_open_**. Whenever a
   position is uncovered, the new value is added to its **_state_** and it is removed from its neighbours questionmarks.
   Should the number of questionmarks equal the **_state_**, all remaining questionmarks are informed, that they are
   bombs. If a **_Node_** is informed about being a bomb by calling  **_mark_bomb_** on them; The Node is  **_
   state_**
   and clue are set to 'x' they in turn informs all their neighbours by removing themselves from those neighbours
   questionmarks and reducing those neighbours  **_state_** by one. Since state is a property, each neighbour asks
   itself whether its  **_state_** is now 0 (all the bomb in its vicinity are found)
   or if the number of questionmarks equals its state. If any of the two conditions are met, it communicates
   accordingly. As a result, a recursive communication is invoked, whenever a position is opened, marked a bomb or the
   state is altered. Much care is taken to ensure state safety, that is the both  **_open_** and  **_mark_bomb_**
   ensure the board's state is clear before any further recursive communication is initiated. This recursive **_state_**
   property communication will be used in the subsequent algorithms automatically, whenever new information is revealed.

   Consider the following two boards:

         A:
         x 1 0

         B:
         x 2 0
         x 2 0

[comment]: <> (When either the number of "?" is the same as the number of)

[comment]: <> (   remaining bombs &#40;"**_clue_**"&#41; or the number of bombs found in the vicinity is exactly equal to)

[comment]: <> (   **_clue_**; indicating all remaining "?" neighbours can be **_open_**[ed] safely. This strategy is made use of during)

[comment]: <> (   the subsequent strategies automatically -without interrupting their flow-, whenever they uncover new )

[comment]: <> (   information.  )

2) **Supersets**. Double & tripple supersets  
   To grasp the basic idea of this strategy consider the following board.

         0 0 0
         1 2 1
         x 2 x

   The last row cannot be known by single Node's communication patterns; the ones will have two questionmarks and the
   two has three; none of them ever meets the condition  **_state_** == len(questionmarks). The first Strategy is thus
   incapable of solving such (common) patterns. However, considering all three  **_Node_**[s]
   provides a definite solution: since the two needs two bombs still and the ones questionmarks build a non empty
   intersection, it wouldn't suffice to place a bomb underneath the two. What remains is the combination
   'x ? x'. Notice how this is still true, if the neighbouring ones' questionmarks are real supersets

        0 0 0 0 0
        1 1 2 1 1
        1 x 2 x 1

   This solution is far more general than it would lead on and is not at all restricted to this particular (but common)
   shape. Besides, since the strategy works with  **_state_** rather than clue, many information states of the game can
   be traced back to this solution.


3) **Endgame.remain_bomb_count**
   Consider the following board

         0 0 0 0 0 0 0 0 0 
         0 0 1 2 3 3 2 1 0 
         0 1 3 x x x x 1 0 
         0 2 x x 6 x 5 2 0 
         0 3 x 4 4 x x 2 0 
         0 3 x 5 5 x x 2 0 
         0 2 x x x x 3 1 0 
         0 1 2 3 3 2 1 0 0 
         0 0 0 0 0 0 0 0 0 

   knowing the number of remaining bombs will reveal, that the inner clues can be opened safely. The opposite is true
   here:

         0 2 x x
         0 2 x x

   all remaining ? must be bombs and marked as such.


4) **Endgame.combinations**. The number of Bombs is very limited, indicating that most of the board is already unveiled.
   The Superset logic is no longer sufficient to solve the remaining board. To achieve a general solution, all the yet
   unveiled positions ("?") and their revealed neighbours are gathered to jointly decide if bombs placed on a subset of
   all available "?" is a valid combination. This again exploits the communication pattern for ease of checking the
   validity. In the first step, the combination of potential bombs is communicated to the entire board via a **_state_**
   update "-1" on each neighbour i.e. as if the bomb was really placed their, except the calls to **_open_** are
   prevented. Should any **_state_** become invalid, the combination is easily reverted with the opposite update. In
   this stage of the game -i.e. given this amount of information- multiple combinations may pose viable solutions. To
   reduce ambiguity and increase the amount of information available, those Nodes that have not been placed bombs on
   validly in any of the combinations are safe to be opened. Subsequently, the board is updated recursively, including
   any -now deterministic- bomb. This increases the amount of information. This procedure can be repeated
   **_relentless_**[ly] until the board is completely deterministically updated and solved. Should there be no change in
   the board during **_relentless_**
   execution and multiple "?" are left (multiple combinations viable), this board is ambiguous and thus unsolvable.

### solve()

With all those partial solutions in place, the whole **_solve_** method reads as follows:

1) Zeros: At the beginning of the board, there are zeros, whose neighbours can be opened safely. To leverage recursion
   and avoid opening zeros multiple times, a while loop is used, that pops the initially provided zeros and removes
   those of the zeros from the list that are already opened recursively in a previous step. This way each connected
   group is opened recursively by a single open call at this level. The interplay of
   **_state_**,  **_mark_bomb_** and  **_open_** recursively reveals all the information, that can be derived from a
   single position's state and questionmarks.

2) When there is no further information derivable from a single position, Supersets is leveraged in relentless execution
   - executing both double and tripple supersets to find higher level; aggregated information of multiple positions
     jointly.

3) ideally this already sufficed to solve the board, in this case , the StrategyEndgame
   **_remain_bomb_count_** method is invoked which merely checks if the number of remaining '?' equals the number of
   bombs or if all bombs were found.

4) if that did not suffice, StrategyEndgame is called to find positions that can be opened safely, as the restriction on
   the number of bombs and the clues indicate only a few remaining combinations of bombs across the '?' that are
   suitable. In this restricted number of suitable combinations, there might be positions, that by the provided
   information never can be occupied by a bomb - and thus can be opened safely. The same idea carries over to positions
   where in each combination a bomb is placed. In this case, it is certain, that a bomb must be placed there. Relentless
   execution repeats this strategy on the basis of the new (potentially recursive)
   information and stops once no additional information can be acquired. Should there be remaining ambiguity the board
   must be unsolvable and marked as such.

### Refactoring Ideas:

* The communication pattern may be more easily implemented via the ["Observer" design pattern][1]. The Issue here might
  be that each position must be both observer and sender and the recursive feedback loop must be avoided (solved in
  **_Node.state_**).

* Another option is to split the **_state_** property into subclasses, that can be more easily tested. This can be
  implemented in a ["State" design pattern][2]. easily. Issue: State.__init__ i.e. do's at the switch of a State are not
  accessible from the outside such as Game.board - which make debugging painstacking. The advantage is that the
  recursive communication behaviour (and when not to communicate) can be modeled far more verbose and explicitly.

* Implement random tests: make the board samplable

<!--
### Issues:

* The recursion depth can be significant due to the communication.
* **_Endgame_** has a simplifying assumption on the number of bombs, before this 
strategy is leveraged to avoid to large amounts of combinations. Check if this 
assumption is necessary at all, since **_Superset_** solver is a fairly potent solver.
  
* The dependency between Node and Game (**_Node.game_**) to enable communication
and board awareness of the other Nodes and **_Node.game.open_** are not per se 
an issue, but there should be a more elegant solution to it.

### TODOs
* write test cases for Node.state to ensure stability during maintainance
-->


<!--- MARKDOWN COMMENT: Reference Section-->

[0]: https://www.codewars.com/kata/57ff9d3b8f7dda23130015fa

[1]: https://refactoring.guru/design-patterns/observer

[2]: https://refactoring.guru/design-patterns/state

