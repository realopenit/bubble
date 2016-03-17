# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.


from .. import Bubble


class Counter(Bubble):

    def __init__(self):
        self._count = 0

    def count(self):
        self._count += 1
        self.say('Current counter:%d' % self._count, verbosity=100)

    def get_total(self):
        return self._count
