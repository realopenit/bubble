# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from functools import wraps

from json import dumps

# THE memory
mem_cache = {}  # SortedDict()
mem_stats = {}  # SortedDict()


def get_memory():
    global mem_cache
    global mem_stats
    res = {'cache': mem_cache,
           'stats': mem_stats}
    return res


def set_memory(cache, stats):
    global mem_cache
    global mem_stats
    mem_cache = cache
    mem_stats = stats
    return None


def memoize(debug=False):
    def decoratr(fn):
        global mem_cache
        global mem_stats
        mem_cache[fn.__name__] = {}
        mem_stats[fn.__name__] = {}

        @wraps(fn)
        def wrapper(*a, **kw):
            global mem_cache
            global mem_stats
            key = dumps(*a, **kw)
            if key == '>>>stats>>>':
                return mem_stats[fn.__name__]
            if key == '>>>cache>>>':
                return mem_cache[fn.__name__]

            if key in mem_cache[fn.__name__]:
                mem_stats[fn.__name__]['counter_' + key] += 1

                return mem_cache[fn.__name__][key]

            mem_cache[fn.__name__][key] = fn(*a, **kw)
            mem_stats[fn.__name__]['counter_' + key] = 1
            return mem_cache[fn.__name__][key]

        wrapper.cache = mem_cache[fn.__name__]
        wrapper.stats = mem_stats[fn.__name__]
        wrapper.func = fn
        return wrapper
    return decoratr


if __name__ == '__main__':
    import arrow
    n = 200

    @memoize(False)
    def fibonl(n):
        if n > 1:
            return fibonl(n - 1) + fibonl(n - 2)
        else:
            return n

    s = arrow.now()
    print(fibonl(n))
    print(arrow.now() - s)
    print(fibonl.cache)

    # print(mem_cache)
    print(get_memory())
