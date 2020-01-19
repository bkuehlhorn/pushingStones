# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# -*- coding: utf-8 -*-
"""
Basic testing for Pushing Stones block
"""

import functools
from hamcrest import *
import pytest
import unittest

# import pushingStones
from application import Application, VALID_BLOCK, VALID_CELL, BLOCK, CELL, DIRECTION
from tests import *


class TestStartApp(unittest.TestCase):
    """
    basic testing for Pushing Stones application

    Additional Tests:
        * Init blocks with captured stones

    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param destination_cell: int: [0-3, 0-3]

    """

    def setUp(self):
        self.app = Application()

    def tearDown(self):
        self.app.destroy()

    def test_white_stones_start(self):
        """
        Initial setup with White stones active

        Verify:
            White home blocks active
            Black home blocks inactive

        :return:
        """
        initial_block_styles = [
            ['active.block.TFrame', 'block.TFrame'],
            ['active.block.TFrame', 'block.TFrame'],
        ]
        block_styles = self.app.board.get_block_style()
        assert_that(block_styles, equal_to(initial_block_styles))

    def test_stones_in_setup_board(self):
        """
        Set board conditions and check it is correct

        :return:
        """
        # initial_white_stones = {
        #     '0,0': [CELL(BLOCK(0,0), 0, 0), CELL(BLOCK(0,0), 0, 1), CELL(BLOCK(0,0), 0, 2), CELL(BLOCK(0,0), 0, 3)],
        #     '0,1': [CELL(BLOCK(0,1), 0, 0), CELL(BLOCK(0,1), 0, 1), CELL(BLOCK(0,1), 0, 2), CELL(BLOCK(0,1), 0, 3)],
        #     '1,0': [CELL(BLOCK(1,0), 0, 0), CELL(BLOCK(1,0), 0, 1), CELL(BLOCK(1,0), 0, 2), CELL(BLOCK(1,0), 0, 3)],
        #     '1,1': [CELL(BLOCK(0,1), 0, 0), CELL(BLOCK(1,1), 0, 1), CELL(BLOCK(1,1), 0, 2), CELL(BLOCK(1,1), 0, 3)]
        # }
        # initial_black_stones = {
        #     '0,0': [CELL(BLOCK(0,0), 3, 0), CELL(BLOCK(0,0), 3, 1), CELL(BLOCK(0,0), 3, 2), CELL(BLOCK(0,0), 3, 3)],
        #     '0,1': [CELL(BLOCK(0,1), 3, 0), CELL(BLOCK(0,1), 3, 1), CELL(BLOCK(0,1), 3, 2), CELL(BLOCK(0,1), 3, 3)],
        #     '1,0': [CELL(BLOCK(1,0), 3, 0), CELL(BLOCK(1,0), 3, 1), CELL(BLOCK(1,0), 3, 2), CELL(BLOCK(1,0), 3, 3)],
        #     '1,1': [CELL(BLOCK(0,1), 3, 0), CELL(BLOCK(1,1), 3, 1), CELL(BLOCK(1,1), 3, 2), CELL(BLOCK(1,1), 3, 3)]
        # }
        initial_white_stones = {
            '0,0': [CELL(BLOCK(0,0), 1, 0), CELL(BLOCK(0,0), 0, 1), CELL(BLOCK(0,0), 0, 2), CELL(BLOCK(0,0), 0, 3)],
            '0,1': [CELL(BLOCK(0,1), 0, 0), CELL(BLOCK(0,1), 2, 1), CELL(BLOCK(0,1), 0, 2), CELL(BLOCK(0,1), 0, 3)],
            '1,0': [CELL(BLOCK(1,0), 0, 0), CELL(BLOCK(1,0), 0, 1), None, CELL(BLOCK(1,0), 0, 3)],
            '1,1': [CELL(BLOCK(1,1), 0, 0), CELL(BLOCK(1,1), 0, 1), CELL(BLOCK(1,1), 0, 2), None]
        }
        initial_black_stones = {
            '0,0': [CELL(BLOCK(0,0), 3, 0), CELL(BLOCK(0,0), 3, 1), CELL(BLOCK(0,0), 3, 2), None],
            '0,1': [CELL(BLOCK(0,1), 3, 0), CELL(BLOCK(0,1), 3, 1), CELL(BLOCK(0,1), 2, 2), CELL(BLOCK(0,1), 3, 3)],
            '1,0': [CELL(BLOCK(1,0), 3, 0), CELL(BLOCK(1,0), 1, 1), CELL(BLOCK(1,0), 3, 2), CELL(BLOCK(1,0), 3, 3)],
            '1,1': [None, CELL(BLOCK(1,1), 3, 1), CELL(BLOCK(1,1), 3, 2), CELL(BLOCK(1,1), 3, 3)]
        }
        self.app.board.set_board(initial_white_stones, initial_black_stones)

        errors = verify_cells(self.app, 'white', initial_white_stones)
        assert_that(errors, is_([]), f'missing white stones: {errors}')

        errors = verify_cells(self.app, 'black', initial_black_stones)
        assert_that(errors, is_([]), f'missing black stones: {errors}')


