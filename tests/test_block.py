# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# -*- coding: utf-8 -*-
"""
Test: pushingStones block
-------------------------------

Basic testing for Pushing Stones block
"""

import functools
from hamcrest import *
import pytest
import unittest

# import pushingStones
# from application import Application, VALID_BLOCK, VALID_CELL, BLOCK, CELL
from tests import *


class TestStartApp(unittest.TestCase):
    """
    basic testing for Pushing Stones application

    Additional Tests:
        * Home cell moves one or two cells and pushes one Other Color stone - failure to move

    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param dest_cell: int: [0-3, 0-3]

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
        block_styles = self.app.board_frame.get_block_style()
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
        self.app.board_frame.set_board(initial_white_stones, initial_black_stones)

        errors = verify_cells(self.app, 'white', initial_white_stones)
        assert_that(errors, is_([]), f'missing white stones: {errors}')

        errors = verify_cells(self.app, 'black', initial_black_stones)
        assert_that(errors, is_([]), f'missing black stones: {errors}')


class TestSelectingHomeStones(unittest.TestCase):
    """
    basic testing for Pushing Stones application

    Additional Tests:
        * Home cell moves one or two cells and pushes one Other Color stone - failure to move

    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param dest_cell: int: [0-3, 0-3]

    """

    def setUp(self):
        self.app = Application()

    def tearDown(self):
        self.app.destroy()

    def test_select_own_home_stone(self):
        """
        Select home stone of own color

        Verify:
            Cell for home stone is highlighted

        :return:
        """
        color = 'white'
        block_loc = BLOCK(0, 0)
        home_stone = CELL(block_loc, 0, 0)
        verified = verify_cell_details(self.app, '', color, home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        select_results = select_cell(self.app, color, home_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')

        verified = verify_cell_details(self.app, 'selected.TLabel', color, home_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{color}',
                                                        cell_status(home_stone),
                                                        f'white',
                                                        f'Please select destination cell'
                                                        ]))

        assert_that(statusbar_text(self.app, 0), equal_to(f'{color}'))
        assert_that(statusbar_text(self.app, 1), equal_to(f'block {block_loc.column} {block_loc.row} {home_stone.column} {home_stone.row}'))
        assert_that(statusbar_text(self.app, 2), equal_to(f'white'))
        assert_that(statusbar_text(self.app, 3), equal_to(f'Please select destination cell'))

    def test_select_empty_home_stone(self):
        """
        Select home stone of own color

        Verify:
            Cell for home stone is highlighted

        :return:
        """
        color = 'white'
        block_loc = BLOCK(0, 0)
        # home_stone = CELL(block_loc, 1, 0)
        home_stone = CELL(block_loc, 0, 1)
        verified = verify_cell_details(self.app, '', color, home_stone)
        assert_that(verified, starts_with('Cell not expected color'))

        select_results = select_cell(self.app, color, home_stone)
        assert_that(select_results, equal_to(f'Cell not expected color: expected: {color}, actual: empty'), f'select_cell failed: {select_results}')
        assert_that(verified, contains_string('empty'))

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
        Select home stone of own color

        Verify:
            Cell for home stone is highlighted

        :return:
        """
        color = 'white'
        block_loc = BLOCK(0, 0)
        home_stone = CELL(block_loc, 0, 3)
        verified = verify_cell_details(self.app, '', color, home_stone)
        assert_that(verified, starts_with('Cell not expected color'))
        assert_that(verified, contains_string('black'))

        select_results = select_cell(self.app, color, home_stone)
        assert_that(select_results, equal_to(f'Cell not expected color: expected: {color}, actual: black'), f'select_cell failed: {select_results}')

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
    basic testing for Pushing Stones application

    Additional Tests:
        * Destination cell 

    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param dest_cell: int: [0-3, 0-3]

    """

    def setUp(self):
        self.app = Application()

    def tearDown(self):
        self.app.destroy()

    def init(self, color, home_block, home_stone, dest_cell, attack_block, attack_cell):
        self.color = color
        self.home_block_loc = BLOCK(*home_block)
        self.attack_block_loc = BLOCK(*attack_block)
        self.home_stone = CELL(self.home_block_loc, *home_stone)
        self.dest_cell = CELL(self.home_block_loc, *dest_cell)
        self.attack_stone = CELL(self.attack_block_loc, *attack_cell)
        self.find_home_cell = find_cell(self.app, self.home_stone)
        self.find_dest_cell = find_cell(self.app, self.dest_cell)
        self.find_attack_cell = find_cell(self.app, self.attack_stone)
        verify_cell_details(self.app, '', self.color, self.home_stone)
        select_cell(self.app, self.color, self.home_stone)


    def test_select_home_destination_cell_valid_1(self):
        """
        Select home cell as destination cell on home board

        Verify:
            Cell for home stone is highlighted

        :return:
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  dest_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, 'empty', self.dest_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'empty', self.dest_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')
        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.dest_cell),
                                                        f'empty',
                                                        f'Please select stone to move on attack blocks'
                                                        ]))

    def test_select_home_destination_cell_valid_2(self):
        """


        Verify:
            Cell for home stone is highlighted

        :return:
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  dest_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, 'empty', self.dest_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'empty', self.dest_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.dest_cell),
                                                        f'empty',
                                                        f'Please select stone to move on attack blocks'
                                                        ]))

    def test_select_home_destination_cell_valid_3(self):
        """


        Verify:
            Cell for home stone is highlighted

        :return:
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  dest_cell=(0, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, 'empty', self.dest_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'empty', self.dest_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.dest_cell),
                                                        f'empty',
                                                        f'Please select stone to move on attack blocks'
                                                        ]))

    def test_select_home_destination_cell_invalid(self):
        """


        Verify:
            Cell for home stone is highlighted

        :return:
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  dest_cell=(2, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_results = select_cell(self.app, 'empty', self.dest_cell)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, '', 'empty', self.dest_cell)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.dest_cell),
                                                        f'empty',
                                                        f'Please cell closer to stone to move'
                                                        ]))

class TestSelectingStones(unittest.TestCase):
    """
    basic testing for Pushing Stones application

    Additional Tests:
        * Home cell moves one or two cells and pushes one Other Color stone - failure to move
        * Attack cell moves one cell and pushes one Other Color stone to another cell
        * Attack cell moves two cells and pushes one Other Color stone in first cell to another cell
        * Attack cell moves two cells and pushes one Other Color stone in second cell to another cell
        * Attack cell moves one cell and pushes one other Color stone off board (one or two cells)
        * Attack cell moves stone of same color (moves one or two cells) - failure to move (check)
        * Attack cell moves more than one stone - failure to move

    Common Parameters (change parameters to namedtuple)

    :param home_block: int: [0-1, 0-1]
    :param attack_block: int: [0-1, 0-1]
    :param stone_cell: int: [0-3, 0-3]
    :param dest_cell: int: [0-3, 0-3]

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
        self.app.board_frame.set_board(self.initial_white_stones, self.initial_black_stones)

    def tearDown(self):
        self.app.destroy()

    def init(self, color, home_block, home_stone, dest_cell, attack_block, attack_cell):
        self.color = color
        self.home_block_loc = BLOCK(*home_block)
        self.attack_block_loc = BLOCK(*attack_block)
        self.home_stone = CELL(self.home_block_loc, *home_stone)
        self.dest_cell = CELL(self.home_block_loc, *dest_cell)
        self.attack_stone = CELL(self.attack_block_loc, *attack_cell)
        self.find_home_cell = find_cell(self.app, self.home_stone)
        self.find_dest_cell = find_cell(self.app, self.dest_cell)
        self.find_attack_cell = find_cell(self.app, self.attack_stone)
        verify_cell_details(self.app, '', self.color, self.home_stone)
        select_cell(self.app, self.color, self.home_stone)
        
    def test_select_attack_cell_valid(self):
        """


        Verify:
            Cell for self.home stone is highlighted

        :return:
        """
        self.init(color='white',
                  home_block=(0, 0),
                  home_stone=(0, 0),
                  dest_cell=(1, 1),
                  attack_block=(1, 0),
                  attack_cell=(0, 0))

        select_cell(self.app, 'empty', self.dest_cell)
        select_results = select_cell(self.app, self.color, self.attack_stone)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')
        verified = verify_cell_details(self.app, 'selected.TLabel', 'white', self.attack_stone)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{self.color}',
                                                        cell_status(self.attack_stone),
                                                        f'tbd',
                                                        f'Hit make move when done'
                                                        ]))

