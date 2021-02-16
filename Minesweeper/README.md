# Minesweeper Solver

#### A communication approach.

This package implements the refactored & successful solution to [Codewar's Minesweeper][0] kyu 1 kata. The originally
submitted (single file) solution draft can be found in Minesweeper.Minesweeper.py The refactored version emphasises on
structure, test- and maintainability. Additionally, it comes with a new debug interface and board sampling method. The
code is decluttered and far better documented & tested. The code of the state property, found_bomb and open are far more
consice and annotated with intent.


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

Except for this communication strategy, that is hardwired into the very foundation of the board, all other Strategies
are factored into separate classes according to the ['Strategy design pattern'][3]. This way the  **_Game_** is not
clutterd with solving strategies that go beyond the recursive pattern. The Algorithms are nicely separated from the
board and can be switched easily on demand.

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


2) **Supersets**. Double & tripple supersets  
   The basic idea of this strategy is best understood through the examples, it is intended to solve. Consider the
   following board:

         0 0 0
         1 2 1
         ? ? *

   The last row cannot be known by single Node's communication patterns; the ones will have two questionmarks and the
   two has three; none of them ever meets the condition  **_state_** == len(questionmarks). The communication strategy
   is thus incapable of solving such (common and early stage) patterns. However, considering all two  
   **_Node_**[s]  provides a definite solution: a single 1 and the 2 suffice: since 1's questionmarks are a real subset
   of two's questionmarks, two's state is 'softly' reduced and since two's surpluss questionmark is equal its reduced
   state from the soft reduction, * must be a bomb. However, this algorithm would require additional steps in a more
   complex example

         0 0 0 0 0
         1 1 2 1 1
         ? ? * ? ?

   here, the rightmost one's questionmarks are a subset of its neighbours' and in turn * can be opened. Recursive
   communication solves the rest, since opening * checks two's state against its no. of questionmarks - and finds the
   two bombs. In turn, the ones are reduced in state and the outer ? can be opened safely.

   The same logic can be applied in the following partial example

         x 3 ? ? ?
         x 3 ? ? ?
         2 3 ? ? ?
         x 2 1 ? ?  
      
         the state_map of the above example looks like this:
         x 1 ? ? ?  # topmost 1
         x 1 ? ? ?  # the one below
         0 1 ? ? ?
         x 1 1 ? ?  

         x 1 ? ? ?
         x 1 ? ? ?
         0 1 * ? ?
         x 1 1 ? ?  

   The * can be opened safely because of the above ones:
   the topmost one's questionmarks are a subset of the one's questionmarks below it. This is a 'soft' state reduction of
   the second one: it is certain that there is one bomb exacly in the questionmarks excluding the intersection of the
   two ones. The second one's state is 'softly' reduced to 0, and the questionmarks not contained in the intersection
   can can be opened safely.

   Upon revisiting the first example, it becomes apparent, that this variant could have been solved using three rather
   than two positions jointly as well:

         0 0 0
         1 2 1
         x 2 x

   since the two needs two bombs still and the ones' questionmarks build a non empty intersection, it wouldn't suffice
   to place a bomb underneath the two. What remains is the combination
   'x ? x'. Notice how this is still true, if the neighbouring ones' questionmarks are real supersets

        0 0 0 0 0
        1 1 2 1 1
        1 x 2 x 1

   This solution is far more general than it would lead on and is not at all restricted to this particular (but common)
   shape. Besides, since the strategy works with  **_state_** rather than clue, many information states of the game can
   be traced back to this solution.

   The next example is somewhat similar (sub/superset & intersection - based):

         * ? ?
         ? 2 1
         ? 1 0

   the top leftmost (*) can be opened safely, because the ones' questionmarks are a real subset of two's, but they '
   softly' reduce the state of 2, such that there cannot be a bomb in the corner. This former example is the lower right
   corner of the larger example:

         x 3 x ? ? ? ?
         1 3 x 3 ? ? ?
         0 2 2 3 ? * ?
         0 1 x 2 1 * ?  # 2 1 in this row
         0 1 2 ? ? 2 1
         0 0 1 ? ? 1 0

   Notice how the * positions can now be opened safely, because of the '2 1'. Because the 2 is of state 1, and 2's
   questionmarks are a subset to those of the one's questionmarks, one is 'softly' reduced to state 0, and all those
   questionmarks that are not shared with 2 (i.e. *) can be opened safely.

   Notice, that instead we could have derived something else by the same logic, looking at the two stacked 3s

         x 3 x * * ? ?
         1 3 x 3 ? ? ?  # the right one
         0 2 2 3 ? ? ?  # and this one
         0 1 x 2 1 ? ?
         0 1 2 ? ? 2 1
         0 0 1 ? ? 1 0

   If the state_map is considered, these types of informative pattern occur fairly frequent during the course of the
   game - and in very hard problems may even proove decisive very early on. The main intent of this strategy is to
   progress the board in tricky positions, where recursion simply does not suffice and brute force is way to expensive.
   There may exist more complex sets of logic, a real player may employ, but these "simple" comparisons proove very
   potent.

   Now that we established a feeling for what the algorithm is supposed to do, let's formalise it. The current
   implementation distinguishes set comparisons between two and three nodes. In both it favours informative
   comparisions, that is state comparisons, were at lest a one or in case of three nodes, two ones are used. This is a
   second pillar of simplification. It remains to be tested, if lifting this simplification will lead to runtime gains (
   since the endgames burden is reduced)
   or itself would be a burden.

   **_Double_**:
   Find those positions that are neighbour to a questionmark and not a bomb and of those find the ones of state 1, as
   they are most informative. Build all pairs of questionmark neighbours that themselves are neighbours and where at
   least one of them has state 1. For each pair check if the "larger"
   (i.e. higher state) position's questionmarks is a superset of the other. If True, check the soft state (i.e. the
   superset's state reduced by the smaller state)
   against the soft questionmarks i.e. the questionmarks without the intersection. if they are equal, all questionmarks
   without the intersection are bombs. if the soft state is 0, the questionmarks without the intersection can be opened
   safely.

   **_Triple_**:
   Essentially, it tries the same thing; Find those positions that are neighbour to a questionmark and not a bomb and of
   those find the ones of state 1, as they are most informative. Build all triples of questionmark neighbours that
   themselves are (intermediate) neighbours and where at least two of them have state 1. For each pair check if the "
   largest"
   (i.e. highest state) position's questionmarks is a superset of the union of the others. If True, check the soft
   state (i.e. the superset's state reduced by the smaller states)
   against the soft questionmarks i.e. the questionmarks without the intersections. also check if the soft state is
   zero.

   Notice how recursion is triggered whenever a bomb is found or a clue is opened!
   These two procedures can jointly be repeated
   **_relentless_**[ly] until the board does not change anymore.

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

2) When there is no further information derivable from a single position, Supersets is leveraged in relentless  
   execution - executing both double and tripple supersets to find higher level; aggregated information of multiple
   positions jointly.

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

