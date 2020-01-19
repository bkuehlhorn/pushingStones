"""
pushingStones application
--------------------------

Pushing Stones: game to push 2 stones off one of 2x2 blocks with 4x4 cells and 4 stones of each color on blocks


"""

from collections import namedtuple
import datetime
import gettext
from functools import partial
from math import copysign
from PIL import Image, ImageTk
import sys
import time
import tkinter
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename


# All translations provided for illustrative purposes only.
# english

BLOCK = namedtuple('BLOCK', 'column, row')
CELL = namedtuple('CELL', 'block column row')
DIRECTION = namedtuple('DIRECTION', 'column_delta, row_delta')


_ = lambda s: s
__ = lambda s: ' '.join(s)
def VALID_BLOCK(block):
    return ( -1 < block.column < 2) and (-1 < block.row < 2)
def VALID_CELL(cell):
    return (-1 < cell.column < 4) and (-1 < cell.row < 4)
def LOG_STATUSBAR(application, index=0, text='testing'):
    application.statusbar.set_text(index, text)

class MoveStones(object):
    """
    Support to move stones on home and attack boards.
        * saves home_stone, attack_stone, direction, distance
        * verify destination cell on block and valid cell
        * verify attack_stone moves on block and pushes 0 or 1 other stones
    """
    def __init__(self, application, home_stone):
        self.application = application
        self.home_stone = home_stone
        self.destination_cell = None
        self.attack_stone = None
        self.attack_destination_cell = None
        self.direction = None
        self.distance = None

    def __str__(self):
        return f'home={self.home_stone}:attack={self.attack_stone}:direction={self.direction}:distance={self.distance}'

    def set_attack_stone(self, cell):
        """
        # check for valid move
        # stays on board
        # pushes only 1 other stone

        :param cell:
        :return:
        """
        # check for valid move
        # stays on board
        # pushes only 1 other stone
        # self.attack_stone = cell
        if cell is None:
            self.attack_stone = None
        else:
            self.attack_stone = CELL(cell.block, cell.column, cell.row)
        return True

    def get_attack_stone(self):
        if self.attack_stone is None:
            return None
        else:
            return self.attack_stone.block.cells[self.attack_stone.column][self.attack_stone.row]

    def set_direction(self, direction, destination_cell):
        """
        # check for valid move
        # pushes only 0 stone

        :param direction:
        :param destination_cell:
        :return:
        """
        self.destination_cell = destination_cell
        self.direction = direction
        self.distance = max(abs(direction.column_delta), abs(direction.row_delta))
        return True

    def add_to_cell(self, to_cell):
        self.to_cell = to_cell
        self.rowDelta = self.from_cell.row - self.to_cell.row
        self.columnDelta = self.from_cell.column - self.to_cell.column
        self.direction = max(abs(self.rowDelta), abs(self.columnDelta))
        return

    def clear_cells(self, cell):
        # if cell in (self.home_stone, self.destination_cell, self.attack_stone)
        if cell == self.get_attack_stone():
            self.get_attack_stone().set_cell(style='')
            self.set_attack_stone(None)
            if self.attack_destination_cell is not None:
                self.attack_destination_cell.set_cell(style='')
                self.attack_destination_cell = None
            LOG_STATUSBAR(self.application, 3, 'Select attack cell')
            return True
        elif cell == self.destination_cell:
            if self.get_attack_stone() is not None:
                self.get_attack_stone().set_cell(style='')
                self.set_attack_stone(None)
                self.attack_destination_cell.set_cell(style='')
                self.attack_destination_cell = None
            self.destination_cell.set_cell(style='')
            self.destination_cell = None
            self.direction = None
            self.distance = None
            LOG_STATUSBAR(self.application, 3, 'Select destination cell')
            return True
        elif cell == self.home_stone:
            if self.get_attack_stone() is not None:
                self.get_attack_stone().set_cell(style='')
                self.set_attack_stone(None)
                self.attack_destination_cell.set_cell(style='')
                self.attack_destination_cell = None
            if self.destination_cell is not None:
                self.destination_cell.set_cell(style='')
                self.destination_cell = None
                self.direction = None
                self.distance = None
            self.home_stone.set_cell(style='')
            self.home_stone = None
            LOG_STATUSBAR(self.application, 3, 'Select home stone')
            return True
        else:
            LOG_STATUSBAR(self.application, 3, 'You have nothing to reset. Play on')
        return False


    def use_distance(self, block, direction, distance):
        """
        possible to save pushed cells. one for each distance
        :param direction:
        :param distance:
        :return:
        """
        self.direction = direction
        self.distance = distance
        self.to_cell = CELL(block,
                            self.from_cell.column + self.distance.columnDelta * self.distance,
                            self.from_cell.row + self.distance.rowDelta * self.distance)
        self.pushed_cells = [] # one or two cells are pushed
        return VALID_CELL(self.to_cell)


