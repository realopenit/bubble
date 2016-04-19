# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click
import tablib
from ..cli import pass_bubble

from ..cli import STAGES
from ..util.cli_misc import bubble_lod_load
from ..util.cli_misc import get_pairs
from ..util.generators import get_gen_slice
from ..util.flat_dict import flat, get_flat_path
from ..util.buts import buts

# todo:move to magic definitions
exportables = ['pulled', 'uniq_pull', 'uniq_push',
               'push', 'pushed', 'store', 'stats']


@click.command('promote',
               short_help='Like Export, but promote from step stage to step stage(experimental)')
@click.option('--amount',
              '-a',
              type=int,
              default=-1,
              help='set the amount to export')
@click.option('--index',
              '-i',
              type=int,
              default=-1,
              help='set the starting index')
@click.option('--stage',
              '-s',
              default='DEV',
              help='set the staging :' + ','.join(STAGES))
@click.option('--deststage',
              '-d',
              default='DEV',
              help='set the destination staging :' + ','.join(STAGES))
@click.option('--stepresult',
              '-r',
              default='pushed',
              help='the input stepresult for the export one of:' + ', '.join(exportables))
@click.option('--tostep',
              '-t',
              default='pushed',
              help='the selection of "export" of  should be stored in this step, one of:' + ', '.join(exportables))
@click.option('--select',
              '-c',
              default='',
              help='keys to select keys for export key1,key2 or aliased key1:first,key2:second')
@click.option('--where',
              '-w',
              default='',
              help='where  key1:value1 [,key2:value2]')
@click.option('--order',
              '-O', default='',
              help='order by key,ascending')
@click.option('--position',
              '-p',
              is_flag=True,
              default=False,
              help='if position, also append the position (index for item in total list)')
@pass_bubble
def cli(ctx, amount, index, stage, deststage, stepresult, tostep, select, where, order, position):
    """Promote data from one stage to another(experimental)

    First collect the correct information with export,
    and promote result by adjusting command to promote and adding missing options.
    """
    if not ctx.bubble:
        msg = 'There is no bubble present, will not promote'
        ctx.say_yellow(msg)
        raise click.Abort()

    if stage not in STAGES:
        ctx.say_yellow('There is no known stage:' + stage)
        raise click.Abort()
    if stepresult not in exportables:
        ctx.say_yellow('stepresult not one of: ' + ', '.join(exportables))
        raise click.Abort()
    ctx.gbc.say('promote:args', stuff=(ctx, amount, index, stage,
                                       deststage, stepresult, tostep, select, where, order, position))
    data_gen = bubble_lod_load(ctx, stepresult, stage)

    ctx.gbc.say('data_gen:', stuff=data_gen, verbosity=20)

    part = get_gen_slice(ctx.gbc, data_gen, amount, index)
    ctx.gbc.say('selected part:', stuff=part, verbosity=20)

    aliases = get_pairs(ctx.gbc, select, missing_colon=True)
    if position:
        ctx.gbc.say('adding position to selection of columns:',
                    stuff=aliases, verbosity=20)
        aliases.insert(0, {'key': buts('index'), 'val': 'BUBBLE_IDX'})
        ctx.gbc.say('added position to selection of columns:',
                    stuff=aliases, verbosity=20)

    wheres = get_pairs(ctx.gbc, where)
    # TODO: use aliases as lookup for wheres

    data = tablib.Dataset()

    data.headers = [sel['val'] for sel in aliases]
    ctx.gbc.say('select wheres:' + str(wheres), verbosity=20)
    ctx.gbc.say('select aliases:' + str(aliases), verbosity=20)
    ctx.gbc.say('select data.headers:' + str(data.headers), verbosity=20)

    # TODO: get this selecting stuff into a shared function from export

    try:
        for ditem in part:
            row = []
            ctx.gbc.say('curr dict', stuff=ditem, verbosity=101)

            flitem = flat(ctx, ditem)
            ctx.gbc.say('curr flat dict', stuff=flitem, verbosity=101)
            row_ok = True
            for wp in wheres:
                # TODO: negative selects: k:None, k:False,k:Zero,k:Null,k:0,k:-1,k:'',k:"",
                # TODO: negative selects: k:BUBBLE_NO_KEY,k:BUBBLE_NO_VAL

                if not wp['val'] in str(flitem[wp['key']]):
                    row_ok = False
            if not row_ok:
                continue

            for sel in aliases:
                if sel['key'] in flitem:
                    row.append(flitem[sel['key']])
                else:
                    # temporary to check, not use case for buts()
                    bnp = '____BTS_NO_PATH_'
                    tempv = get_flat_path(ctx, flitem, sel['key'] + '.*', bnp)
                    if tempv != bnp:
                        row.append(tempv)
                    else:
                        row.append('None')
                        # TODO maybe 'NONE', or just '' or something like:
                        # magic.export_format_none

            data.append(row)

    except Exception as excpt:
        ctx.say_red('Cannot promote data', stuff=excpt)
        raise click.Abort()

    if order:
        olast2 = order[-2:]
        ctx.gbc.say('order:' + order + ' last2:' + olast2, verbosity=100)
        if olast2 not in [':+', ':-']:
            data = data.sort(order, False)
        else:
            if olast2 == ':+':
                data = data.sort(order[:-2], False)
            if olast2 == ':-':
                data = data.sort(order[:-2], True)
