Take Turn
*********

Turn is HomeCell, AttackCell, Direction and Distance.

* Movement:
    * HomeCell, AttackCell: Board, Cell
    * Direction: 0 to 7 with 0 Up, Clockwise.
    * Movement: 0, 1. Move +1 cells in Direction.
* Check Legal Movement: make callable from Board object
    * Parameters: Home|Attack, Board, Original Cell, Destination Cell
    * Check HomeCell Direction and Distance
        * HomeCell is on Home Boards
        * Cells from HomeCell, Direction and Distance are:
            * On Board.
            * Empty
    * Check AttackCell Direction and Distance
        * AttackCell is on Attack Boards
        * Cells from AttackCell, Direction and Distance are:
            * On Board.
            * Have no Friendly Stones
            * Have less than 2 Enemy Stones
    * Move HomeCells
        * Update board for stones in new location
    * Move AttackCells
        * Update board for stones in new location
        * Stones pushed off rendered at top
* Evaluate Winning Condition
    * True: Stones on any block is less than 3 for one color
    * False: otherwise
* Return Results