class PopupDialog(ttk.Frame):
    """
    Sample popup dialog implemented to provide feedback.

    """

    def __init__(self, parent, title, body):
        ttk.Frame.__init__(self, parent)
        self.top = tkinter.Toplevel(parent)
        _label = ttk.Label(self.top, text=body, justify=tkinter.LEFT)
        _label.pack(padx=10, pady=10)
        _button = ttk.Button(self.top, text=_("OK"), command=self.ok_button)
        _button.pack(pady=5)
        self.top.title(title)

    def ok_button(self):
        "OK button feedback."

        self.top.destroy()



class StatusBar(ttk.Frame):
    """
    Sample status bar provided by cookiecutter switch.

    """
    _status_bars = 4

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.labels = []
        self.config(border=1, relief=tkinter.GROOVE)
        for i in range(self._status_bars):
            _label_text = _('Unset status ') + str(i + 1)
            self.labels.append(ttk.Label(self, text=_label_text))
            self.labels[i].config(relief=tkinter.GROOVE)
            self.labels[i]['style'] = 'status.TLabel'
            self.labels[i].pack(side=tkinter.LEFT, fill=tkinter.X)
        self.pack()

    def set_text(self, status_index, new_text):
        self.labels[status_index].config(text=new_text)



class ToolBar(ttk.Frame):
    """
    Sample toolbar provided by cookiecutter switch.

    """

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.buttons = []
        self.config(border=1, relief=tkinter.GROOVE)
        for i in range(1, 5):
            _button_text = _('Tool ') + str(i)
            self.buttons.append(ttk.Button(self, text=_button_text,
                                           command=lambda i=i: self.run_tool(i)))
            self.buttons[i - 1].pack(side=tkinter.LEFT, fill=tkinter.X)
        self.pack()

    def run_tool(self, number):
        """
        Sample function provided to show how a toolbar command may be used.

        :param number:
        :return:
        """

        print(_('Toolbar button'), number, _('pressed'))
        self.master.mainframe.tick(f'Toolbar {number} clicked')



class MainFrame(ttk.Frame):
    """
    Main area of user interface content.

    """

    past_time = datetime.datetime.now()
    _advertisement = 'Cookiecutter: Open-Source Project Templates'
    _product = _('Template') + ': pushing stones'
    _boilerplate = _advertisement + '\n\n' + _product + '\n\n'

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        # self.boardframe = Board(self, 0, 0)
        # self.boardframe.pack(side='left') #, fill='y')
        # self.boardframe.(color)

        self.display = ttk.Label(parent, anchor=tkinter.CENTER, name='label',
                                 foreground='green', background='black')
        self.display.pack(fill=tkinter.BOTH, expand=1)

        self.display = ttk.Label(parent, anchor=tkinter.CENTER, name='label',
                                 foreground='green', background='black')
        self.display.pack(fill=tkinter.BOTH, expand=1)

        self.tick()
        self.b1 = ttk.Button(self, text='Button 1', name='b1', command=self.click1)
        self.b1.pack(side='left')
        self.b2 = ttk.Button(self, text='Button 2', name='b2', command=self.click2)
        self.b2.pack(side='left')

    def click1(self):
        # print('Button 1 clicked.')
        self.master.main_frame.tick('Button 1 clicked')

    def click2(self):
        # print('Button 2 clicked.')
        self.b1.invoke()
        self.master.main_frame.tick('Button 2 clicked')

    def tick(self, button='none'):
        "Invoked automatically to update a clock displayed in the GUI."

        this_time = datetime.datetime.now()
        if this_time != self.past_time:
            self.past_time = this_time
            _timestamp = this_time.strftime('%Y-%m-%d %H:%M:%S')
            self.display.config(text=self._boilerplate + _timestamp + f'\n\n{button}')
        self.display.after(10000, self.tick)


