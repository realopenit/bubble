# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

from .buts import buts

BUBBLE_SEP = '.'
__esc_table = []


def add_esc(chars, tag):
    global __esc_table
    tra = {'chars': chars,
           'tag': buts('esc' + tag)}
    __esc_table.append(tra)

add_esc(BUBBLE_SEP, 'sep')
add_esc(':', 'colon')
add_esc(',', 'comma')
add_esc('>>>', 'arrows')
# add_esc('@','at')


def escape(ctx, key_str, sep='.'):
    escaped = key_str
    for esc in __esc_table:
        escaped = escaped.replace(esc['chars'], esc['tag'])

    if key_str != escaped:
        ctx.gbc.say('path_str:escaped: [%s] to [%s]' %
                    (key_str, escaped), verbosity=100)
    return escaped


def unescape(ctx, key_str):
    unescaped = key_str
    for esc in __esc_table:
        unescaped = unescaped.replace(esc['tag'], esc['chars'])

    if key_str != unescaped:
        ctx.gbc.say('path_str:unescaped: [%s] to [%s]' % (
            key_str, unescaped), verbosity=100)
    return unescaped