class TestSelectingHomeStones(unittest.TestCase):
    """
    basic testing for Pushing Stones application

    Additional Tests:
        * Home cell moves one or two cells and pushes one Other Color stone - failure to move
        * Reset move after selecting Home cell
        * Clear home cell

    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param destination_cell: int: [0-3, 0-3]

    """

    def setUp(self):
        self.app = Application()

    def tearDown(self):
        self.app.destroy()

    def init(self, color, home_block, home_stone, destination_cell, attack_block, attack_cell):
        self.color = color
        self.home_block_loc = BLOCK(*home_block)
        self.attack_block_loc = BLOCK(*attack_block)
        self.home_stone = CELL(self.home_block_loc, *home_stone)
        self.destination_cell = CELL(self.home_block_loc, *destination_cell)
        self.attack_stone = CELL(self.attack_block_loc, *attack_cell)
        self.find_home_cell = find_cell(self.app, self.home_stone)
        self.find_destination_cell = find_cell(self.app, self.destination_cell)
        self.find_attack_cell = find_cell(self.app, self.attack_stone)

    def test_select_own_home_stone(self):
        """
        Verify:
            Cell for home stone is highlighted
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        verified = verify_cell_details(self.app, '', self.color, self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        select_results = select_cell(self.app, self.color, self.home_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')

        verified = verify_cell_details(self.app, 'selected.TLabel', self.color, self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.home_stone),
                                                        f'white',
                                                        f'Please select destination cell'
                                                        ]))

        assert_that(statusbar_text(self.app, 0), equal_to(f'{self.color}'))
        assert_that(statusbar_text(self.app, 1), equal_to(f'block {self.home_block_loc.column} {self.home_block_loc.row} {self.home_stone.column} {self.home_stone.row}'))
        assert_that(statusbar_text(self.app, 2), equal_to(f'white'))
        assert_that(statusbar_text(self.app, 3), equal_to(f'Please select destination cell'))

    def test_select_clear_home_stone(self):
        """
        Select home stone of own color
        Select second time

        Verify:
            Cell for home stone is normal
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        verify_cell_details(self.app, '', self.color, self.home_stone)
        select_cell(self.app, self.color, self.home_stone)

        select_results = select_cell(self.app, self.color, self.home_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')

        verified = verify_cell_details(self.app, '', self.color, self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.home_stone),
                                                        f'white',
                                                        f'Select home stone'
                                                        ]))

        assert_that(statusbar_text(self.app, 0), equal_to(f'{self.color}'))
        assert_that(statusbar_text(self.app, 1), equal_to(f'block {self.home_block_loc.column} {self.home_block_loc.row} {self.home_stone.column} {self.home_stone.row}'))
        assert_that(statusbar_text(self.app, 2), equal_to(f'white'))
        assert_that(statusbar_text(self.app, 3), equal_to(f'Select home stone'))

    def test_select_empty_home_stone(self):
        """
        Verify:
            Status report invalid selection
        """
        self.init(color='white',
                  home_block=(0, 0),
                  # home_stone=(0, 1), # empty cell
                  home_stone=(0, 3), # black stone
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))
        # error_color = 'empty'
        error_color = 'black'

        verified = verify_cell_details(self.app, '', self.color, self.home_stone)
        assert_that(verified, starts_with('Cell not expected color'))

        select_results = select_cell(self.app, self.color, self. home_stone)
        assert_that(select_results, equal_to(f'Cell not expected color: expected: {self.color}, actual: {error_color}'), f'select_cell failed: {select_results}')
        assert_that(verified, contains_string(error_color))

        assert_that(statusbar_text(self.app), equal_to([f'Unset status 1',
                                                        f'Unset status 2',
                                                        f'Unset status 3',
                                                        f'Unset status 4'
                                                        ]))

        assert_that(statusbar_text(self.app, 0), equal_to(f'Unset status 1'))
        assert_that(statusbar_text(self.app, 1), equal_to(f'Unset status 2'))
        assert_that(statusbar_text(self.app, 2), equal_to(f'Unset status 3'))
        assert_that(statusbar_text(self.app, 3), equal_to(f'Unset status 4'))

    def test_select_other_home_stone(self):
        """
        Verify:
            Status report invalid selection
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 3),
                  # self. home_stone=(1, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        verified = verify_cell_details(self.app, '', self.color, self. home_stone)
        assert_that(verified, starts_with('Cell not expected color'))
        assert_that(verified, contains_string('black'))

        select_results = select_cell(self.app, self.color, self.home_stone)
        assert_that(select_results, equal_to(f'Cell not expected color: expected: {self.color}, actual: black'), f'select_cell failed: {select_results}')

        assert_that(statusbar_text(self.app), equal_to([f'Unset status 1',
                                                        f'Unset status 2',
                                                        f'Unset status 3',
                                                        f'Unset status 4'
                                                        ]))

        assert_that(statusbar_text(self.app, 0), equal_to(f'Unset status 1'))
        assert_that(statusbar_text(self.app, 1), equal_to(f'Unset status 2'))
        assert_that(statusbar_text(self.app, 2), equal_to(f'Unset status 3'))
        assert_that(statusbar_text(self.app, 3), equal_to(f'Unset status 4'))


class TestSelectingDestinationCell(unittest.TestCase):
    """
    Test selecting destination cell:
        * Reset move after selecting Home cell

    Additional Tests:
        * Destination cell 

    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param destination_cell: int: [0-3, 0-3]

    """

    def setUp(self):
        self.app = Application()

    def tearDown(self):
        self.app.destroy()

    def init(self, color, home_block, home_stone, destination_cell, attack_block, attack_cell):
        self.color = color
        self.home_block_loc = BLOCK(*home_block)
        self.attack_block_loc = BLOCK(*attack_block)
        self.home_stone = CELL(self.home_block_loc, *home_stone)
        self.destination_cell = CELL(self.home_block_loc, *destination_cell)
        self.attack_stone = CELL(self.attack_block_loc, *attack_cell)
        self.find_home_cell = find_cell(self.app, self.home_stone)
        self.find_destination_cell = find_cell(self.app, self.destination_cell)
        self.find_attack_cell = find_cell(self.app, self.attack_stone)
        verify_cell_details(self.app, '', self.color, self.home_stone)
        select_cell(self.app, self.color, self.home_stone)

    def test_valid_move_one_cell(self):
        """
        Verify:
            Cell for destination cell is highlighted
            Clear highlights for home blocks
            Highlight attack blocks
            Status: select attack stone
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, 'empty', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'empty', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'empty',
                                                        f'Please select stone to move on attack blocks'
                                                        ]))

    def test_valid_move_two_cells(self):
        """
        Destination is 2 cells away
        Verify:
            Cell for destination cell is highlighted
            Clear highlights for home blocks
            Highlight attack blocks
            Status: select attack stone
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 2),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, 'empty', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'empty', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'empty',
                                                        f'Please select stone to move on attack blocks'
                                                        ]))

    def test_pushing_other_stone_one_cell(self):
        """
            Move other stone next to home stone to move
            Select home stone
            Select destination cell to move other stone

        Verify:
        """
        home_block = BLOCK(0, 0)
        from_cell = find_cell(self.app, CELL(home_block, 0, 3))
        to_cell = find_cell(self.app, CELL(home_block, 1, 1))
        self.app.board.blocks[0][0].move_stone(from_cell, to_cell)

        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, 'empty', self.destination_cell)

        select_results = select_cell(self.app, 'black', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', 'black', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'black',
                                                        f'Please select an empty cell'
                                                        ]))

    def test_pushing_other_stone_two_cell(self):
        """
            Move other stone next to home stone to move
            Select home stone
            Select destination cell to move other stone

        Verify:
        """
        home_block = BLOCK(0, 0)
        from_cell = find_cell(self.app, CELL(home_block, 0, 3))
        to_cell = find_cell(self.app, CELL(home_block, 1, 1))
        self.app.board.blocks[0][0].move_stone(from_cell, to_cell)

        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 2),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, 'empty', self.destination_cell)

        select_results = select_cell(self.app, 'black', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', 'black', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'black',
                                                        f'Please select an empty cell'
                                                        ]))

    def test_pushing_other_stone_two_cell(self):
        """
            Move other stone next to home stone to move
            Select home stone
            Select destination cell to move other stone

        Verify:
        """
        home_block = BLOCK(0, 0)
        from_cell = find_cell(self.app, CELL(home_block, 0, 3))
        to_cell = find_cell(self.app, CELL(home_block, 2, 2))
        self.app.board.blocks[0][0].move_stone(from_cell, to_cell)

        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 2),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, 'empty', self.destination_cell)

        select_results = select_cell(self.app, 'black', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', 'black', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'black',
                                                        f'Please select an empty cell'
                                                        ]))

    def test_destination_cell_cleared(self):
        """
        Select destination cell on home board second time to clear

        Verify:
            Cell for home stone is normal
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, 'empty', self.destination_cell)

        select_results = select_cell(self.app, 'empty', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', 'empty', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'empty',
                                                        f'Select destination cell'
                                                        ]))

    def test_home_stone_cleared(self):
        """
        Select home cell on home board second time to clear

        Verify:
            Destination cell is normal
            Cell for home stone is normal
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, 'empty', self.destination_cell)

        select_results = select_cell(self.app, self.color, self.home_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', self.color, self.home_stone)
        verified = verify_cell_details(self.app, '', 'empty', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'empty',
                                                        f'Select home stone'
                                                        ]))

    def test_invalid(self):
        """
        Select destination more that 2 cell away

        Verify:
            Status reports select destination cell
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, 'empty', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', 'empty', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'empty',
                                                        f'Please cell closer to stone to move'
                                                        ]))

    def test_select_home_destination_cell_invalid(self):
        """
        Verify:
            Cell for home stone is highlighted
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, 'empty', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', 'empty', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.destination_cell),
                                                        f'empty',
                                                        f'Please cell closer to stone to move'
                                                        ]))


class TestSelectingAttackStone(unittest.TestCase):
    """
    Select home stone and dest cell to test different Attack stone selection

    Additional Tests:
        * Select empty cell for attack stone
        * Select other stone for attack stone
        * Pushes one other stone
        * Pushes two other stone
        * Pushes one same stone
        * Moves off board one cell
        * Moves off board two cells
        * Pushes one other stone off block by one cell
        * Pushes one other stone off block by two cells
        * Reset move after selecting attack cell
        * Reset move after selecting destination cell
        * Reset move after selecting home cell


    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param destination_cell: int: [0-3, 0-3]

    """
    initial_white_stones = {
        '0,0': [CELL(BLOCK(0,0), 0, 0), CELL(BLOCK(0,0), 0, 1), CELL(BLOCK(0,0), 0, 2), CELL(BLOCK(0,0), 0, 3)],
        '0,1': [CELL(BLOCK(0,1), 0, 0), CELL(BLOCK(0,1), 0, 1), CELL(BLOCK(0,1), 0, 2), CELL(BLOCK(0,1), 0, 3)],
        '1,0': [CELL(BLOCK(1,0), 0, 0), CELL(BLOCK(1,0), 0, 1), CELL(BLOCK(1,0), 0, 2), CELL(BLOCK(1,0), 0, 3)],
        '1,1': [CELL(BLOCK(0,1), 0, 0), CELL(BLOCK(1,1), 0, 1), CELL(BLOCK(1,1), 0, 2), CELL(BLOCK(1,1), 0, 3)]
    }
    initial_black_stones = {
        '0,0': [CELL(BLOCK(0,0), 3, 0), CELL(BLOCK(0,0), 3, 1), CELL(BLOCK(0,0), 3, 2), CELL(BLOCK(0,0), 3, 3)],
        '0,1': [CELL(BLOCK(0,1), 3, 0), CELL(BLOCK(0,1), 3, 1), CELL(BLOCK(0,1), 3, 2), CELL(BLOCK(0,1), 3, 3)],
        '1,0': [CELL(BLOCK(1,0), 3, 0), CELL(BLOCK(1,0), 3, 1), CELL(BLOCK(1,0), 3, 2), CELL(BLOCK(1,0), 3, 3)],
        '1,1': [CELL(BLOCK(0,1), 3, 0), CELL(BLOCK(1,1), 3, 1), CELL(BLOCK(1,1), 3, 2), CELL(BLOCK(1,1), 3, 3)]
    }
    
    captured_white_stones = {
        '0,0': [CELL(BLOCK(0,0), 1, 0), CELL(BLOCK(0,0), 0, 1), CELL(BLOCK(0,0), 0, 2), CELL(BLOCK(0,0), 0, 3)],
        '0,1': [CELL(BLOCK(0,1), 0, 0), CELL(BLOCK(0,1), 2, 1), CELL(BLOCK(0,1), 0, 2), CELL(BLOCK(0,1), 0, 3)],
        '1,0': [CELL(BLOCK(1,0), 0, 0), CELL(BLOCK(1,0), 0, 1), None, CELL(BLOCK(1,0), 0, 3)],
        '1,1': [CELL(BLOCK(1,1), 0, 0), CELL(BLOCK(1,1), 0, 1), CELL(BLOCK(1,1), 0, 2), None]
    }
    captuerd_black_stones = {
        '0,0': [CELL(BLOCK(0,0), 3, 0), CELL(BLOCK(0,0), 3, 1), CELL(BLOCK(0,0), 3, 2), None],
        '0,1': [CELL(BLOCK(0,1), 3, 0), CELL(BLOCK(0,1), 3, 1), CELL(BLOCK(0,1), 2, 2), CELL(BLOCK(0,1), 3, 3)],
        '1,0': [CELL(BLOCK(1,0), 3, 0), CELL(BLOCK(1,0), 1, 1), CELL(BLOCK(1,0), 3, 2), CELL(BLOCK(1,0), 3, 3)],
        '1,1': [None, CELL(BLOCK(1,1), 3, 1), CELL(BLOCK(1,1), 3, 2), CELL(BLOCK(1,1), 3, 3)]
    }

    def setUp(self):
        self.app = Application()
        # self.app.board.init_board()
        # self.app.board.set_board(self.captured_white_stones, self.captuerd_black_stones)

    def tearDown(self):
        self.app.destroy()

    def init(self, color, home_block, home_stone, destination_cell, attack_block, attack_cell):
        self.color = color
        self.home_block_loc = BLOCK(*home_block)
        self.attack_block_loc = BLOCK(*attack_block)
        self.home_stone = CELL(self.home_block_loc, *home_stone)
        self.destination_cell = CELL(self.home_block_loc, *destination_cell)
        self.attack_stone = CELL(self.attack_block_loc, *attack_cell)
        direction = DIRECTION(self.destination_cell.column - self.home_stone.column,
                              self.destination_cell.row - self.home_stone.row
                              )
        attack_destination_column = self.attack_stone.column + direction.column_delta
        attack_destination_row = self.attack_stone.row + direction.row_delta
        self.attack_destination_cell =  CELL(self.attack_block_loc, attack_destination_column, attack_destination_row)
        if not VALID_CELL(self.attack_destination_cell):
            self.attack_destination_cell = None

        self.find_home_cell = find_cell(self.app, self.home_stone)
        self.find_destination_cell = find_cell(self.app, self.destination_cell)
        self.find_attack_cell = find_cell(self.app, self.attack_stone)
        verify_cell_details(self.app, '', self.color, self.home_stone)
        select_cell(self.app, self.color, self.home_stone)
        select_cell(self.app, 'empty', self.destination_cell)

    def test_valid(self):
        """
        Verify:
            Cell for self.attack stone is highlighted
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, self.color, self.attack_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'white', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        # destination cell on attack board highlighted

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.attack_stone),
                                                        f'tbd',
                                                        f'Hit make move when done'
                                                        ]))
        if self.attack_destination_cell is not None:
            verified = verify_cell_details(self.app, 'selected.TLabel', None, self.attack_destination_cell)
            assert_that(verified, equal_to(''), f'cell not verified: {verified}')


    def test_to_edge(self):
        """
        Select attack stone near edge. Distance from edge.

        Verify:
            Cell for self.attack stone is highlighted
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 2),
                  attack_block=(1, 0),
                  attack_cell=(1, 0))

        select_results = select_cell(self.app, self.color, self.attack_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'white', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        # destination cell on attack board highlighted

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.attack_stone),
                                                        f'tbd',
                                                        f'Hit make move when done'
                                                        ]))
        if self.attack_destination_cell is not None:
            verified = verify_cell_details(self.app, 'selected.TLabel', None, self.attack_destination_cell)
            assert_that(verified, equal_to(''), f'cell not verified: {verified}')


    def test_double_move_off_edge(self):
        """
        Select attack stone near edge. Double move will be off block.

        Verify:
            Status reports invalid attack stone selected
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 2),
                  attack_block=(1, 0),
                  attack_cell=(2, 0))

        select_results = select_cell(self.app, self.color, self.attack_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'white', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        # destination cell on attack board highlighted

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.attack_stone),
                                                        f'white',
                                                        f'Attack Destination cell invalid'
                                                        ]))

    def test_move_off(self):
        """
        Select attack cell at edge. Move will be off block
        Verify:
            Status reports invalid attack stone selected
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(3, 0))

        select_results = select_cell(self.app, self.color, self.attack_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'white', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        # destination cell on attack board highlighted

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.attack_stone),
                                                        f'white',
                                                        f'Attack Destination cell invalid'
                                                        ]))

    def test_clear_attack_cell(self):
        """
        Click attack cell twice
        Verify:
            Status reports select attack stone
            Clear attack cells
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, self.color, self.attack_stone)

        select_results = select_cell(self.app, self.color, self.attack_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', 'white', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        # destination cell on attack board normal
        if self.attack_destination_cell is not None:
            verified = verify_cell_details(self.app, '', None, self.attack_destination_cell)
            assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.attack_stone),
                                                        f'tbd',
                                                        f'Select attack cell'
                                                        ]))

    def test_clear_destination_cell(self):
        """
        Click destination cell after selecting attack stone

        Verify:
            Status reports select destination cell
            Clear attack and destination  cells
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, self.color, self.attack_stone)

        select_results = select_cell(self.app, 'empty', self.destination_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', self.color, self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', 'empty', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        # destination cell on attack board normal

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.attack_stone),
                                                        f'tbd',
                                                        f'Select destination cell'
                                                        ]))

    def test_clear_home_cell(self):
        """
        Click home ston after selecting attack stone

        Verify:
            Status reports select home cell
            Clear attack, destination and home cells
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, self.color, self.attack_stone)

        select_results = select_cell(self.app, self.color, self.home_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', self.color, self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', 'empty', self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        # destination cell on attack board normal

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.attack_stone),
                                                        f'tbd',
                                                        f'Select home stone'
                                                        ]))