class Board(tkinter.Canvas):
    """
    Row of 5 black capture cells, one from each block and one more is game over
    Row of 5 white capture cells, one from each block and one more is game over
    2x2 blocks of 4x4 cells for stones
    Home: movement, Attach movement (movement: block: x,y, direction, cells moved)
    Move button (enabled when Home and Attack are set)

    Design:
        Render: board, blocks, cells and cell button
        Highlight: Home Blocks, Attack Blocks, Origin Cell, Destination Cell

        methods:
            undo: backout history move
            redo: do history again

        Click cell button:
            if home origin cell is empty
                if cell is same color:
                    highlight cell,
                    save column and row for original home block
                else:
                    report error
            else if home origin cell is not empty
                if distance is more than 2 or stones in destination cells:  -- check cell 1 or 2 in direction
                    report error, highlight cells
                else:
                    highlight cell,
                    save column and row for destination home block
                    highlight attack blocks

            else if home origin cell is not empty and attack origin cell is same color:
                highlight cell,
                save column and row for destination home block
                action is attack destination cell
                calculate attack destination cell and highlight
                if is attack destination cell off board or attack pushes 2 stones or (maybe) pushes own stone:
                    report error, highlight cells, action is home destination cell

                else:
                    highlight cell,
                    save column and row for origin attack block,
                    save column and row for destination attack block -- may not save this
                    clear attack blocks highlight
            else:
                report error: select your stone to move

    """
    image_size = 75
    # player = 'white' # color of current player
    home_boards = {'white': 0, 'black': 1}  # rows
    attack_boards = [1, 0] # selected home board column is index to attack column

    # test different initial placement and captured stones
    # initial_white_stones_test = {
    #     '0,0': [CELL(1, 0), CELL(0, 1), CELL(0, 2), CELL(0, 3)],
    #     '0,1': [CELL(0, 0), CELL(2, 1), CELL(0, 2), CELL(0, 3)],
    #     '1,0': [CELL(0, 0), CELL(0, 1), None,       CELL(0, 3)],
    #     '1,1': [CELL(0, 0), CELL(0, 1), CELL(0, 2), None]
    # }
    # initial_black_stones_test = {
    #     '0,0': [CELL(3, 0), CELL(3, 1), CELL(3, 2), None],
    #     '0,1': [CELL(3, 0), CELL(3, 1), CELL(2, 2), CELL(3, 3)],
    #     '1,0': [CELL(3, 0), CELL(1, 1), CELL(3, 2), CELL(3, 3)],
    #     '1,1': [None,       CELL(3, 1), CELL(3, 2), CELL(3, 3)]
    # }
    # self.set_board(initial_white_stones_test, initial_black_stones_test)

    initial_white_stones = {
        '0,0': [CELL(BLOCK(0, 0), 0, 0), CELL(BLOCK(0, 0), 0, 1), CELL(BLOCK(0, 0), 0, 2), CELL(BLOCK(0, 0), 0, 3)],
        '0,1': [CELL(BLOCK(0, 1), 0, 0), CELL(BLOCK(0, 1), 0, 1), CELL(BLOCK(0, 1), 0, 2), CELL(BLOCK(0, 1), 0, 3)],
        '1,0': [CELL(BLOCK(1, 0), 0, 0), CELL(BLOCK(1, 0), 0, 1), CELL(BLOCK(1, 0), 0, 2), CELL(BLOCK(1, 0), 0, 3)],
        '1,1': [CELL(BLOCK(0, 1), 0, 0), CELL(BLOCK(1, 1), 0, 1), CELL(BLOCK(1, 1), 0, 2), CELL(BLOCK(1, 1), 0, 3)]
    }
    initial_black_stones = {
        '0,0': [CELL(BLOCK(0, 0), 3, 0), CELL(BLOCK(0, 0), 3, 1), CELL(BLOCK(0, 0), 3, 2), CELL(BLOCK(0, 0), 3, 3)],
        '0,1': [CELL(BLOCK(0, 1), 3, 0), CELL(BLOCK(0, 1), 3, 1), CELL(BLOCK(0, 1), 3, 2), CELL(BLOCK(0, 1), 3, 3)],
        '1,0': [CELL(BLOCK(1, 0), 3, 0), CELL(BLOCK(1, 0), 3, 1), CELL(BLOCK(1, 0), 3, 2), CELL(BLOCK(1, 0), 3, 3)],
        '1,1': [CELL(BLOCK(0, 1), 3, 0), CELL(BLOCK(1, 1), 3, 1), CELL(BLOCK(1, 1), 3, 2), CELL(BLOCK(1, 1), 3, 3)]
    }

    def __init__(self, parent, x, y):
        # ttk.Frame.__init__(self, parent)
        super().__init__(parent) # create a frame (self)
        self.application = self.master
        self.setup_cells = False

        self.other_stone = {'white': 'black', 'black': 'white'}
        self.capture_detail = {'black': [], 'white': []}
        self.capture_count = {'black': 0, 'white': 0}
        self.capture_black = set
        self.capture_white = set
        self.blocks = [[0,1],[2,3]]
        self.move_history = [] # (move, push)
        self.game_over = False

        self.images = dict(empty=self.make_image('image/emptycell.png'),
                           black=self.make_image('image/blackStone.png'),
                           white=self.make_image('image/whiteStone.png'))

        for column in range(2):
            for row in range(2):
                block = Block(self, column, row, self.images, 0, 0, name=f'block:{column}:{row}')
                block.grid(column=column*6, row=row*10+2, columnspan=6)
                self.blocks[column][row] = block

        self.init_board()
        self.set_board(self.initial_white_stones, self.initial_black_stones)

        self.clear_button = ttk.Button(self, text=f'clear moves', name=f'clear moves', command=self.clear_moves)
        self.clear_button['style'] = 'BW.TButton'
        self.clear_button.grid(column=5, row=13)

        self.move_button = ttk.Button(self, text=f'make move', name=f'make move', command=self.make_moves)
        self.move_button['style'] = 'BW.TButton'
        self.move_button.grid(column=6, row=13)

        pass

    def get_block_style(self):
        blocks_style = list(map(lambda x: list(map(lambda y: y['style'], x)), self.blocks))
        return blocks_style

    def set_player(self, color):
        """
        save color as current player
        highlight home boards for current player

        :param color:
        :return:
        """
        self.current_player = color
        # self.from_cell = None  # CELL
        # self.home_move = None  # MOVE_STONE
        # self.attack_move = None  # MOVE_STONE
        self.move = None

        self.set_home_active(self.current_player)

    def set_blocks_style(self, style='block.TFrame'):
        # change style for all blocks
        for block_column in range(2):
            for block_row in range(2):
                self.blocks[block_column][block_row]['style'] = style

    def set_home_active(self, color, style='active.block.TFrame'):
        # home blocks for white are [1][0] and [1][1]
        # change style to highlight
        for block_column in range(2):
            self.blocks[block_column][self.home_boards[color]]['style'] = style

    def set_attack_active(self, block, style='active.block.TFrame'):
        # home blocks for white are [1][0] and [1][1]
        # change style to highlight
        for block_row in range(2):
            self.blocks[self.attack_boards[block.column]][block_row]['style'] = style

    def clear_moves(self):
        if self.move is not None:
            self.move.clear_cells()

    def make_moves(self):
        """
        hold method for moving stones:
            find pushed stones
            home stone moves: empty origin cell, color destination cell
            move pushed attack stone: empty origin cell, (color destination cell or add pushed off stones to capture images)
            attack stone moves: empty origin cell, color destination cell
            save push for history
            player is other color
            highlight home blocks for player

        add to self.move_history: move, push

        :return:

        """
        if self.move.attack_destination_cell is not None:
            pushed_stone = self.find_pushed_stone(self.move)
            if pushed_stone is not None:
                pushed_to = self.move.attack_destination_cell.get_next_cell(self.move)
                if pushed_to is not None:
                    pushed_to = self.find_cell(pushed_to)
                    pushed_stone.block.move_stone(pushed_stone, pushed_to)
                else:
                    self.capture_stone(pushed_stone)
                    pushed_stone.set_cell(color='empty')

            self.move.get_attack_stone().block.move_stone(self.move.get_attack_stone(),
                                                    self.move.attack_destination_cell)
            self.move.home_stone.block.move_stone(self.move.home_stone,
                                                  self.move.destination_cell)
            self.move.clear_cells(self.move.home_stone)
            self.set_player(self.other_stone[self.current_player])

        return True

    def find_pushed_stone(self, move):
        next_cell = move.get_attack_stone()
        for push_distance in range(move.distance):
            next_cell = next_cell.get_next_cell(move)
            if next_cell is not None and next_cell.get_cell_color() == self.other_stone[self.current_player]:
                return next_cell
        return None

    def capture(self, color):
        """
        Add to captured stones
        Count stones captured from each board by color

        :param color: color of captured stone
        :return: false: game continue, true: game over
        """
        self.captured_stones[color][self.capture_count[color]].configure(image=self.images[color])
        self.capture_count[color] += 1
        #todo check game over: captured 2 stones from one board. check new board string in captured set
        #todo save board for captured stones: add board string to set
        # save move in history. Need to add history to __init__
        return False # default to continue playing

    def capture_stone(self, stone):
        color = stone.get_cell_color()
        self.capture(color)
        self.capture_detail[color].append(stone)

    def make_image(self, png):
        photo = Image.open(png)
        return ImageTk.PhotoImage(photo.resize((self.image_size, self.image_size)))

    def set_capture_stones(self, image, column, row):
        """
        is this needed
        need to pass color and mape to image
        :param image:
        :param column:
        :param row:
        :return:
        """
        capture_cells = []
        for each in range(5):
            capture = tkinter.Label(self, image=image)
            capture.grid(column=each+column, row=row)
            capture_cells.append(capture)
        return capture_cells

    def init_board(self):
        """

        :return:
        """
        for block_column in range(2):
            for block_row in range(2):
                for cell_column in range(4):
                    for cell_row in range(4):
                        cell = self.blocks[block_column][block_row].cells[cell_column][cell_row]
                        cell.set_cell(style='', color='empty')

        self.captured_stones = {'black': self.set_capture_stones(self.images['empty'], column=0, row=1),
                                'white': self.set_capture_stones(self.images['empty'], column=6, row=1)}
        self.move = None

    def set_board(self, white_stones, black_stones):
        """
        clear stones off board
        Put stones on board and captured
        stone list is four[0-3] cells in each block [0-1][0-1]

        :param white_stones: list of stones, None in list are captured
        :param black_stones: list of stones, None in list are captured
        :return:
        """
        for block, stones in white_stones.items():
            (block_column, block_row) = block.split(',')
            block_column = int(block_column)
            block_row = int(block_row)
            self.set_stones('white', block_column, block_row, stones)

        for block, stones in black_stones.items():
            (block_column, block_row) = block.split(',')
            block_column = int(block_column)
            block_row = int(block_row)
            self.set_stones('black', block_column, block_row, stones)

    def set_stones(self, color, block_column, block_row, stones):
        """

        :param stones:
        :return:
        """
        for stone in stones:
            if stone is None:
                #todo need to fix this capture of stone
                # self.capture_stone(stone)
                pass
            else:
                cell = self.blocks[block_column][block_row].cells[stone.row][stone.column]
                cell.set_cell(color=color)

    def find_cell(self, cell):
        """
        find cell in block on board in app

        :param cell: block, (0-3), (0-3)
        :return: null if no cell found (bad block values, bad cell values
        """
        if VALID_BLOCK(cell.block) and VALID_CELL(cell):
            app_block = self.blocks[cell.block.column][cell.block.row]
            app_cell = app_block.cells[cell.column][cell.row]
            return app_cell
        else:
            return None


