Board
+++++

Make Board of 2 x 2 block of 4 x 4 squares. Each square has 3 states: Empty, Black, White

Board is rendered in window. 4 blocks in 2 by 2. 4 x 4 cells on each block.

Player stone is color of active player.

Opponent stone is color of inactive player

Consider flipping blocks for each player to have **home** boards on bottom.

* Create board
* Set stones
    * Stone
* Render board
    * Render blocks
    * Render cells in blocks
* Render stones
    * Taken stones on top of blocks
        * Group of black stones
            * Transparent when not taken
            * Colored black when taken
        * Group of white stones
            * Transparent when not taken
            * Colored white when taken
    * Stones on blocks
        * Cell with white on board is colored white
        * Cell with black on board is colored black
        * Empty cells on board are transparent
* Make play
    Initial implementation clicks original stone and destination cell.
    May be one or two cells away from original cell.
    Selection is in Home and Attack order. Evaluated after destination click.
    Highlight cells moved. Include pushed cells. Removed cells are highlighted on score bar.
    Future: Add arrow for movement.

    Future: Drag stone from original to destination cells.
    Pushing stones in movement. Highlight when not legel.

    * Enter Home movement
        * Highlight Home blocks and enable selecting cells
        * Select cell with player stone, Highlight cell, make bold
        * Select destination cell.
            Future: Check if move is legal, does not push stone
        * Future: Draw arrow from original cell to destination cell
    * Enter Attack movement
        * Highlight Attack blocks and enable selecting cells
        * Select cell with player stone, Highlight cell, make bold
        * Select destination cell.
            Future: Check if move is legal, pushes stone 0 or 1 stones.
        * Future: Draw arrow from original cell to destination cell
    * Enable make turn button
    * Click make turn button to Take Turn
* Render movement arrow