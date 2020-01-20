Overview
********

App to play Pushing Stones with only one screen

Menu
++++++
Standard menu options:

* File
    * new
    * open
    * save
    * resign
    * close
* Game Options:
    * Play:
        * undo
        * redo
        * evaluate

Board
++++++
* Row of captured stones for white (init transparent)
* Row of captured stones for black (init transparent)
* 2x2 blocks with 4x4 cells(*buttons* transparent)
    * Add colored rectangle between rows of blocks.
        * Hight: 1/4 width of cells and 1/8 from each block
        * Width: spaning both blocks: 8 * width of cell + 1/2 width of cell
    * separate blocks by 1/2 width of cells
* 4 white stones in cell(*buttons* white)
* 4 white stones in cell(*buttons* black)
* *button* for making moves. Init: disabled. Enabled after Attack move set
    place center below blocks


Status
++++++
Game status: Player to move (white or black) or Game over (white|black) wins

Evaluation
++++++++++
Need to develop way to evaluate and render results