class Block(ttk.Frame):
    """
    Block of 4x4 cells
    Render buttons for cells starting a x, y of parent.
    """

    def __init__(self, parent, block_column, block_row, images, column=0, row=0, name=''):
        # ttk.Frame.__init__(self, parent, borderwidth=20)
        ttk.Frame.__init__(self, parent, style='block.TFrame', borderwidth=20, name=name)
        self.application = self.master.master
        self.board = self.master
        self.column = block_column
        self.row = block_row

        self.cell_image = images

        button_size = 20
        # create
        self.cells = []
        for cell_column in range(4):
            row_cells = []
            for cell_row in range(4):
                cell = Cell(self, color='empty', column=cell_column, row=cell_row, name=f'{name}:{cell_column}:{cell_row}')
                cell.grid(column=cell_column, row=cell_row)
                row_cells.append(cell)
            self.cells.append(row_cells)
        pass

    def __str__(self):
        return f'{self.board}:block={self.column}:{self.row}:style={self["style"]}'

    def move_stone(self, from_cell, to_cell):
        """

        :param from_cell: cell for stone to move
        :param to_cell: cell to move stone
        :return: False if to_cell is not empty, True if move works
        """
        if to_cell.get_cell_color() != 'empty':
            return False
        to_cell.set_cell(color=from_cell.get_cell_color())
        from_cell.set_cell(color='empty')
        return True

    def in_cell(self, column, row, colors):
        """

        :param colors: single color or list of colors
        :return: true if is, false if not
        """
        return self.cells[column][row].cget('text') == colors

    def reset_all_cells(self):
        for column in range(4):
            for row in range(4):
                self.cells[column][row].set_cell(color='empty', style='')

    def all_styles(self):
        # return list(map(lambda x: list(map(lambda y: f'{self}:{y}', x)), list(self.cells)))
        return list(map(lambda x: list(map(lambda y: f'{self} style:{y["style"]}', x)), list(self.cells)))

    def all_text(self):
        # return list(map(lambda x: list(map(lambda y: f'{self}:{y}', x)), list(self.cells)))
        return list(map(lambda x: list(map(lambda y: f'{self} contents:{y.cget("text")}', x)), list(self.cells)))

