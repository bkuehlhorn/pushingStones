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
        * Select cell with player stone, Highlight cell, make bold
        * highlight attack destination cell and pushed stone
        * Future: Draw arrow from original cell to destination cell
    * Enable make turn button
    * Click make turn button to Take Turn
* Render movement arrow

todo:
    * setup turn actions:
        * click on valid destination cell:
            * restore style for home boards
            * set select style for attack boards
        * click on home destination cell:
            * reset style of attack boards
            * set active style of home boards
            * clear home destination cell and all attack cells
        * click on home stone:
            * reset style of attack boards
            * set active style of home boards
            * clear home stone, home destination cell and all attack cells
        * click on valid attack stone:
            * highlight attack destination cell
            * highlight pushed stone (future)
            * Enable move button
        * click on second valid attack stone:
            * clear old attack cells
            * do continue with valid attack stone steps

    * click on move button
        * add move to history
        * set new home cell with color stone
        * set old home cell with empty color
        * set new attack cell with color stone
        * if new moved stone on board:
            * set new moved stone cell with color stone
        * set old moved stone to empty
        * if new moved stone off board:
            * add board and color to captured stones
            * if game over: go to victory
        * set board for othe color move
