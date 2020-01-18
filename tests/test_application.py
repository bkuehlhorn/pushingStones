
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# -*- coding: utf-8 -*-
"""
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
    --------------------------------------------------------------
    basic testing for Pushing Stones application

    Additional Tests:
        * Application startup

    """
    def setUp(self):
        self.app = Application()

    def tearDown(self):
        self.app.destroy()

    def test_startup(self):
        """
        proper startup of application
        """
        assert_that(self.app.main_frame.display.cget('text'), starts_with('Cookiecutter: Open-Source Project Templates'))
        assert_that(self.app.main_frame.display.cget('text'), contains_string('pushing stones'))

    def test_click_button1(self):
        """
        Click button 1 at 46, 9
        Action of button 1 is completed
        :return:
        """
        self.simulate_mouse_click(self.app, 46, 9)
        # assert_that(self.app.statusbar.labels[0].cget('text'), equal_to('Mouse: 1'))
        # assert_that(self.app.statusbar.labels[1].cget('text'), equal_to('Clicked at x = 46 y = 9'))
        # assert_that(self.app.statusbar.labels[2].cget('text'), equal_to('Uptime: 0'))
        # assert_that(self.app.statusbar.labels[3].cget('text'), equal_to('Unset status 4'))

    def test_button1(self):
        """
        Invoke action of b1 button
        :return:
        """
        self.app.main_frame.children['b1'].invoke()
        # assert_that(self.app.statusbar.labels[0].cget('text'), equal_to('Unset status 1'))
        # assert_that(self.app.statusbar.labels[1].cget('text'), equal_to('Unset status 2'))
        # assert_that(self.app.statusbar.labels[2].cget('text'), equal_to('Uptime: 0'))
        # assert_that(self.app.statusbar.labels[3].cget('text'), equal_to('Unset status 4'))

        pass

    def test_button2(self):
        """
        Invoke action of b2 button
        :return:
        """
        self.app.main_frame.children['b2'].invoke()
        # assert_that(self.app.statusbar.labels[0].cget('text'), equal_to('Unset status 1'))
        # assert_that(self.app.statusbar.labels[1].cget('text'), equal_to('Unset status 2'))
        # assert_that(self.app.statusbar.labels[2].cget('text'), equal_to('Uptime: 0'))
        # assert_that(self.app.statusbar.labels[3].cget('text'), equal_to('Unset status 4'))
        pass

    def simulate_mouse_click(self, widget, x, y, buttonPress=1):
        """Generate proper events to click at the x, y position (tries to act
        like an X server)."""
        widget.event_generate('<Enter>', x=0, y=0)
        widget.event_generate('<Motion>', x=x, y=y)
        widget.event_generate(f'<ButtonPress-{buttonPress}>', x=x, y=y)
        widget.event_generate(f'<ButtonRelease-{buttonPress}>', x=x, y=y)


class TestFileMenu(unittest.TestCase):
    """
    test menu functions
    --------------------------------------------------------------

    test menu functions

    Additional Tests:

        **File Menu:**

        * Test New game
        * Open
        * Save
        * Exit - maybe

        **Play Menu:**

        * Undo
        * Redo
        * Evaluate
        * Setup

        **Help Menu: maybe**

        * Help
        * About

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
        # self.app.
        assert_that(self.app.main_frame.display.cget('text'), starts_with('Cookiecutter: Open-Source Project Templates'))
        assert_that(self.app.main_frame.display.cget('text'), contains_string('pushing stones'))