class Cell(ttk.Frame):
    """
    Button where stones are placed and moved.

    """
    def __init__(self, parent, color, column, row, *args, **kwargs):
        """
        Block, images and location for cell
        :param parent: block
        :param color: black, white, empty
        :param x: column
        :param y: row
        """
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.application = self.master.master.master
        self.board = self.master.master
        self.block = self.master
        self.column = column
        self.row = row
        self.change_cell = {'empty': 'white', 'white': 'black', 'black': 'empty'}

        image = self.master.cell_image[color]
        self.button = CellButton(parent, *args, image=image, text=color, command=partial (self.select_stone), **kwargs)

    def __str__(self):
        return f'{self.block}:{self.get_cell_color()}:{self.column}:{self.row}'

    def select_stone(self):
        """
        First click: home cell is None
            clear highlights
            cell has player stone: false: ignore click
            select stone to move
            highlight cell: green

        Second click: home cell is not None
            destination cell
            if legal move from first cell to cell: highlight destination cell: green
            else: status error, highlight destination cell: red

        Third click: home destination is not None
            attack origin cell
            calculate attack destination cell
            verify 0 or 1 opponent's stones are pushed
            {details}

        :return:
        """
        s = ttk.Style()
        color = self.board.current_player
        name = self.winfo_name().split(':')
        # look for a better way
        (_, block_column, block_row, cell_column, cell_row) = name
        block = self.block
        cell = self

        if self.board.setup_cells:
            image_keys = list(self.master.cell_image.keys())
            index = image_keys.index(cell.get_cell_color()) + 1
            index = index if index < len(image_keys) else 0
            cell.set_cell(color=image_keys[index])
            return
        if not VALID_BLOCK(block) or not VALID_CELL(self):
            LOG_STATUSBAR(self.application, 3, f'invalid cell {name}')
            return

        if self.board.move is not None and self.board.move.clear_cells(self):
            return

        LOG_STATUSBAR(self.application, text=color)
        LOG_STATUSBAR(self.application, 1, name)
        LOG_STATUSBAR(self.application, 2, self.button.cget('text'))
        # LOG_STATUSBAR(self.application, 3, self['style'])
        # if self['style'] == 'selected.TLabel':
        #     LOG_STATUSBAR(self.application, 3, f'Please select another cell')
        #     self['style'] = ''
        #     self.board.move = None
        #     return

        if self.board.move is None or self.board.move.home_stone is None:
            if color != self.button.cget('text'):
                LOG_STATUSBAR(self.application, 3, f'Please select your own stone')
                return

            self.board.move = MoveStones(self.application, home_stone=cell)
            LOG_STATUSBAR(self.application, 3, f'Please select destination cell')
            self['style'] = 'selected.TLabel'
        elif self.board.move.direction is None:
            if 'empty' != self.button.cget('text'):
                LOG_STATUSBAR(self.application, 3, f'Please select an empty cell')
                return
            if block != self.board.move.home_stone.block:
                LOG_STATUSBAR(self.application, 3, f'Please cell on same block')
                return
            direction = DIRECTION(cell.column - self.board.move.home_stone.column,
                                  cell.row - self.board.move.home_stone.row
                                  )

            if (abs(direction.column_delta) == abs(direction.row_delta) and abs(direction.column_delta) > 2) or (
                    abs(direction.column_delta) == 0 and abs(direction.row_delta) > 2) or (
                    abs(direction.row_delta) == 0 and abs(direction.column_delta) > 2) or (
                    (abs(direction.column_delta) != abs(direction.row_delta) and (
                        abs(direction.column_delta) != 0 and abs(direction.row_delta) != 0))):
                LOG_STATUSBAR(self.application, 3, f'Please cell closer to stone to move')
                return
            self.board.move.set_direction(direction=direction, destination_cell=self)

            if self.destination_cells_invalid(self.board.move, self.board.move.home_stone, 1):
                LOG_STATUSBAR(self.application, 3, f'Destination cells must be empty')
                return

            self['style'] = 'selected.TLabel'
            self.board.set_blocks_style()
            self.board.set_attack_active(self.board.move.home_stone.block, style='active.block.TFrame')
            LOG_STATUSBAR(self.application, 3, f'Please select stone to move on attack blocks')
        elif self.board.move.get_attack_stone() == None:
            '''
            verify attack move:
                On attack blocks
                own stone
                move destination on block
                push 0 or 1 stone
                push only other stone (check if push own is valid)
                
            '''
            if self.button.cget('text') == color:
                self['style'] = 'selected.TLabel'
                self.board.move.set_attack_stone(self)
                #todo target can not be over edge of block

                if self.destination_cells_invalid(self.board.move, self.board.move.get_attack_stone(), 1):
                    #todo check for color of pushed cell
                    self.board.move.attack_destination_cell = None
                    LOG_STATUSBAR(self.application, 3, f'Attack Destination cell invalid')
                    return
                attack_destination_column = self.column + self.board.move.direction.column_delta
                attack_destination_row = self.row + self.board.move.direction.row_delta
                self.board.move.attack_destination_cell = self.block.cells[attack_destination_column][attack_destination_row]
                if VALID_CELL(self.board.move.attack_destination_cell):
                    self.board.move.attack_destination_cell.set_cell(style='selected.TLabel')
                #todo verify 0 or 1 other stone pushed

                self.board.set_blocks_style()
                LOG_STATUSBAR(self.application, 2, f'tbd')
                LOG_STATUSBAR(self.application, 3, f'Hit make move when done')
            else:
                LOG_STATUSBAR(self.application, 3, f'Please select stone to move on attack blocks')
        pass

    def destination_cells_invalid(self, move, cell, count=0):
        """
        ensure destination cells are empty. No pushing on home board

        :param move: Move to be checked
        :param cell: Cell to be moved
        :param count: Number of cells pushed
        :return:
        """
        column = cell.column # copy to prevent changing cell
        row = cell.row # copy to prevent changing cell
        column_delta = 0 if move.direction.column_delta == 0 else int(copysign(1, move.direction.column_delta))
        row_delta = 0 if move.direction.row_delta == 0 else int(copysign(1, move.direction.row_delta))
        pushed_stones = 0
        for place in range(move.distance + 1):
            column += column_delta
            row += row_delta
            if not ((-1 < column < 4) and (-1 < row < 4)):
                if place == move.distance:
                    continue
                return 'off board'
            if not self.block.in_cell(column, row, 'empty'):
                if self.block.in_cell(column, row, cell.get_cell_color()):
                    return True
                pushed_stones += 1
                if pushed_stones > count:
                    return True
        return False

    def get_next_cell(self, move):
        cell = CELL(self.block,
                    self.column + int(copysign(1, move.direction.column_delta)),
                    self.row + int(copysign(1, move.direction.row_delta)))
        if VALID_CELL(cell):
            cell = self.board.find_cell(cell)
            return cell
        else:
            return None

    def get_push_cell(self, move):
        cell = CELL(self.block,
                    self.column + move.direction.column_delta,
                    self.row + move.direction.row_delta)
        if VALID_CELL(cell):
            cell = self.board.find_cell(cell)
            return cell
        else:
            return None

    def check_move_cells(self, stone, direction, distance):

        pass

    def set_cell(self, color=None, style=None):
        """
        :param color: black, white, or empty
        :param style: Style for cell
        :return:
        """
        if color is not None:
            image = self.master.cell_image[color]
            self.button.configure(image=image, text=color)
        if style is not None:
            self['style'] = style

    def get_cell_color(self):
        return self.button.cget('text')

    def get_cell_style(self):
        return self['style']


