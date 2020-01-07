
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# -*- coding: utf-8 -*-
"""
Test: pushingStones application
-------------------------------

Basic testing for Pushing Stones application
"""

import functools
from hamcrest import *
import pytest
import unittest

# import pushingStones
from application import Application


class TestBasicApplication(unittest.TestCase):
    """
    basic testing for Pushing Stones application

    Additional Tests:
        * Click on Home empty cell
        * Click on Home Other Color stone
        * Click on occupied dest cell
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

    def test_startup(self):
        """
        proper startup of application
        """
        assert_that(self.app.mainframe.display.cget('text'), starts_with('Cookiecutter: Open-Source Project Templates'))
        assert_that(self.app.mainframe.display.cget('text'), contains_string('pushing stones'))

    def test_click_button1(self):
        """
        Click button 1 at 46, 9
        Action of button 1 is completed
        :return:
        """
        self.simulate_mouse_click(self.app, 46, 9)
        assert_that(self.app.statusbar.labels[0].cget('text'), equal_to('Mouse: 1'))
        assert_that(self.app.statusbar.labels[1].cget('text'), equal_to('Clicked at x = 46 y = 9'))
        assert_that(self.app.statusbar.labels[2].cget('text'), equal_to('Uptime: 0'))
        assert_that(self.app.statusbar.labels[3].cget('text'), equal_to('Unset status 4'))

    def test_button1(self):
        """
        Invoke action of b1 button
        :return:
        """
        self.app.children['b1'].invoke()
        assert_that(self.app.statusbar.labels[0].cget('text'), equal_to('Unset status 1'))
        assert_that(self.app.statusbar.labels[1].cget('text'), equal_to('Unset status 2'))
        assert_that(self.app.statusbar.labels[2].cget('text'), equal_to('Uptime: 0'))
        assert_that(self.app.statusbar.labels[3].cget('text'), equal_to('Unset status 4'))

        pass

    def test_button2(self):
        """
        Invoke action of b2 button
        :return:
        """
        self.app.children['b2'].invoke()
        assert_that(self.app.statusbar.labels[0].cget('text'), equal_to('Unset status 1'))
        assert_that(self.app.statusbar.labels[1].cget('text'), equal_to('Unset status 2'))
        assert_that(self.app.statusbar.labels[2].cget('text'), equal_to('Uptime: 0'))
        assert_that(self.app.statusbar.labels[3].cget('text'), equal_to('Unset status 4'))
        pass

    def simulate_mouse_click(self, widget, x, y, buttonPress=1):
        """Generate proper events to click at the x, y position (tries to act
        like an X server)."""
        widget.event_generate('<Enter>', x=0, y=0)
        widget.event_generate('<Motion>', x=x, y=y)
        widget.event_generate(f'<ButtonPress-{buttonPress}>', x=x, y=y)
        widget.event_generate(f'<ButtonRelease-{buttonPress}>', x=x, y=y)

    def highlight_home_stone(self, home_block, attack_block, stone_cell, dest_cell):
        """
        Successful more of empty destination cell

        Assert:
            Home_block: stone_cell has stone

        Click Home stone

        Verify:
            Original Home_block/stone_cell is highlighted

        :param home_block:
        :param attack_block:
        :param stone_cell:
        :param dest_cell:
        :return:
        """
        pass

    def highlight_dest_cell(self, home_block, attack_block, stone_cell, dest_cell):
        """
        Assert:
            Home_block: stone_cell has stone

        Click Home stone
        Click Dest cell

        Verify:
            Original Home_block/stone_cell is highlighted
            Destination cell is highlighted

        :param home_block:
        :param attack_block:
        :param stone_cell:
        :param dest_cell:
        :return:
        """
        pass

    def highlight_attack_stone(self, home_block, attack_block, stone_cell, dest_cell):
        """
        Successful more of empty destination cell

        Assert:
            Home_block: stone_cell has stone
            Attack_block: stone_cell has stone

        Click Home stone
        Click Destination stone
        Click Attack stone

        Verify:
            Original Attack_block/stone_cell is highlighted

        :param home_block:
        :param attack_block:
        :param stone_cell:
        :param dest_cell:
        :return:
        """
        pass

    def move_home_attack_stones_one_cell(self, home_block, attack_block, stone_cell, dest_cell):
        """
        Successful more of empty destination cell

        Assert:
            Home_block: stone_cell has stone
            Attack_block: stone_cell has stone
            Both stones are same color

        Click Home stone and destination cell.
        Click Attack stone.
        Click Move

        Verify:
            Original Home_block/stone_cell is empty
            Original Attack_block/stone_cell is empty
            Home_block/dest_cell is stone of same color
            Attack_block/dest_cell is stone of same color

        :param home_block:
        :param attack_block:
        :param stone_cell:
        :param dest_cell:
        :return:
        """
        pass
