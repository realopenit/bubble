# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.


import six
import inspect
from functools import wraps

from .. import Bubble

"""
TODO: make a triage:
http://en.wikipedia.org/wiki/Mission_critical
As a rule in crisis management, if a triage-type decision is made in which certain
components must be eliminated or delayed, e.g. because of resource or personnel constraints,
the mission critical ones must not be among them.

http://en.wikipedia.org/wiki/Triage
"""

_try_options = {'count_it': False,
                'print_it': True,
                'print_args': True,
                'inspect_it': False,
                'log_it': True,
                'reraise_it': False,
                'logger': None,
                'ctx': None
                }


def set_try_option(ctx, key, value):
    ctx.gbc.say('set_try_option(%s,%s)' % (str(key), str(value)))
    global _try_options
    ctx.gbc.say('set_try_option:k:%senv,v:%s' % (key, value),
                stuff=_try_options, verbosity=200)
    if key not in _try_options:
        pass
        # raise ... no such option

    if _try_options[key] == value:
        # no change
        return
    # update
    _try_options[key] = value
    ctx.gbc.say('try option:%s to %s' % (key, str(value)), verbosity=50)


def get_try_option(ctx, key):
    global _try_options
    if ctx:
        ctx.gbc.say('get try option:options:',
                    stuff=_try_options, verbosity=50)
    else:
        print('get try option:options:' + str(_try_options))

    ret = _try_options[key]
    if ctx:
        ctx.gbc.say('get try option:%s: %s' % (key, str(ret)), verbosity=50)
    else:
        print('get try option:%s: %s' % (key, str(ret)))
    return ret


def inside_try(func, options={}):
    """ decorator to silence exceptions, for logging
        we want a "safe" fail of the functions """
    if six.PY2:
        name = func.func_name
    else:
        name = func.__name__

    @wraps(func)
    def silenceit(*args, **kwargs):
        """ the function func to be silenced is wrapped inside a
        try catch and returned, exceptions are logged
        exceptions are returned in an error dict
        takes all kinds of arguments and passes to the original func
        """
        excpt = None
        try:
            return func(*args, **kwargs)
        # pylint: disable=W0703
        # inside_try.silenceit: Catching too general exception Exception
        # that's the idea!
        except Exception as excpt:
            # first tell the object in charge
            if 'ctx' in kwargs:
                ctx = kwargs['ctx']
            else:
                # otherwise tell object defined in options
                # if we can be sure there is a context
                ctx = get_try_option(None, 'ctx')

            if not ctx:
                # tell a new object
                ctx = Bubble('Inside Try')
                # ctx.set_verbose(100); #todo: move to magic

            head = name + ': silenced function inside_try:Error:'
            if get_try_option(ctx, 'count_it'):
                ctx.gbc.cry(head + 'counting')
            if get_try_option(ctx, 'print_it'):
                ctx.gbc.cry(head + 'printing:' + str(excpt))
            if get_try_option(ctx, 'print_args'):
                ctx.gbc.cry(head + 'printing ak:' + str(excpt))
                ctx.gbc.cry('args', stuff=args)
                ctx.gbc.cry('kwargs', stuff=kwargs)
            if get_try_option(ctx, 'inspect_it'):
                ctx.gbc.cry(head + 'inspecting:', stuff=excpt)
                for s in inspect.stack():
                    ctx.gbc.cry(head + ':stack:', stuff=s)
            if get_try_option(ctx, 'log_it'):
                ctx.gbc.cry(head + 'logging')
                for s in inspect.stack():
                    ctx.gbc.cry(head + ':stack:', stuff=s)
            if get_try_option(ctx, 'reraise_it'):
                ctx.gbc.cry(head + 'reraising')
                raise excpt
            # always return error
            return {'error': str(excpt),
                    'silenced': name,
                    'args': args,
                    'kwargs': kwargs}
    return silenceit

if __name__ == '__main__':
    @inside_try
    def erring(*a, **k):
        return 1 / 0
    erring()
    print('setting option print it')
    set_try_option(Bubble(), 'print_it', True)
    print(get_try_option(Bubble(), 'print_it'))
    erring()
    print('setting option inspect it')
    set_try_option(Bubble(), 'inspect_it', True)
    # print(get_try_option('inspect_it'))
    erring()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
