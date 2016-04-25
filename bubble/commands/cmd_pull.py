# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import pass_bubble
from ..cli import STAGES
from ..util.cli_misc import get_client, update_stats
from ..util.cli_misc import bubble_lod_dump

@click.command('pull',
               short_help='Pull data from Source Service Client')
@click.option('--amount',
              '-a',
              type=int,
              default=-1,
              help='set the amount to pull')
@click.option('--index',
              '-i',
              type=int,
              default=-1,
              help='set the starting index for the pull')
@click.option('--query',
              '-q',
              type=str,
              default=None,
              help='get single object with SRC ID, only if client has a query method')
@click.option('--stage',
              '-s',
              default='DEV',
              help='set the staging :' + ','.join(STAGES))
@pass_bubble
def cli(ctx, amount, index, query, stage):
    """Pull data from Source Service Client"""

    if not ctx.bubble:
        ctx.say_yellow('There is no bubble present, will not pull')
        raise click.Abort()
    STAGE = None
    SRC = None

    if stage in STAGES and stage in ctx.cfg.CFG:
        STAGE = ctx.cfg.CFG[stage]

    if not STAGE:
        ctx.say_red('There is no STAGE in CFG:' + stage)
        ctx.say_yellow('please check configuration in ' +
                       ctx.home + '/config/config.yaml')
        raise click.Abort()

    if 'SOURCE' in STAGE:
        SRC = STAGE.SOURCE
    if not SRC:
        ctx.say_red('There is no SOURCE in stage:' + stage)
        ctx.say_yellow('please check configuration in ' +
                       ctx.home + '/config/config.yaml')
        raise click.Abort()
    gbc = ctx.GLOBALS['gbc']
    src_client = get_client(gbc, SRC.CLIENT, ctx.home)

    # TODO: client get error count?
    # make default counters
    # client.pull(amount,index,counters)
    # counter:#Good Bad Ugly: BUG, counters
    # for this the client must be able to keep stats, or update stats in the pull loop.
    # bug.counters

    try:
        sclient = src_client.BubbleClient(cfg=SRC)
        sclient.set_parent(gbc)
        sclient.set_verbose(ctx.get_verbose())
    except Exception as e:
        ctx.say_red(
            'cannot create bubble client:' + SRC.CLIENT)
        ctx.say_red(str(e))
        raise click.Abort('cannot pull')

    full_data = False
    if amount == -1 and index == -1:
        full_data = True

    try:
        if amount > 0:
            if index < 0:
                index = 0
            pb_label='Pulling %d+%d '% (index,amount)
            src_data_gen = sclient.pull(amount, index)
        else:
            if query:
                pb_label='Querying:%s' % query
                src_data_gen = [sclient.query(query)]
                full_data = False
            else:
                pb_label='Pulling all'
                src_data_gen = sclient.pull()
    except Exception as e:
        ctx.say_red('cannot pull from source client: ' + SRC.CLIENT)
        ctx.say_red(str(e))
        raise click.Abort('cannot pull')
    click.echo()

    # TODO: these actually need to be counted someway.
    # in client,
    # in storage,
    # where else?
    error_count = 0

    with click.progressbar(src_data_gen,
                           label=pb_label,
                           show_pos=True,
                           length=amount,
                           show_eta=True,
                           fill_char='◐') as progress_src_data_gen:
        pfr = bubble_lod_dump(ctx=ctx,
                          step='pulled',
                          stage=stage,
                          full_data=full_data,
                          reset=True,
                          data_gen=progress_src_data_gen)
    ctx.say('pulled [%d] objects' % pfr['total'])


    stats = {}
    stats['pulled_stat_error_count'] = error_count
    stats['pulled_stat_total_count'] = pfr['total']
    update_stats(ctx, stage, stats)

    return True
