# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import sys
from bubble.util.store import get_file
from bubble import Bubble
from . import lod_dump
from bubble.cli import STORAGE_TYPES
from bubble.cli import STEPS

from bubble.util.cli_misc import utf8_only


def convert(b, from_type, to_type, stage, step_to_convert, ds_args):
    for step in STEPS:
        if step == step_to_convert:
            file_name = '%s_%s.%s' % (step, stage, from_type)
            data = get_file(b, file_name, False)
            b.say(stuff=data)
            return lod_dump(ctx=b,
                            dataset_args=ds_args,
                            step=step,
                            stage=stage,
                            reset=True,
                            full_data=True,
                            data=data['lod_gen'],
                            archive=True)


if __name__ == '__main__':
    if len(sys.argv) == 7:
        from_type = sys.argv[1]   # 'json'
        to_type = sys.argv[2]     # 'sqlite3'
        stage = sys.argv[3]       # 'DEV'
        step = sys.argv[4]        # 'pulled'
        tag = sys.argv[5]         # 'testtag' #customer tag
        verbose = sys.argv[6]     # 100

        b = Bubble()
        utf8_only(b)
        b.set_verbose(verbose)
        DS_ARGS = {'DS_TYPE': 'sqlite',
                   'DS_BUBBLE_TAG': tag}

        convert(b, from_type, to_type, stage, step, DS_ARGS)
    else:
        pm = ' python -m bubble.util.convert_storage '
        print('usage: ' + pm +
              '[from_type] [to_type] [stage] [step] [tag] [verbose]')
        print('example: ' + pm + ' json ds_sqlite DEV pulled custcode 100')
        print('to_type is ignored for now: defaulting to dataset:sqlite')
        print('available storage_types: ' + ', '.join(STORAGE_TYPES))
        print('available steps: ' + ', '.join(STEPS))
