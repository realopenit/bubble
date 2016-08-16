# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click
import tablib

import path as opath
# todo: replace path variables so we can import path as is.


from ..cli import pass_bubble
from ..cli import STAGES
from ..cli import STEPS as exportables
from ..util.cli_misc import get_pairs
from ..util.generators import get_gen_slice
from ..util.cli_misc import bubble_lod_load

from ..util.flat_dict import flat, get_flat_path
from ..util.buts import buts


@click.command('export', short_help='Export from memory to format supported by tablib.')
@click.option('--amount', '-a', type=int, default=-1,
              help='set the amount to export')
@click.option('--index', '-i', type=int, default=-1,
              help='set the starting index')
@click.option('--stage', '-s', default='DEV',
              help='set the staging: ' + ','.join(STAGES))
@click.option('--stepresult', '-r', default='pushed',
              help='the input stepresult for the export one of: ' + ', '.join(exportables))
@click.option('--formattype', '-f', default='csv',
              help='format for the export: csv, yaml, json, tab(to stdout)')
@click.option('--select', '-c', default='',
              help='header for csv or  keys to select keys for export key1,key2 or aliased key1:first,key2:second')
@click.option('--where', '-w', default='',
              help='where  key1:value1 [,key2:value2]')
@click.option('--order', '-O', default='',
              help='order by key,ascending')
@click.option('--outputfile', '-o', default='',
              help='the file to write to (defaults to ./export/export_stepresult_stage.format)')
@click.option('--showkeys', '-k', is_flag=True, default=False,
              help='show the (flattened) available keys first selected dict')
@click.option('--showvalues', '-v', is_flag=True, default=False,
              help='if showkeys, also show the values')
@click.option('--showalways', '-d', is_flag=True, default=False,
              help='show (dump) the keys/values always')
@click.option('--position', '-p', is_flag=True, default=False,
              help='if position, also append the position (index for item in total list)')
@pass_bubble
def cli(ctx,
        amount,
        index,
        stage,
        stepresult,
        formattype,
        select,
        where,
        order,
        outputfile,
        showkeys,
        showvalues,
        showalways,
        position):
    """Export from memory to format supported by tablib"""
    if not ctx.bubble:
        msg = 'There is no bubble present, will not export'
        ctx.say_yellow(msg)
        raise click.Abort()
    path = ctx.home + '/'

    if stage not in STAGES:
        ctx.say_yellow('There is no known stage:' + stage)
        raise click.Abort()
    if stepresult not in exportables:
        ctx.say_yellow('stepresult not one of: ' + ', '.join(exportables))
        raise click.Abort()

    data_gen = bubble_lod_load(ctx, stepresult, stage)

    ctx.gbc.say('data_gen:', stuff=data_gen, verbosity=20)

    part = get_gen_slice(ctx.gbc, data_gen, amount, index)
    ctx.gbc.say('selected part:', stuff=part, verbosity=20)

    aliases = get_pairs(ctx.gbc, select, missing_colon=True)
    if position or len(aliases) == 0:
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

    not_shown = True
    try:
        for ditem in part:
            row = []
            ctx.gbc.say('curr dict', stuff=ditem, verbosity=101)

            flitem = flat(ctx, ditem)
            ctx.gbc.say('curr flat dict', stuff=flitem, verbosity=101)
            row_ok = True
            for wp in wheres:
                # TODO: negative selects: k:None, k:False,k:Zero,k:Null,k:0,k:-1,k:'',k:"",
                # TODO: negative selects:
                # k:BUBBLE_NO_KEY,k:BUBBLE_NO_VAL,k:BUBBLE_NO_KEY_OR_NO_VAL

                wcheck_key=True
                if wp['key'] not in flitem:
                    row_ok = False
                    wcheck_key=False
                if wcheck_key and wp['val'] not in str(flitem[wp['key']]):
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
            # todo: count keys, and show all keys in selection: i,a
            if not_shown and showkeys:
                if not showalways:
                    not_shown = False
                ks = list(flitem.keys())
                ks.sort()
                ctx.say(
                    'available dict path keys from first selected dict:', verbosity=0)
                for k in ks:
                    ctx.say('keypath: ' + k, verbosity=0)
                    if showvalues:
                        ctx.say('value: ' + str(flitem[k]) + '\n', verbosity=0)

    except Exception as excpt:
        ctx.say_red('Cannot export data', stuff=excpt)
        raise click.Abort()

    if not outputfile:
        outputfile = path + 'export/export_' + \
            stepresult + '_' + stage + '.' + formattype

    # todo: order key must be present in selection
    # add to selection before
    # and remove from result before output to format.
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

    # Write `spreadsheet` to disk
    formatted = None
    if formattype == 'yaml':
        formatted = data.yaml
    if formattype == 'json':
        formatted = data.json
    if formattype == 'csv':
        formatted = data.csv

    # TODO:
    # if formattype == 'ldif':
    #    formatted = data.ldif

    if formattype == 'tab':
        # standard, output, whatever tablib makes of it, ascii table
        print(data)

    if formatted:
        enc_formatted = formatted.encode('utf-8')
        of_path = opath.Path(outputfile)
        of_dir = of_path.dirname()
        if not of_dir.exists():
            of_dir.makedirs_p()

        with open(outputfile, 'wb') as f:
            f.write(enc_formatted)
            ctx.say_green('exported: ' + outputfile)
