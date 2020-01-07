"""
pushingStones application
--------------------------

Pushing Stones: game to push 2 stones off one of 2x2 blocks with 4x4 cells and 4 stones of each color on blocks


"""

from collections import namedtuple
import datetime
import gettext
from functools import partial
from PIL import Image, ImageTk
import sys
import time
import tkinter
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename

CELL = namedtuple('CELL', 'row, column')
DIRECTION = namedtuple('DIRECTION', 'rowDelta, columnDelta')
MOVE_STONE = namedtuple('MOVE_STONE', 'board, row, column, direction, distance')
MOVE_STONES = namedtuple('MOVE_STONES', 'home_move, attack_move')


def Move_stone(board, from_cell, to_cell):
    """
    calculate direction and distance for from and to cells

    :param board: 
    :param from_cell: 
    :param to_cell: 
    :return: 
    """
    rowDelta = from_cell.row - to_cell.row
    columnDelta = from_cell.column - to_cell.column
    direction = DIRECTION(rowDelta, columnDelta)
    distance = max(abs(direction.rowDelta), abs(direction.columnDelta))
    return MOVE_STONE(board, from_cell, direction, distance)


def Set_home_move(move_stone):
    """
    Create MOVE_STONES for column with 
    :param move_stone: of stone to move
    :return MOVE_STONE: Half move for home block 
    """
    return MOVE_STONES(move_stone, None)


def Add_attack_move(move_stones, attack_move):
    """
    Add attack_move to move_stones
    
    :param move_stones: 
    :param attack_move: Cell on attach board to move
    :return MOVE_STONE: complete move for home and attack blocks
    """
    return MOVE_STONES(move_stones.home_move, attack_move)

