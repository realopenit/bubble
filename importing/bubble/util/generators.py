# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.


"""store: for getting and putting files """
import arrow
import six

from .. import Bubble
from .flat_dict import flat
from .buts import buts


def make_gen(ctx=Bubble(), iterable=[], counter=None):
    ctx.gbc.say('make gen', stuff=iterable, verbosity=10)
    for item in iterable:
        if counter:
            counter.count()
        yield item


def make_stamping_gen(ctx=Bubble(), iterable=[], full_data=True, counter=None):
    ctx.gbc.say('make stamping gen', stuff=iterable, verbosity=10)

    for fat_item in iterable:
        item = flat(ctx, fat_item)
        ctx.gbc.say('stamping item:', stuff=item, verbosity=100)
        item[buts('storetimestamp')] = str(arrow.utcnow())
        item[buts('fulldata')] = full_data
        if counter:
            counter.count()
        yield item


def get_gen_slice(ctx=Bubble(), iterable=[], amount=-1, index=-1):
    """very crude way of slicing a generator"""
    ctx.gbc.say('get_gen_slice', stuff=iterable, verbosity=10)

    i = -1
    # TODO
    # i = 0 #NATURAL INDEX, this will break all features with exports and -p

    if amount > 0:
        if index < 0:
            index = 0
    else:
        for item in iterable:
            i += 1
            item[buts('index')] = i
            ctx.gbc.say('Get gen NO slice:item %d' % i, verbosity=100)
            ctx.gbc.say('Get gen NO slice:a:%d i:%d' %
                        (amount, index), verbosity=100)
            ctx.gbc.say('Get gen NO slice:item', stuff=item, verbosity=1000)
            yield item

    until = index + amount
    if six.PY2:
        sli = xrange(index, until)
    else:
        sli = range(index, until)

    ctx.gbc.say('Get gen slice:range %s' % str(sli), verbosity=1000)

    # TODO: iterable should be empty if not slicing
    # if valid slice ...
    for item in iterable:
        i += 1
        if i in sli:
            ctx.gbc.say('Get gen slice:item %d' % i, verbosity=100)
            ctx.gbc.say('Get gen slice:a:%d i:%d' %
                        (amount, index), verbosity=100)
            ctx.gbc.say('Get gen slice:item', stuff=item, verbosity=1000)
            item[buts('index')] = i
            yield item
        elif i > until:
            break
        else:
            pass
