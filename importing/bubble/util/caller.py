# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import inspect

# TODO move to configuration, options
CFG_UTIL_INSPECT_STACK = True
CFG_UTIL_INSPECT_STACK_DEBUG = False
CFG_UTIL_STACK_GET_LINE_NOT = ['get_caller_line',
                               '_msg',
                               '_say_color',
                               'say',
                               'gbc_say',
                               'say_green',
                               'say_yellow',
                               'say_yellow']


# todo: add ctx, and test very well, watch out for recursions!!
# def get_caller_line(ctx, stack_pos=2):

def get_caller_line(stack_pos=2):
    if not CFG_UTIL_INSPECT_STACK:
        return 'INSPECT_STACK=False'
    try:
        c = inspect.stack()
        if CFG_UTIL_INSPECT_STACK_DEBUG:
            print("stack_len:", len(c))
            for i in range(len(c)):
                if c[i][1].endswith('click/core.py'):
                    print('stack:not showing click and below')
                    break
                print('stack:', i, c[i][1], c[i][3], c[i][2])
            # print c[stack_pos]
        for i in range(len(c)):
            if c[i][3] in CFG_UTIL_STACK_GET_LINE_NOT:
                continue
            else:
                return c[i]

        return c[stack_pos]
    except IndexError:
        return 'get_caller_line: no caller'

if __name__ == '__main__':
    def a():
        def b():
            def c():
                for i in range(10):
                    print(get_caller_line(i))
            c()
        b()
    a()