class CellButton(ttk.Button):
    """
    Button where stones are placed and moved.

    """
    def __init__(self, parent, *args, **kwargs):
        """
        Block, images and location for cell
        :param parent: block
        :param images: list of images to render
        :param color: black, white, empty
        :param x: column
        :param y: row
        """
        ttk.Button.__init__(self, parent, *args, **kwargs)
        self.application = self.master.master.master.master
        self.board = self.master.master.master
        self.block = self.master.master

        # self.cell_image = images


class MenuBar(tkinter.Menu):
    """
    Menu bar appearing with expected components.

    """

    def __init__(self, parent):
        """
        “File(new, open, save, resign, close) Game Options: Play: undo, redo, evaluate”

        Excerpt From: Bernard Kuehlhorn. “Pushing Stones Application.” Apple Books.
        """
        tkinter.Menu.__init__(self, parent)

        filemenu = tkinter.Menu(self, tearoff=False)
        filemenu.add_command(label=_('New game'), command=self.new_dialog)
        filemenu.add_command(label=_('Open'), command=self.open_dialog)
        filemenu.add_command(label=_('Save'), command=self.save_dialog)
        filemenu.add_separator()
        filemenu.add_command(label=_('Exit'), underline=1,
                             command=self.quit)

        playmenu = tkinter.Menu(self, tearoff=False)
        playmenu.add_command(label=_('Undo'), command=self.undo_dialog)
        playmenu.add_command(label=_('Redo'), command=self.redo_dialog)
        filemenu.add_separator()
        playmenu.add_command(label=_('Evaluate'), command=self.evaluate_dialog)
        playmenu.add_command(label=_('Setup'), command=self.setup_dialog)

        helpmenu = tkinter.Menu(self, tearoff=False)
        helpmenu.add_command(label=_('Help'), command=lambda:
                             self.help_dialog(None), accelerator="F1")
        helpmenu.add_command(label=_('About'), command=self.about_dialog)
        self.bind_all('<F1>', self.help_dialog)

        self.add_cascade(label=_('File'), underline=0, menu=filemenu)
        self.add_cascade(label=_('Play'), underline=0, menu=playmenu)
        self.add_cascade(label=_('Help'), underline=0, menu=helpmenu)

    def quit(self):
        """
        Ends toplevel execution.

        :return:
        """

        sys.exit(0)

    def help_dialog(self, event):
        """
        Dialog cataloging results achievable, and provided means available.

        :param event:
        :return:
        """

        _description = __(['Pushing Stones Application.', '\n',
                           'Game with 2x2 boards with 4x4 cells', '\n',
                           ' Two stones are moved 1 or 2 cells', '\n',
                           ' First stone is moved on one of boards closest to player.', '\n',
                           ' Home store can push another stone.', '\n',
                           ' Second stone is move on other column boards.', '\n',
                           ' Second stone can push one other stone.', '\n',
                           ' Stones pushed off a board is captured.', '\n',
                           ' ', '\n',
                           'Game is won by capturing 2 stones from one board.'])
        PopupDialog(self, 'pushing stones', _description)

    def about_dialog(self):
        """
        Dialog concerning information about entities responsible for program.

        :return:
        """

        _description = __(['Pushing Stones:', '\n',
                            ' game to push 2 stones off one of 2x2 blocks', '\n',
                            ' with 4x4 cells and 4 stones of each color on blocks'])
        # _description = ''
        if _description == '':
            _description = __(['No description available', '\n',
                               '\n',
                               _('Author'), ': Bernard Kuehlhorn', '\n',
                               _('Email'), ': bkuehlhorn@acm.org', '\n',
                               _('Version'), ': 0.0.1', '\n',
                               _('GitHub Package'), ': pushingStones'])
        PopupDialog(self, _('About') + ' pushing stones',
                    _description)

    def new_dialog(self):
        """
        Non-functional dialog indicating successful navigation.

        :return:
        """

        # PopupDialog(self, _('New button pressed'), _('implemented'))
        self.master.board.init_board()
        self.master.board.set_board(self.master.board.initial_white_stones,
                                    self.master.board.initial_black_stones)
        #todo reset history, set origin board

    def open_dialog(self):
        """
        Standard askopenfilename() invocation and result handling.

        :return:
        """

        _name = tkinter.filedialog.askopenfilename()
        if isinstance(_name, str):
            print(_('File selected for open saved game: ') + _name)
        else:
            print(_('No file selected'))

    def save_dialog(self):
        """
        Non-functional dialog indicating successful navigation.

        :return:
        """

        PopupDialog(self, _('Save button pressed- save board and game'), _('Not yet implemented'))

    def setup_dialog(self):
        """
        Non-functional dialog indicating successful navigation.

        :return:
        """

        PopupDialog(self, _('Setup button pressed'), _(f'state for setup: {self.master.board.setup_cells}'))
        self.master.board.setup_cells = not self.master.board.setup_cells

    def undo_dialog(self):
        """
        Non-functional dialog indicating successful navigation.

        :return:
        """

        PopupDialog(self, _('Undo button pressed'), _('Not yet implemented'))

    def redo_dialog(self):
        """
        Non-functional dialog indicating successful navigation.

        :return:
        """

        PopupDialog(self, _('Redo button pressed'), _('Not yet implemented'))

    def evaluate_dialog(self):
        """
        Non-functional dialog indicating successful navigation.

        :return:
        """

        PopupDialog(self, _('Evaluate button pressed'), _('Not yet implemented'))


