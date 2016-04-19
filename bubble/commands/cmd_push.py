# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import pass_bubble
from ..cli import STAGES
from ..util.cli_misc import get_client, update_stats
from ..util.generators import get_gen_slice
from ..util.cli_misc import bubble_lod_dump, bubble_lod_load
from ..util.counter import Counter


def do_yielding_push(ctx, to_push, tclient, total_counter, error_counter):
    with click.progressbar(to_push, label='Pushing') as data:
        for d in data:
            total_counter.count()
            try:
                ctx.gbc.say('pushing(in try)', stuff=d, verbosity=100)
                yield {'res': tclient.push(d),
                       'input': d}

            except Exception as e:
                ctx.say_red(
                    'cannot push data to bubble.clients.' + tclient.name)
                yield {'error': e,
                       'input': d,
                       'from': 'command_push_to_client_try'}
                error_counter.count()

@click.command('push',
               short_help='Push data to Target Service Client.')
@click.option('--amount',
              '-a',
              type=int,
              default=-1,
              help='set the amount to push')
@click.option('--index',
              '-i',
              type=int,
              default=-1,
              help='set the starting index')
@click.option('--stage',
              '-s',
              default='DEV',
              help='set the staging :' + ','.join(STAGES))
@pass_bubble
def cli(ctx,
        amount,
        index,
        stage):
    """Push data to  Target Service Client"""

    if not ctx.bubble:
        ctx.say_yellow('There is no bubble present, will not push')
        raise click.Abort()

    TGT = None
    transformed = True
    STAGE = None

    if stage in STAGES and  stage in ctx.cfg.CFG:
        STAGE = ctx.cfg.CFG[stage]
    if not STAGE:
        ctx.say_red('There is no STAGE in CFG:' + stage)
        ctx.say_yellow('please check configuration in ' +
                        ctx.home + '/config/config.yaml')
        raise click.Abort()


    if 'TARGET' in STAGE:
        TGT = STAGE.TARGET
    if 'TRANSFORM' in STAGE:
        transformed = True
    else:
        transformed = False

    if not transformed:
        ctx.say_yellow("""There is no transform defined in the configuration, will not transform,
using the results of step 'pulled' instead of 'push'
""")

    if not TGT:
        ctx.say_red('There is no TARGET in: ' + stage)
        ctx.say_yellow('please check configuration in ' +
                       ctx.home + '/config/config.yaml')
        raise click.Abort()

    tgt_client = get_client(ctx.gbc, TGT.CLIENT, ctx.home)

    try:
        tclient = tgt_client.BubbleClient(cfg=TGT)
        tclient.set_parent(ctx.gbc)
        tclient.set_verbose(ctx.get_verbose())
    except Exception as e:
        ctx.say_red('cannot create bubble client:' + TGT.CLIENT)
        ctx.say_red(str(e))
        raise click.Abort('can not push')

    step_to_load = 'push'
    if not transformed:
        step_to_load = 'pulled'
    data_gen = bubble_lod_load(ctx, step_to_load, stage)

    full_data = False
    if amount == -1 and index == -1:
        full_data = True
    to_push = get_gen_slice(ctx.gbc, data_gen, amount, index)

    error_count = Counter()
    total_count = Counter()

    pushres = do_yielding_push(ctx=ctx,
                               to_push=to_push,
                               tclient=tclient,
                               total_counter=total_count,
                               error_counter=error_count)
    pfr = bubble_lod_dump(ctx=ctx,
                          step='pushed',
                          stage=stage,
                          full_data=full_data,
                          reset=True,
                          data_gen=pushres)

    ctx.say('pushed [%d] objects' % pfr['total'])

    stats = {}
    stats['pushed_stat_error_count'] = error_count.get_total()
    stats['pushed_stat_total_count'] = total_count.get_total()
    update_stats(ctx, stage, stats)

    return True