class TestMoveWhiteStone(unittest.TestCase):
    """
    Test moving white stone

    Additional Tests:
        * move white single distance
        * move white double distance
        * move white single distance black move
        * move white double distance black next to white
        * move white double distance black distance one from white
        * move white capture black on edge single distance
        * move white capture black on edge double distance
        * move white capture black next to edge double distance


    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param destination_cell: int: [0-3, 0-3]

    """
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

    captured_white_stones = {
        '0,0': [CELL(BLOCK(0, 0), 1, 0), CELL(BLOCK(0, 0), 0, 1), CELL(BLOCK(0, 0), 0, 2), CELL(BLOCK(0, 0), 0, 3)],
        '0,1': [CELL(BLOCK(0, 1), 0, 0), CELL(BLOCK(0, 1), 2, 1), CELL(BLOCK(0, 1), 0, 2), CELL(BLOCK(0, 1), 0, 3)],
        '1,0': [CELL(BLOCK(1, 0), 0, 0), CELL(BLOCK(1, 0), 0, 1), None, CELL(BLOCK(1, 0), 0, 3)],
        '1,1': [CELL(BLOCK(1, 1), 0, 0), CELL(BLOCK(1, 1), 0, 1), CELL(BLOCK(1, 1), 0, 2), None]
    }
    captuerd_black_stones = {
        '0,0': [CELL(BLOCK(0, 0), 3, 0), CELL(BLOCK(0, 0), 3, 1), CELL(BLOCK(0, 0), 3, 2), None],
        '0,1': [CELL(BLOCK(0, 1), 3, 0), CELL(BLOCK(0, 1), 3, 1), CELL(BLOCK(0, 1), 2, 2), CELL(BLOCK(0, 1), 3, 3)],
        '1,0': [CELL(BLOCK(1, 0), 3, 0), CELL(BLOCK(1, 0), 1, 1), CELL(BLOCK(1, 0), 3, 2), CELL(BLOCK(1, 0), 3, 3)],
        '1,1': [None, CELL(BLOCK(1, 1), 3, 1), CELL(BLOCK(1, 1), 3, 2), CELL(BLOCK(1, 1), 3, 3)]
    }

    def setUp(self):
        self.app = Application()
        # self.app.board_frame.init_board()
        # self.app.board_frame.set_board(self.captured_white_stones, self.captuerd_black_stones)

    def tearDown(self):
        self.app.destroy()

    def init(self, color, home_block, home_stone, destination_cell, attack_block, attack_cell):
        self.color = color
        self.home_block_loc = BLOCK(*home_block)
        self.attack_block_loc = BLOCK(*attack_block)
        self.home_stone = CELL(self.home_block_loc, *home_stone)
        self.destination_cell = CELL(self.home_block_loc, *destination_cell)
        self.attack_stone = CELL(self.attack_block_loc, *attack_cell)
        direction = DIRECTION(self.destination_cell.column - self.home_stone.column,
                              self.destination_cell.row - self.home_stone.row
                              )
        attack_destination_column = self.attack_stone.column + direction.column_delta
        attack_destination_row = self.attack_stone.row + direction.row_delta
        self.attack_destination_cell =  CELL(self.attack_block_loc, attack_destination_column, attack_destination_row)
        if not VALID_CELL(self.attack_destination_cell):
            self.attack_destination_cell = None

        self.find_home_cell = find_cell(self.app, self.home_stone)
        self.find_destination_cell = find_cell(self.app, self.destination_cell)
        self.find_attack_cell = find_cell(self.app, self.attack_stone)
        self.find_attack_destination_cell = find_cell(self.app, self.attack_destination_cell)
        verify_cell_details(self.app, '', self.color, self.home_stone)
        select_cell(self.app, self.color, self.home_stone)
        select_cell(self.app, 'empty', self.destination_cell)
        select_cell(self.app, self.color, self.attack_stone)

    def test_white_single_distance(self):
        """

        :return:
        """
        attack_block = BLOCK(1, 0)
        from_cell = find_cell(self.app, CELL(attack_block, 3, 3))
        to_cell = find_cell(self.app, CELL(attack_block, 1, 1))
        push_cell = find_cell(self.app, CELL(attack_block, 2, 2))
        # self.app.board.blocks[1][0].move_stone(from_cell, to_cell)

        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        self.app.board.make_moves()
        verified = verify_cell_details(self.app, '', 'empty', self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        verified = verify_cell_details(self.app, '', 'empty', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.attack_destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', 'empty', push_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        #todo check history for move

        pass

    def test_white_single_distance_push(self):
        """

        :return:
        """
        attack_block = BLOCK(1, 0)
        from_cell = find_cell(self.app, CELL(attack_block, 3, 3))
        to_cell = find_cell(self.app, CELL(attack_block, 1, 1))
        push_cell = find_cell(self.app, CELL(attack_block, 2, 2))
        self.app.board.blocks[1][0].move_stone(from_cell, to_cell)

        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        self.app.board.make_moves()
        verified = verify_cell_details(self.app, '', 'empty', self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        verified = verify_cell_details(self.app, '', 'empty', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.attack_destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.app.board.other_stone[self.color], push_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        #todo check history for move

        pass

    def test_white_double_distance(self):
        """

        :return:
        """
        attack_block = BLOCK(1, 0)
        from_cell = find_cell(self.app, CELL(attack_block, 3, 3))
        to_cell = find_cell(self.app, CELL(attack_block, 2, 2))
        push_cell = find_cell(self.app, CELL(attack_block, 3, 3))
        # self.app.board.blocks[1][0].move_stone(from_cell, to_cell)

        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 2),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        self.app.board.make_moves()
        verified = verify_cell_details(self.app, '', 'empty', self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        verified = verify_cell_details(self.app, '', 'empty', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.attack_destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.app.board.other_stone[self.color], push_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        #todo check history for move

        pass

    def test_white_double_distance_push(self):
        """

        :return:
        """
        attack_block = BLOCK(1, 0)
        from_cell = find_cell(self.app, CELL(attack_block, 3, 3))
        to_cell = find_cell(self.app, CELL(attack_block, 1, 1))
        push_cell = find_cell(self.app, CELL(attack_block, 3, 3))
        self.app.board.blocks[1][0].move_stone(from_cell, to_cell)

        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 2),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        self.app.board.make_moves()
        verified = verify_cell_details(self.app, '', 'empty', self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        verified = verify_cell_details(self.app, '', 'empty', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.attack_destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.app.board.other_stone[self.color], push_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        #todo check history for move

    def test_white_double_distance_push_two(self):
        """
        Move black cell from 3, 3 to 2, 2
        Move white 0, 0 to 1, 1
        Check empty in 0, 0
        Check white in 1, 1
        Check
        """
        attack_block = BLOCK(1, 0)
        from_cell = find_cell(self.app, CELL(attack_block, 3, 3))
        to_cell = find_cell(self.app, CELL(attack_block, 2, 2))
        push_cell = find_cell(self.app, CELL(attack_block, 3, 3))
        self.app.board.blocks[1][0].move_stone(from_cell, to_cell)

        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  destination_cell=(2, 2),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        self.app.board.make_moves()
        verified = verify_cell_details(self.app, '', 'empty', self.home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        verified = verify_cell_details(self.app, '', 'empty', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.color, self.attack_destination_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        verified = verify_cell_details(self.app, '', self.app.board.other_stone[self.color], push_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        # todo check history for move

