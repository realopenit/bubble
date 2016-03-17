# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import sys
from bubble.util.store import get_file, put_file
from bubble import Bubble


def _convert(ctx=Bubble(), abspath='', fromtype='json', totype='yaml'):
    new_file = abspath.replace(fromtype, totype)
    ctx.say('converting:' + abspath + '>>>' + new_file, verbosity=10)
    data = get_file(ctx, abspath, False)
    ctx.say('data', stuff=data, verbosity=1000)
    res = put_file(ctx, new_file, data['lod_gen'], remove_first=True)
    return res


def convert(b, from_type, to_type, stage, step_to_convert):
    steps = 'pulled', 'push', 'transformed', 'uniq_pull', 'uniq_push', 'store'
    for step in steps:
        if step == step_to_convert:
            file_name = '%s_%s.%s' % (step, stage, from_type)
            print(_convert(b, file_name, from_type, to_type))


if __name__ == '__main__':
    from bubble.util.cli_misc import utf8_only
    from bubble.cli import STORAGE_TYPES
    b = Bubble()
    b.verbose = 100
    utf8_only(b)
    # print b
    # from_type='json'
    # to_type='sqlite3'
    # print sys.argv
    if len(sys.argv) == 6:
        from_type = sys.argv[1]  # 'json'
        to_type = sys.argv[2]  # 'sqlite3'
        stage = sys.argv[3]  # 'DEV'
        step = sys.argv[4]  # 'pulled'
        verbose = sys.argv[5]  # 100

        b.set_verbose(verbose)
        convert(b, from_type, to_type, stage, step)
    else:
        print(
            'usage: python -m bubble.utile.convert_storage [from_type] [to_type] [stage] [step] [verbose]')
        print(
            'example: python -m bubble.utile.convert_storage json sqlite3 DEV pulled 100')
        print(
            'available storage_types: python -m bubble.utile.convert_storage json sqlite3 pulled')

        steps = 'pulled', 'push', 'transformed', 'uniq_pull', 'uniq_push', 'store'
        print('available steps:' + str(steps))
        print(','.join(STORAGE_TYPES))