* It is fairly apparent, that these two substrategies are very simmilar in structure, and usually DRY (Do not Repeat
  Yourself) is favoured: join the StrategySupersets.triple and double strategy to a single one

* The communication pattern may be more easily implemented via the ["Observer" design pattern][1]. The Issue here might
  be that each position must be both observer and sender and the recursive feedback loop must be avoided (solved in
  **_Node.state_**).

* Another option is to split the **_state_** property into subclasses, that can be more easily tested. This can be
  implemented in a ["State" design pattern][2]. easily. Issue: State.__init__ i.e. do's at the switch of a State are not
  accessible from the outside such as Game.board - which make debugging painstacking. The advantage is that the
  recursive communication behaviour (and when not to communicate) can be modeled far more verbose and explicitly. For a
  first draft check out the 'Refactor_Minesweeper_Statepattern' git branch.
* Implement random tests: make the board samplable

* StrategySupersets: do higher order comparisions or comparisons without the 'single' simplifaction help? or are they a
  mere computational burden?


### Issues:

* The recursion depth can be significant due to the communication.
* **_Endgame_** has a simplifying assumption on the number of bombs, before this 
strategy is leveraged to avoid to large amounts of combinations. Check if this 
assumption is necessary at all, since **_Superset_** solver is a fairly potent solver.
  
* The dependency between Node and Game (**_Node.game_**) to enable communication
and board awareness of the other Nodes and **_Node.game.open_** are not per se 
an issue, but there should be a more elegant solution to it.

<!--- MARKDOWN COMMENT: Reference Section-->

[0]: https://www.codewars.com/kata/57ff9d3b8f7dda23130015fa

[1]: https://refactoring.guru/design-patterns/observer

[2]: https://refactoring.guru/design-patterns/state

[3]: https://refactoring.guru/design-patterns/strategy

