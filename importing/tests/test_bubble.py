#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_bubble
----------------------------------

Tests for `bubble` module.
"""

import unittest

from bubble import Bubble


class TestBubble(unittest.TestCase):

    def setUp(self):
        self.bubble=Bubble() 

    def test_something(self):
        self.bubble.say('hi from first test case')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
