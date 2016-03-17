# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

''' system rule functions which are predefined for generic usage '''
from .functions import register_system_function
##########################################################################


@register_system_function
def size(a):
    return len(a)


@register_system_function
def replace(this, that):
    ret = input.replace(str(this), str(that))
    return ret


@register_system_function
def equal(a, b):
    r = False
    if str(a) == str(b):
        r = True
    return r


@register_system_function
def bool_equal(str_bool='True', bool_bool=False):
    r = False
    if str_bool == 'False':
        c = False
    if str_bool == 'True':
        c = True
    if c == bool_bool:
        r = True
    return r


def isin(sub, string):
    r = False
    if sub in string:
        r = True
    return r
register_system_function(isin, name='in')


@register_system_function
def get(thing, stuff):
    if thing in stuff:
        return stuff[thing]
    return None


def set_kv(k, v, stuff):
    stuff[k] = v
    # print stuff
    return stuff
register_system_function(set_kv, name='set')


def slicing(slicable, start=0, stop=-1, step=1):
    return slicable[int(start):int(stop):int(step)]
register_system_function(slicing, name='slice')


@register_system_function
def concat(*a):
    return ''.join(a)


@register_system_function
def increment(i):
    return int(i) + 1


@register_system_function
def append(thing, stuff):
    return stuff.append(thing)
