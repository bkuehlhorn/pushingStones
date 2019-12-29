
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# -*- coding: utf-8 -*-
# test_clickinvoke.py


import unittest

# import pushingStones
from application import Application


class TestClickInvoke(unittest.TestCase):
    def setUp(self):
        self.app = Application()

    def tearDown(self):
        self.app.destroy()

    def test_button1(self):
        self.app.children['b1'].invoke()
        pass

    def test_button2(self):
        self.app.children['b2'].invoke()