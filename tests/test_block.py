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

    def test_select_own_home_stone(self):
        """
        Select home stone of own color

        Verify:
            Cell for home stone is highlighted

        :return:
        """
        color = 'white'
        block_loc = BLOCK(0, 0)
        cell_loc = CELL(0, 0)
        verified = verify_cell_details(self.app, '', color, block_loc, cell_loc)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        select_results = select_stone(self.app, color, block_loc, cell_loc)
        assert_that(select_results, equal_to(''), f'select_cell failed: {select_results}')

        verified = verify_cell_details(self.app, 'selected.TLabel', color, block_loc, cell_loc)
        assert_that(verified, equal_to(''), f'cell not verified: {verified}')

        assert_that(statusbar_text(self.app), equal_to([f'{color}',
                                                        f'block {block_loc.column} {block_loc.row} {cell_loc.column} {cell_loc.row}',
                                                        f'white',
                                                        f''
                                                        ]))

        assert_that(statusbar_text(self.app, 0), equal_to(f'{color}'))
        assert_that(statusbar_text(self.app, 1), equal_to(f'block {block_loc.column} {block_loc.row} {cell_loc.column} {cell_loc.row}'))
        assert_that(statusbar_text(self.app, 2), equal_to(f'white'))
        assert_that(statusbar_text(self.app, 3), equal_to(f''))

    def test_select_empty_home_stone(self):
        """
        Select home stone of own color

        Verify:
            Cell for home stone is highlighted

        :return:
        """
        color = 'white'
        block_loc = BLOCK(0, 0)
        cell_loc = CELL(1, 0)
        verified = verify_cell_details(self.app, '', color, block_loc, cell_loc)
        assert_that(verified, starts_with('Cell not expected color'))

        select_results = select_stone(self.app, color, block_loc, cell_loc)
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
        cell_loc = CELL(3, 0)
        verified = verify_cell_details(self.app, '', color, block_loc, cell_loc)
        assert_that(verified, starts_with('Cell not expected color'))
        assert_that(verified, contains_string('black'))

        select_results = select_stone(self.app, color, block_loc, cell_loc)
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

    def test_stones_in_setup_board(self):
        """
        Set board conditions and check it is correct

        :return:
        """
        initial_white_stones = {
            '0,0': [CELL(1, 0), CELL(0, 1), CELL(0, 2), CELL(0, 3)],
            '0,1': [CELL(0, 0), CELL(2, 1), CELL(0, 2), CELL(0, 3)],
            '1,0': [CELL(0, 0), CELL(0, 1), None, CELL(0, 3)],
            '1,1': [CELL(0, 0), CELL(0, 1), CELL(0, 2), None]
        }
        initial_black_stones = {
            '0,0': [CELL(3, 0), CELL(3, 1), CELL(3, 2), None],
            '0,1': [CELL(3, 0), CELL(3, 1), CELL(2, 2), CELL(3, 3)],
            '1,0': [CELL(3, 0), CELL(1, 1), CELL(3, 2), CELL(3, 3)],
            '1,1': [None, CELL(3, 1), CELL(3, 2), CELL(3, 3)]
        }
        self.app.board_frame.set_board(initial_white_stones, initial_black_stones)

        errors = verify_cells(self.app, 'white', initial_white_stones)
        assert_that(errors, is_([]), f'missing white stones: {errors}')

        errors = verify_cells(self.app, 'black', initial_black_stones)
        assert_that(errors, is_([]), f'missing black stones: {errors}')