class Application(tkinter.Tk):
    """
    Create top-level Tkinter widget containing all other widgets.

    """

    def __init__(self):
        tkinter.Tk.__init__(self)

        style = ttk.Style()
        style.configure("status.TLabel", font=('Helvetica', 20))
        # style.configure("status.TLabel", foreground="black", highlightcolor='red', background="white", font=('Helvetica', 20))
        style.configure("BW.TLabel", foreground="green", highlightcolor='red', background="black", height=200, bd=40, font=('Helvetica', 30))
        style.configure("BW.TButton", foreground="green", highlightcolor='red', background="black", height=200, bd=40, font=('Helvetica', 20))
        style.configure("f.BW.TLabel", foreground="magenta",  relief='raised')
        style.configure("selected.TLabel", foreground="magenta",  relief='raised')
        style.configure("block.TFrame", foreground="magenta", bd=20, bg='red',  relief='sunken', borderwidth=20)
        style.configure("active.block.TFrame", relief='raised')
        style.configure("BW.TFrame", foreground="blue", background="white", height=200, bd=10)
        style.configure('blue.TFrame', highlightbackground="red", highlightcolor="black", highlightthickness=10, width=1000,
                       height=300, bd=30, bg='black',)

        self.wm_title('Pushing Stones')
        self.wm_geometry('1500x2000')

        self.menubar = MenuBar(self)
        self.config(menu=self.menubar)

        self.statusbar = StatusBar(self)
        self.statusbar.pack(side='bottom', fill='x')
        # self.bind_all('<Enter>',
        #               lambda e: self.statusbar.set_text(0, 'Mouse: 1'))
        # self.bind_all('<Leave>',
        #               lambda e: self.statusbar.set_text(0, 'Mouse: 0'))
        # self.bind_all('<Button-1>',
        #               lambda e: self.statusbar.set_text(1, 'Clicked at x = ' + str(e.x) + ' y = ' + str(e.y)))
        self.start_time = datetime.datetime.now()
        # self.uptime()

        self.tool_bar = ToolBar(self)
        self.tool_bar.pack(side='top', fill='x')

        # self.board = Board(self, 0, 0)
        # self.board.pack(side='left', fill='y')

        self.main_frame = MainFrame(self)
        self.main_frame.pack(side='top', fill='y')

        self.board = Board(self, 0, 0)
        self.board.pack(side='left', fill='y')

        # select start player (black or white)
        self.board.set_player('white') # default to white

# Status bar selection == 'y'
    def uptime(self):
        _upseconds = str(int(round((datetime.datetime.now() - self.start_time).total_seconds())))
        # self.statusbar.set_text(2, _('Uptime') + ': ' + _upseconds)
        self.after(1000, self.uptime)

if __name__ == '__main__':
    APPLICATION_GUI = Application()
    APPLICATION_GUI.mainloop()