# All translations provided for illustrative purposes only.
# english
_ = lambda s: s
__ = lambda s: ' '.join(s)



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
        self.boardframe = Board(self, 0, 0)
        self.boardframe.pack(side='left') #, fill='y')

        self.display = ttk.Label(parent, anchor=tkinter.CENTER, name='label',
                                 foreground='green', background='black')
        self.display.pack(fill=tkinter.BOTH, expand=1)

        self.display = ttk.Label(parent, anchor=tkinter.CENTER, name='label',
                                 foreground='green', background='black')
        self.display.pack(fill=tkinter.BOTH, expand=1)

        self.tick()
        self.b1 = ttk.Button(text='Button 1', name='b1', command=self.click1)
        self.b1.pack(side='left')
        self.b2 = ttk.Button(text='Button 2', name='b2', command=self.click2)
        self.b2.pack(side='left')

    def click1(self):
        print('Button 1 clicked.')
        self.master.mainframe.tick('Button 1 clicked')

    def click2(self):
        print('Button 2 clicked.')
        self.b1.invoke()
        self.master.mainframe.tick('Button 2 clicked')

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
    Row of 16 black capture cells
    Row of 16 white capture cells
    2x2 blocks of 4x4 cells for stones
    Home: movement, Attach movement (movement: block: x,y, direction, cells moved)
    Move button (enabled when Home and Attack are set)

    Design:
        Render: board, blocks, cells and cell button
        Highlight: Home Blocks, Attack Blocks, Origin Cell, Destination Cell

        Click cell button:
            if home origin cell is empty
                if cell is same color:
                    highlight cell,
                    save column and row for original home block,
                    action is home destination cell
                else:
                    report error
            else if home origin cell is not empty
                if distance is more than 2 or pushes a stone:
                    report error, highlight cells, action is home destination cell
                else:
                    highlight cell,
                    save column and row for destination home block,
                    action is attack origin cell
            else if home origin cell is not empty and attack origin cell is empty:
                if cell is same color:
                    highlight cell,
                    save column and row for destination home block,
                    action is attack destination cell
                else:
                    report error
            else if attack origin cell is not empty:
                if distance is not equal to home distance or pushes 2 stones:
                    report error, highlight cells, action is home destination cell
                else:
                    highlight cell,
                    save column and row for destination home block,
                    action is attack origin cell

    """
    image_size = 75
    player = 'white' # color of current player

    def __init__(self, parent, x, y):
        # ttk.Frame.__init__(self, parent)
        super().__init__(parent) # create a frame (self)

        self.vsb = ttk.Scrollbar(parent, orient='vertical', command=self.yview)
        self.hsb = ttk.Scrollbar(parent, orient='horizontal', command=self.xview)
        self.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        # self.grid(column=0, row=0, sticky='nsew', in_=parent)
        # vsb.grid(column=1, row=0, sticky='ns', in_=parent)
        # hsb.grid(column=0, row=1, sticky='ew', in_=parent)
        self.vsb.pack()
        self.hsb.pack()

        # self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.yview)  # place a scrollbar on self
        # self.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas
        # self.vsb.pack(side="right", fill="y")
        # self.config(bd=10, bg='blue')
        self.capture_count = {'black': 0, 'white': 0}
        self.capture_black = []
        self.capture_white = []
        self.blocks = [[0,1],[2,3]]

        self.images = dict(empty=self.make_image('image/emptycell.png'),
                           black=self.make_image('image/blackStone.png'),
                           white=self.make_image('image/whiteStone.png'))
        self.white_image = self.make_image('image/whiteStone.png')
        self.black_image = self.make_image('image/blackStone.png')

        self.captured_stones = {'black': self.set_capture_stones(self.images['empty'], row=0, column=0),
                                'white': self.set_capture_stones(self.images['empty'], row=0, column=6)}
        self.set_capture_stones(self.images['empty'], row=8, column=0)
        self.set_capture_stones(self.images['empty'], row=8, column=6)

        for x in range(2):
            for y in range(2):
                block = Block(self, x, y, self.images, 0, 0)
                block.grid(row=x*9+3, column=y*6, columnspan=6)
                self.blocks[x][y] = block

        # render black and white origin stones
        for i in range(2):
            for j in range(2):
                for column in range(4):
                    self.blocks[i][j].cells[0][column].set_cell('white')
                    self.blocks[i][j].cells[3][column].set_cell('black')

        self.move_button = tkinter.Button(self, text=f'make move', name=f'make move', command=self.click1)
        self.move_button.grid(row=13, column=5)

        self.from_cell = None  # CELL
        self.home_move = None  # MOVE_STONE
        self.attack_move = None  # MOVE_STONE
        pass

    def set_cell(self, block_column, block_row, cell_column, cell_row, color):
        """

        :param block_column:
        :param block_row:
        :param cell_column:
        :param cell_row:
        :param color:
        :return:
        """
        self.blocks[block_column][block_row].cells[cell_column][cell_row].set_cell(color)

    def click1(self):
        """
        hold method for clicking cell

        :return:
        """
        return True

    def capture(self, stone, board):
        """
        Add to captured stones
        Count stones captured from each board by color

        :param stone: color of captured stone
        :param board: x, y of board for captured stone
        :return: false: game continue, true: game over
        """
        self.captured_stones[stone][self.capture_count[stone]].configure(image=self.images[stone])
        self.capture_count[stone] += 1
        # count


    def make_image(self, png):
        photo = Image.open(png)
        return ImageTk.PhotoImage(photo.resize((self.image_size, self.image_size)))

    def set_capture_stones(self, image, row, column):
        capture_cells = []
        for each in range(5):
            capture = tkinter.Label(self, image=image)
            capture.grid(row=row, column=each+column)
            capture_cells.append(capture)
        return capture_cells

    def highlight_home_blocks(self, player):
        """
        add border around home blocks for player

        :param player:
        :return:
        """
        pass

    def highlight_attack_blocks(self, home_block):
        """
        add border around attack blocks using home_block

        :param home_block:
        :return:
        """
        pass

    def click_move(self):
        """
        update blocks and capture if push off block
        render blocks and capture stones
        :return:
        """
        pass


class Block(ttk.Frame):
    """
    Block of 4x4 cells
    Render buttons for cells starting a x, y of parent.
    """
    def __init__(self, parent, block_x, block_y, images, x=0, y=0):
        ttk.Frame.__init__(self, parent)
        self.cell_image = images

        button_size = 20
        # create
        self.cells = []
        for cell_x in range(4):
            row_cells = []
            for cell_y in range(4):
                cell = Cell(self, color='empty', name=f'{cell_x}:{cell_y}')
                cell.grid(row=cell_x, column=cell_y)
                row_cells.append(cell)
            self.cells.append(row_cells)
        pass

    def set_cell(self, x, y, stone):
        """
        set image and text for cell
        :param x: column of cell
        :param y: row of cell
        :param stone: black, white, or empty
        :return:
        """
        image = self.cell_image[stone]
        self.cells[x][y].configure(image=image, text=stone)

    def in_cell(self, x, y, color):
        """

        :param color:
        :return: true if is, false if not
        """
        return self.cells[x][y].cget('text') == color


    def select_stone(self, block_x, block_y, x, y):
        """
        First click:
            clear highlights
            Has player stone: false: ignore click
            select stone to move
            highlight cell: green

        Second click:
            destination cell
            if legal move from first cell to cell: highlight destination cell: green
            else: status error, highlight destination cell: red

        :return:
        """
        self.cells[x][y].config(relief=tkinter.SUNKEN)
        pass


class Cell(ttk.Frame):
    """
    Button where stones are placed and moved.

    """
    def __init__(self, parent, color, *args, **kwargs):
        """
        Block, images and location for cell
        :param parent: block
        :param color: black, white, empty
        :param x: column
        :param y: row
        """
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        image = self.master.cell_image[color]
        # ttk.Frame.__init__(self, parent, highlightbackground="green", highlightcolor="black", highlightthickness=10, *args, **kwargs)
        # cell = Cell(self, image=self.cell_image['empty'], text='empty', name=f'{cell_x}:{cell_y}',
        #             command=partial(self.select_stone, block_x, block_y, cell_x, cell_y))
        self.button = CellButton(parent, *args, image=image, text=color, command=partial (self.select_stone), **kwargs)
        # cell.pack()

        # self.cell_image = images

    def set_cell(self, stone):
        """
        :param stone: black, white, or empty
        :return:
        """
        image = self.master.cell_image[stone]
        self.button.configure(image=image, text=stone)

    def select_stone(self):
        """
        First click:
            clear highlights
            Has player stone: false: ignore click
            select stone to move
            highlight cell: green

        Second click:
            destination cell
            if legal move from first cell to cell: highlight destination cell: green
            else: status error, highlight destination cell: red

        :return:
        """
        s = ttk.Style()
        s.configure('Select.TButton', font='helvetica 24', foreground='red', padding=10)
        # self['style'] = 'Select.TButton'
        # s.theme_use('classic')
        self['style'] = 'selected.TLabel' if self['style'] is '' else ''
        self.master['style'] = 'block.TFrame' if self.master['style'] is '' else ''
        # self.config(relief=tkinter.SUNKEN , style="f.BW.TLabel")
        # self.config(style="f.BW.TLabel")
        pass


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
        filemenu.add_command(label=_('New'), command=self.new_dialog)
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

        PopupDialog(self, _('New button pressed'), _('Not yet implemented'))

    def open_dialog(self):
        """
        Standard askopenfilename() invocation and result handling.

        :return:
        """

        _name = tkinter.filedialog.askopenfilename()
        if isinstance(_name, str):
            print(_('File selected for open: ') + _name)
        else:
            print(_('No file selected'))

    def save_dialog(self):
        """
        Non-functional dialog indicating successful navigation.

        :return:
        """

        PopupDialog(self, _('Save button pressed'), _('Not yet implemented'))

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
        # style.configure("BW.TLabel", foreground="magenta", highlightcolor='red', background="white", height=200, bd=20, relief='raised', font='Times')
        style.configure("BW.TLabel", foreground="green", highlightcolor='red', background="black", height=200, bd=40, font=('Helvetica', 30))
        style.configure("f.BW.TLabel", foreground="magenta",  relief='raised')
        style.configure("selected.TLabel", foreground="magenta",  relief='raised')
        style.configure("block.TFrame", foreground="magenta", bd=2, bg='red',  relief='raised')
        style.configure("BW.TFrame", foreground="blue", background="white", height=200, bd=10)
        style.configure('blue.TFrame', highlightbackground="red", highlightcolor="black", highlightthickness=10, width=1000,
                       height=300, bd=30, bg='black',)

        self.wm_title('Pushing Stones')
        self.wm_geometry('1000x2000')

        # self.l1 = ttk.Label(text="Test this stuff", style="BW.TLabel")
        # self.l2 = ttk.Label(text="Test", style="BW.TLabel")
        # # self.l2 = ttk.Label(text="Test2")
        # self.l1.pack()
        # self.l2.pack()

        # self.frame1 = ttk.Frame(self, style='blue.TFrame')
        # self.frame1 = ttk.LabelFrame(self, style='blue.TFrame')
        # self.frame1 = ttk.Frame(self)
        # self.frame1 = tkinter.Frame(self, highlightbackground="green", highlightcolor="black", highlightthickness=10, width=7000,
        #                height=100, bd=10, bg='blue')

        # self.l1s = ttk.Label(self.frame1, text="Test this stuff", style="BW.TLabel")
        # self.l2s = ttk.Label(self.frame1, text="Test Frame", style="f.BW.TLabel")
        # # self.l2 = ttk.Label(text="Test2")
        # self.l1s.pack()
        # self.l2s.pack()
        # self.frame1.pack()
        #
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # xscrollbar = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL)
        # # xscrollbar.grid(row=1, column=0, sticky=tkinter.E + tkinter.W)
        #
        # yscrollbar = tkinter.Scrollbar(self)
        # yscrollbar.grid(row=0, column=1, sticky=tkinter.N + tkinter.S)

        # self.canvas = tkinter.Canvas(self, bd=0,
        #                 xscrollcommand=xscrollbar.set,
        #                 yscrollcommand=yscrollbar.set)
        # self.canvas = tkinter.Frame(self)
        #
        # # canvas.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        #
        # # xscrollbar.config(command=self.canvas.xview)
        # # yscrollbar.config(command=self.canvas.yview)
        #
        # self.l1sc = ttk.Label(self.canvas, text="Canvas Test this stuff", style="BW.TLabel")
        # self.l2sc = ttk.Label(self.canvas, text="Canvas Test Frame", style="f.BW.TLabel")
        # # self.l2 = ttk.Label(text="Test2")
        # self.l1sc.pack()
        # self.l2sc.pack()
        # self.pack()

        menubar = MenuBar(self)
        self.config(menu=menubar)

        # Status bar selection == 'y'
        self.statusbar = StatusBar(self)
        self.statusbar.pack(side='bottom', fill='x')
        self.bind_all('<Enter>',
                      lambda e: self.statusbar.set_text(0, 'Mouse: 1'))
        self.bind_all('<Leave>',
                      lambda e: self.statusbar.set_text(0, 'Mouse: 0'))
        self.bind_all('<Button-1>',
                      lambda e: self.statusbar.set_text(1, 'Clicked at x = ' + str(e.x) + ' y = ' + str(e.y)))
        self.start_time = datetime.datetime.now()
        self.uptime()

# Tool bar selection == 'y'

#         self.scrollbar = tkinter.Scrollbar(self)
#         self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
#
#         self.listbox = tkinter.Listbox(self, bd=0, yscrollcommand=self.scrollbar.set)
#         self.listbox.pack()
#
#         self.scrollbar.config(command=self.listbox.yview)

        self.tool_bar = ToolBar(self)
        self.tool_bar.pack(side='top', fill='x')

        # self.mainframe = MainFrame(self)
        # self.mainframe.pack(side='left') #, fill='y')
        # self.scrollbar = ttk.Scrollbar(self)
        self.board_frame = Board(self, 0, 0)
        # self.board_frame = Board(self, 0, 0, yscrollcommand=self.scrollbar.set)
        # self.scrollbar.config(command=self.selected_files.yview)

        # self.xscrollbar = ttk.Scrollbar(self, orient=tkinter.HORIZONTAL)
        # # self.xscrollbar.grid(row=1, column=0, sticky=tkinter.E + tkinter.W)
        #
        # self.yscrollbar = ttk.Scrollbar(self)
        # # self.yscrollbar.grid(row=0, column=1, sticky=tkinter.N + tkinter.S)
        #
        # self.board_frame = Board(self, 0, 0, bd=0,
        #                 xscrollcommand=self.xscrollbar.set,
        #                 yscrollcommand=self.yscrollbar.set)
        #
        # self.board_frame.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        #
        # self.xscrollbar.config(command=self.board_frame.xview)
        # self.yscrollbar.config(command=self.board_frame.yview)

        self.board_frame.pack(side='left', fill='y')

# Status bar selection == 'y'
    def uptime(self):
        _upseconds = str(int(round((datetime.datetime.now() - self.start_time).total_seconds())))
        self.statusbar.set_text(2, _('Uptime') + ': ' + _upseconds)
        self.after(1000, self.uptime)


if __name__ == '__main__':
    APPLICATION_GUI = Application()
    APPLICATION_GUI.mainloop()
