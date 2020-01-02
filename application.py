"""
pushingStones application
-----------------

Pushing Stones: game to push 2 stones off one of 2x2 blocks with 4x4 cells and 4 stones of each color on blocks
"""

import datetime
import gettext
from PIL import Image, ImageTk
import sys
import time
import tkinter
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename

# All translations provided for illustrative purposes only.
 # english
_ = lambda s: s
__ = lambda s: ' '.join(s)



class PopupDialog(ttk.Frame):
    '''
    Sample popup dialog implemented to provide feedback.

    '''

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
    '''
    Sample status bar provided by cookiecutter switch.

    '''
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
    '''
    Sample toolbar provided by cookiecutter switch.

    '''

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
        "Sample function provided to show how a toolbar command may be used."

        print(_('Toolbar button'), number, _('pressed'))
        self.master.mainframe.tick(f'Toolbar {number} clicked')



class MainFrame(ttk.Frame):
    '''
    Main area of user interface content.

    '''

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


class Board(ttk.Frame):
    '''
    Row of 16 black capture cells
    Row of 16 white capture cells
    2x2 blocks of 4x4 cells for stones
    Home: movement, Attach movement (movement: block: x,y, direction, cells moved)
    Move button (enabled when Home and Attack are set)
    '''
    image_size = 75

    def __init__(self, parent, x, y):
        ttk.Frame.__init__(self, parent)
        self.capture_black = []
        self.capture_white = []
        self.blocks = [[''] * 2] * 2

        self.empty_cell = self.make_image('image/emptycell.png')
        self.white_image = self.make_image('image/whiteStone.png')
        self.black_image = self.make_image('image/blackStone.png')

        self.capture_black = self.set_capture_stones(self.empty_cell, row=0, column=0)
        self.capture_white = self.set_capture_stones(self.empty_cell, row=0, column=6)
        self.set_capture_stones(self.empty_cell, row=8, column=0)
        self.set_capture_stones(self.empty_cell, row=8, column=6)

        # test capturing stones
        # self.capture_white[1].configure(image=self.white_image)
        # self.capture_white[2].configure(image=self.white_image)
        # self.capture_black[0].configure(image=self.black_image)
        # self.capture_black[4].configure(image=self.black_image)

        for x in range(2):
            for y in range(2):
                block = Block(self, self.black_image, self.white_image, self.empty_cell, 0, 0)
                block.grid(row=x*9+3, column=y*5, columnspan=6)
                # block.grid(row=row, column=y*2)
                self.blocks[x][y] = block
        # render black and white origin stones

        self.move_button = tkinter.Button(self, text=f'make move', name=f'make move', command=self.click1)
        self.move_button.grid(row=13, column=5)
        pass

    def click1(self):
        pass

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
        '''
        add border around home blocks for player

        :param player:
        :return:
        '''

    def highlight_attack_blocks(self, home_block):
        '''
        add border around attack blocks using home_block

        :param home_block:
        :return:
        '''

    def click_move(self):
        '''
        update blocks and capture if push off block
        render blocks and capture stones
        :return:
        '''


class Block(ttk.Frame):
    '''
    Block of 4x4 cells
    Render buttons for cells starting a x, y of parent.
    '''
    def __init__(self, parent, black_stone, white_stone, empty_cell, x=0, y=0):
        ttk.Frame.__init__(self, parent)
        button_size = 20
        # create
        self.cells = []
        for bx in range(4):
            row_cells = []
            for by in range(4):
                cell = tkinter.Button(self, image=empty_cell, text=f'Cell {bx}:{by}', name=f'{bx}:{by}', command=self.click1)
                cell.grid(row=bx, column=by)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def click1(self):
        pass


class MenuBar(tkinter.Menu):
    '''
    Menu bar appearing with expected components.

    '''

    def __init__(self, parent):
        '''
        “File(new, open, save, resign, close) Game Options: Play: undo, redo, evaluate”

        Excerpt From: Bernard Kuehlhorn. “Pushing Stones Application.” Apple Books.
        '''
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
        '''
        Ends toplevel execution.

        :return:
        '''

        sys.exit(0)

    def help_dialog(self, event):
        '''
        Dialog cataloging results achievable, and provided means available.

        :param event:
        :return:
        '''

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
        '''
        Dialog concerning information about entities responsible for program.

        :return:
        '''

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
        '''
        Non-functional dialog indicating successful navigation.

        :return:
        '''

        PopupDialog(self, _('New button pressed'), _('Not yet implemented'))

    def open_dialog(self):
        '''
        Standard askopenfilename() invocation and result handling.

        :return:
        '''

        _name = tkinter.filedialog.askopenfilename()
        if isinstance(_name, str):
            print(_('File selected for open: ') + _name)
        else:
            print(_('No file selected'))

    def save_dialog(self):
        '''
        Non-functional dialog indicating successful navigation.

        :return:
        '''

        PopupDialog(self, _('Save button pressed'), _('Not yet implemented'))

    def undo_dialog(self):
        '''
        Non-functional dialog indicating successful navigation.

        :return:
        '''

        PopupDialog(self, _('Undo button pressed'), _('Not yet implemented'))

    def redo_dialog(self):
        '''
        Non-functional dialog indicating successful navigation.

        :return:
        '''

        PopupDialog(self, _('Redo button pressed'), _('Not yet implemented'))

    def evaluate_dialog(self):
        '''
        Non-functional dialog indicating successful navigation.

        :return:
        '''

        PopupDialog(self, _('Evaluate button pressed'), _('Not yet implemented'))


class Application(tkinter.Tk):
    '''
    Create top-level Tkinter widget containing all other widgets.

    '''

    def __init__(self):
        tkinter.Tk.__init__(self)
        menubar = MenuBar(self)
        self.config(menu=menubar)
        self.wm_title('pushing stones')
        self.wm_geometry('640x480')

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
        self.toolbar = ToolBar(self)
        self.toolbar.pack(side='top', fill='x')

        # self.mainframe = MainFrame(self)
        # self.mainframe.pack(side='left') #, fill='y')
        self.boardframe = Board(self, 0, 0)
        self.boardframe.pack(side='left', fill='y')

# Status bar selection == 'y'
    def uptime(self):
        _upseconds = str(int(round((datetime.datetime.now() - self.start_time).total_seconds())))
        self.statusbar.set_text(2, _('Uptime') + ': ' + _upseconds)
        self.after(1000, self.uptime)


if __name__ == '__main__':
    APPLICATION_GUI = Application()
    APPLICATION_GUI.mainloop()
