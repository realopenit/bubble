# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import pass_bubble
from ..cli import STAGES

from ..util.store import get_bubble
from ..util.generators import get_gen_slice
from ..util.cli_misc import bubble_lod_dump, bubble_lod_load
from ..util.counter import Counter


from ..util.cli_misc import update_stats, make_uniq_for_step

from ..transformer import Transformer


def do_yielding_transform(ctx, transformer, to_transform, total_counter, error_counter):
    with click.progressbar(to_transform, label='Transforming') as data:
        for sd in data:
            total_counter.count()
            try:
                res = transformer.transform(sd)
            except Exception as excpt:
                res = {'exception': str(excpt)}
                yield res
            if 'BUBBLE_SKIPPING' in res:
                continue
            if 'BUBBLE_ERROR' in res:
                error_counter.count()
            if 'exception' in res:
                error_counter.count()
            yield res
            ctx.gbc.say('transformer done one:transformed_count:%d,error_count:%d' %
                        (total_counter.get_total(), error_counter.get_total()),
                        verbosity=100)


@click.command('transform', short_help='Transform data.')
@click.option('--amount', '-a', type=int, default=-1, help='set the amount to transform')
@click.option('--index', '-i', type=int, default=-1, help='set the starting index')
@click.option('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@pass_bubble
def cli(ctx, amount, index, stage):
    """Transform data"""
    if not ctx.bubble:
        ctx.say_yellow('There is no bubble present, will not transform')
        raise click.Abort()

    path = ctx.home + '/'

    STAGE = None
    RULES = None
    UNIQ_KEYS_PULL = None
    UNIQ_KEYS_PUSH = None
    CLEAN_MISSING_AFTER_SECONDS = None
    if stage in STAGES and stage in ctx.cfg.CFG:
        STAGE = ctx.cfg.CFG[stage]
    if not STAGE:
        ctx.say_red('There is no STAGE in CFG:' + stage)
        ctx.say_yellow('please check configuration in ' +
        ctx.home + '/config/config.yaml')
        raise click.Abort()

    if 'TRANSFORM' in STAGE:
         TRANSFORM = ctx.cfg.CFG[stage].TRANSFORM
    else:
         ctx.say_yellow("""There is no transform defined in the configuration, will not transform,
when pushing the results of step 'pulled' will be read instead of 'push'
""")
         raise click.Abort()

    if 'RULES' in TRANSFORM:
        RULES = TRANSFORM.RULES
    if 'UNIQ_KEYS_PULL' in TRANSFORM:
        UNIQ_KEYS_PULL = TRANSFORM.UNIQ_KEYS_PULL
    if 'UNIQ_KEYS_PUSH' in TRANSFORM:
        UNIQ_KEYS_PUSH = TRANSFORM.UNIQ_KEYS_PUSH
    if 'CLEAN_MISSING_AFTER_SECONDS' in TRANSFORM:
        CLEAN_MISSING_AFTER_SECONDS = TRANSFORM.CLEAN_MISSING_AFTER_SECONDS

    if not RULES:
        ctx.say_red('There is no TRANSFORM.RULES in stage:' + stage)
        ctx.say_yellow('please check configuration in ' +
                       ctx.home + '/config/config.yaml')
        raise click.Abort()

    full_data = False
    if amount == -1 and index == -1:
        full_data = True

    data_gen = bubble_lod_load(ctx, 'store', stage)
    stored_data = {}
    for stored_data_item in data_gen:
        stored_data = stored_data_item
        break  # first_only

    ctx.gbc.say('stored:', stuff=stored_data, verbosity=150)

    cfgdict = {}
    cfgdict['CFG'] = ctx.cfg.CFG
    cfgdict['GENERAL_BUBBLE_CONTEXT'] = ctx.GLOBALS['gbc']
    cfgdict['ARGS'] = {'stage': stage,
                       'path': path}

    if type(RULES) == str and RULES.endswith('.bubble'):
        rules = get_bubble(ctx.gbc, path + RULES)
        rule_type = 'bubble'
        transformer = Transformer(rules=rules,
                                  rule_type=rule_type,
                                  store=stored_data,
                                  config=cfgdict,
                                  bubble_path=path,
                                  verbose=ctx.get_verbose())

    src_data = bubble_lod_load(ctx, 'pulled', stage)

    to_transform = get_gen_slice(ctx.gbc, src_data, amount, index)
    ctx.gbc.say('sliced to transform:', stuff=to_transform, verbosity=50)

    if UNIQ_KEYS_PULL:
        to_transform = make_uniq_for_step(ctx=ctx,
                                          ukeys=UNIQ_KEYS_PULL,
                                          step='uniq_pull',
                                          stage=stage,
                                          full_data=full_data,
                                          clean_missing_after_seconds=CLEAN_MISSING_AFTER_SECONDS,
                                          to_uniq=to_transform)

    ctx.gbc.say('transformer to transform', stuff=to_transform, verbosity=295)

    transformed_count = Counter()

    error_count = Counter()
    result = do_yielding_transform(ctx,
                                   transformer,
                                   to_transform,
                                   transformed_count,
                                   error_count)

    ##########################################################################
    pfr = bubble_lod_dump(ctx=ctx,
                          step='push',
                          stage=stage,
                          full_data=full_data,
                          reset=True,
                          data_gen=result)
    ctx.say('transformed [%d] objects' % pfr['total'])

    # closing the store, to be sure, get store after yielding transform has
    # completed
    store = transformer.get_store()
    ctx.gbc.say('transformer persistant storage', stuff=store, verbosity=1000)

    pfr = bubble_lod_dump(ctx=ctx,
                          step='store',
                          stage=stage,
                          full_data=full_data,
                          reset=True,
                          data_gen=[store])
    ctx.say('pulled [%d] objects' % pfr['total'])
    ctx.gbc.say('transformer all done :transformed_count:%d,error_count:%d' %
                (transformed_count.get_total(), error_count.get_total()),
                verbosity=10)

    if UNIQ_KEYS_PUSH:
        make_uniq_for_step(ctx=ctx,
                           ukeys=UNIQ_KEYS_PUSH,
                           step='uniq_push',
                           stage=stage,
                           full_data=full_data,
                           clean_missing_after_seconds=CLEAN_MISSING_AFTER_SECONDS,
                           to_uniq=result)
        # TODO: check if to_uniq can be loaded inside make_uniq
        # the result of the transform is a generator and should be 'empty' already
        # by the previous dump of the results.

    stats = {}
    stats['transformed_stat_error_count'] = error_count.get_total()
    stats['transformed_stat_transformed_count'] = transformed_count.get_total()

    update_stats(ctx, stage, stats)

    return True
