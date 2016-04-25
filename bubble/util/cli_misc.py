# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import arrow
import click
import importlib
import sys
import os
import six

from .store import put_file, get_file, get_file_name
from .delta import make_uniq, get_newest_uniq, get_uniq_list
from .dataset import lod_dump, lod_load
from ..functions import get_registered_rule_functions, load_custom_functions


def file_exists(ctx, abs_file_name):
    if os.path.exists(abs_file_name) and \
       os.path.isfile(abs_file_name):
        ctx.say('yes,file_exists:'+abs_file_name, verbosity=20)
        return True
    else:
        ctx.say('no,file_exists:'+abs_file_name, verbosity=10)
        return False


def create_dir(ctx, abs_dir_path):
    if os.path.exists(abs_dir_path) and os.path.isdir(abs_dir_path):
        pass
    else:
        os.mkdir(abs_dir_path)
        ctx.say_green('Created directory: %s' % abs_dir_path)


def utf8_only(ctx):
    if sys.getdefaultencoding() not in ['UTF8', 'UTF-8', 'utf-8']:
        org_encoding = sys.getdefaultencoding()
        ctx.say('org_encoding=' + org_encoding, verbosity=2)
        if six.PY2:
            reload(sys)
            sys.setdefaultencoding('UTF-8')
            ctx.say('Bubble: set encoding from [%s] to [%s]' %
                    (org_encoding,
                        sys.getdefaultencoding()), verbosity=2)
        else:
            importlib.reload(sys)
            ctx.cry('Bubble: currently working in non UTF8 encoding [%s]' % org_encoding)


def get_client(ctx, CLIENT, abs_path=None):
    ctx.say('getting: ' + str(CLIENT), verbosity=10)
    if abs_path:
        sys.path.insert(0, abs_path)

    try:
        # TODO: if CLIENT.endswith('.py'):
        if CLIENT.startswith('./'):
            ctx.say('Loading custom local BubbleClient', verbosity=10)
            c = CLIENT.replace('./', '')
            c = c.replace('.py', '')
            ctx.say('Importing c:' + c + ' in ' + abs_path, verbosity=10)
            bubble_client = importlib.import_module(c)
        else:
            bubble_client = importlib.import_module(CLIENT)

        return bubble_client
    except ImportError as e:
        ctx.cry('Cannot import bubble clients.' + CLIENT)
        ctx.cry(str(e))
        raise click.Abort()


def get_server(ctx, SERVER, abs_path=None):
    ctx.say('getting ' + str(SERVER), verbosity=10)
    if abs_path:
        sys.path.insert(0, abs_path)

    try:
        # TODO: if SERVER.endswith('.py'):

        if SERVER.startswith('./'):
            ctx.say('loading custom local Bubble Server', verbosity=10)
            c = SERVER.replace('./', '')
            c = c.replace('.py', '')
            ctx.say('importing c:' + c + ' in ' + abs_path)
            bubble_server = importlib.import_module(c)
        else:
            bubble_server = importlib.import_module('bubble.servers.' + SERVER)

        return bubble_server
    except ImportError as e:
        ctx.cry('cannot import bubble server.' + SERVER)
        ctx.cry(str(e))
        raise click.Abort()


def get_pairs(ctx, spairs=None, missing_colon=False):
    ctx.say('get_pairs:' + spairs + ',' + str(missing_colon),
            verbosity=100)
    # to get the pairs of key value for usage as selectors or conditions
    # aliases
    # wheres
    # spairs: ['key:a','key:b']
    # missing_colon=True
    # spairs: ['keya','key:b']

    if not spairs:
        return []
    dpairs = []
    tuples = []
    try:
        pairs = [s.strip() for s in spairs.split(',')]
        if len(pairs) > 0:
            if missing_colon:
                tuples = _get_tuples_missing_colon(ctx, pairs,
                                                   missing_colon_value='copy')
            else:
                tuples = _get_tuples(ctx, pairs)

        if len(tuples) > 0:
            dpairs = [{'key': pt[0].strip(), 'val':pt[1].strip()}
                      for pt in tuples]
    except Exception as e:
        ctx.cry('Cannot understand pairs option:' + spairs)
        raise e
    ctx.say('get_pairs:res:',
            stuff=dpairs,
            verbosity=100)
    return dpairs


def _get_tuples(ctx, pairs):
    tuples = [p.split(':') for p in pairs]
    ctx.say('_get_tuples:res:',
            stuff=tuples,
            verbosity=100)
    return tuples


def _get_tuples_missing_colon(ctx, pairs=None, missing_colon_value='copy'):
    ctx.say('_get_tuples_missing_colon:' + str(pairs) + ',' + str(missing_colon_value),
            verbosity=100)

    tuples = []
    for p in pairs:
        if ':' in p:
            tup = p.split(':')
        else:
            if missing_colon_value == 'copy':
                tup = (p, p)
            else:
                tup = (p, None)

        ctx.say('_get_tuples_missing_colon:tup' + str(tup),
                verbosity=100)
        tuples.append(tup)
    return tuples


def _find_lod_gen(ctx, loader):
    ctx.gbc.say('find_lod_gen', stuff=loader, verbosity=10)
    ctx.gbc.say('find_lod_gen:loader type:[%s]' %
                str(type(loader)), verbosity=10)
    if isinstance(loader, dict) and 'lod_gen' in loader:
        ctx.gbc.say('find_lod_gen:lod_gen found', verbosity=10)
        lod_gen = loader['lod_gen']
    else:
        lod_gen = loader
        ctx.gbc.say(
            'find_lod_gen:lod_gen Not found, returning loader as is', verbosity=10)
    return lod_gen


def update_stats(ctx, stage, stats={}):
    ctx.gbc.say('update_stats:', stuff=stats, verbosity=10)
    last_stats = {}
    step = 'stats'
    loader = bubble_lod_load(ctx, step, stage)

    lod_gen = _find_lod_gen(ctx, loader)

    if lod_gen:
        ctx.gbc.say('lod_gen', stuff=lod_gen, verbosity=10)
        # TODO: pass "order by id desc" to dataset
        for stats_data in lod_gen:
            last_stats = stats_data
        ctx.gbc.say('found last_stats:', stuff=last_stats, verbosity=10)
        # break
    command = ctx.GLOBALS['full_command']
    ctx.gbc.say("command=" + command, verbosity=10)
    last_stats['command'] = command
    start_arrow = ctx.GLOBALS['start_arrow']
    ctx.gbc.say("arrow_start=" + str(start_arrow), verbosity=10)
    last_stats['arrow_start'] = str(start_arrow)
    last_stats['arrow_end'] = str(arrow.now())

    # TODO: add call stats
    # for general idea see: show_verbose_statistics
    # if ctx.statistics:

    ctx.gbc.say('update_stats, last stats:', stuff=last_stats, verbosity=100)
    for key in stats.keys():
        last_stats[key] = stats[key]
    res = bubble_lod_dump(ctx=ctx,
                          step=step,
                          stage=stage,
                          full_data=False,
                          reset=False,
                          data_gen=[last_stats])
    # TODO: json has only this last item, DS just keeps everything in stats
    # table
    ctx.gbc.say('update_stats, updated stats:',
                stuff=last_stats, verbosity=100)
    return res


##########################################################################
def make_uniq_for_step(ctx, ukeys, step, stage, full_data, clean_missing_after_seconds, to_uniq):
    """initially just a copy from UNIQ_PULL"""

    # TODO:
    # this still seems to work ok for Storage types json/bubble,
    # for DS we need to reload de dumped step to uniqify

    if not ukeys:
        return to_uniq
    else:
        uniq_data = bubble_lod_load(ctx, step, stage)
        ctx.say('Creating uniq identifiers for [' + step + '] information', 0)

        ctx.gbc.say('uniq_data:', stuff=uniq_data, verbosity=1000)

        # TODO:make: data->keyed.items
        uniq_step_res = make_uniq(ctx=ctx,
                                  ldict=to_uniq,
                                  keyed=uniq_data,
                                  uniqstr=ukeys,
                                  tag=step,
                                  full_data=full_data,
                                  remove_missing_after_seconds=clean_missing_after_seconds)

        ctx.gbc.say('uniq_step_res:', stuff=uniq_step_res, verbosity=1000)

        to_uniq_newest = get_newest_uniq(ctx.gbc, uniq_step_res)

        # TODO: selected pulled only from slice of uniq
        # PROBLEM: slice of pull is not equal to slice of newest uniq,
        # can only select keys from newest, from slice of pulled
        # need a uid list from to_transform
        # to_transform = get_gen_slice(gbc, to_transform_newest, amount, index)
        # for now not a big problem, as with 'pump' there should be no problem
        to_uniq = to_uniq_newest
        # todo make keyed.items->data
        uniq_res_list = get_uniq_list(ctx.gbc, uniq_step_res)
        reset = True
        pfr = bubble_lod_dump(ctx=ctx,
                              step=step,
                              stage=stage,
                              full_data=full_data,
                              reset=reset,
                              data_gen=uniq_res_list)

        ctx.gbc.say('saved uniq ' + step + ' data res:',
                    stuff=pfr, verbosity=700)
        return to_uniq

##########################################################################
def load_rule_functions(ctx,
                        custom_rule_functions_py='./custom_rule_functions.py'):
    # todo, make sure the stage is passed in also
    ctx.say('cli_misc:load_rule_functions:'+custom_rule_functions_py, verbosity=10)

    rule_functions = get_registered_rule_functions()
    ctx.gbc.say('before loading: number of rule_function:' +
                str(rule_functions.functions_count()),
                verbosity=10)
    load_custom_functions(ctx, custom_rule_functions_py)
    ctx.gbc.say('after loading: number of rule_function:' +
                str(rule_functions.functions_count()),
                verbosity=10)

##########################################################################
def bubble_lod_dump(ctx, step, stage, full_data, reset, data_gen):
    STYPE = ctx.cfg.CFG.BUBBLE.STORAGE_TYPE
    STORAGE_TYPES = ctx.GLOBALS['storage_types']
    pfr = {'error': 'could not dump lod'}
    if STYPE == 'dataset' or STYPE in STORAGE_TYPES:
        STORAGE_TYPE = STYPE
    else:
        STORAGE_TYPE = 'json'

    path = ctx.home + '/'

    if STORAGE_TYPE == 'dataset':
        pfr = lod_dump(ctx=ctx,
                       step=step,
                       stage=stage,
                       dataset_args=ctx.cfg.CFG.BUBBLE.STORAGE_DATASET_ARGS,
                       data=data_gen,
                       full_data=full_data,
                       reset=reset)
        ctx.say_green(
            "\nsaved result in dataset[step:%s][stage:%s]" % (step, stage))

    else:
        storage_file = get_file_name(ctx, path, step, stage, STORAGE_TYPE)
        pfr = put_file(ctx=ctx,
                       storage_file_name=storage_file,
                       data=data_gen,
                       remove_first=True,
                       full_data=full_data)
        ctx.say_green("\nsaved result in [%s]" % storage_file)
    if 'total' not in pfr:
        pfr['total'] = 'Unknown total'
        pfr['total'] = -1
    return pfr

##########################################################################
def bubble_lod_load(ctx, step, stage):
    STYPE = ctx.cfg.CFG.BUBBLE.STORAGE_TYPE
    STORAGE_TYPES = ctx.GLOBALS['storage_types']
    gbc = ctx.GLOBALS['gbc']

    if STYPE == 'dataset' or STYPE in STORAGE_TYPES:
        STORAGE_TYPE = STYPE
    else:
        STORAGE_TYPE = 'json'

    path = ctx.home + '/'

    if STORAGE_TYPE == 'dataset':
        llr = lod_load(ctx=ctx,
                       step=step,
                       stage=stage,
                       dataset_args=ctx.cfg.CFG.BUBBLE.STORAGE_DATASET_ARGS)
        # ctx.say('load result in  dataset[step:%s][stage:%s]' % (step, stage), stuff=llr)
        loader = llr

    else:
        storage_file = get_file_name(ctx, path, step, stage, STORAGE_TYPE)
        gfr = get_file(ctx=ctx,
                       storage_file_name=storage_file)
        ctx.gbc.say('read [%s]' % storage_file, stuff=gfr)
        loader = gfr
    return _find_lod_gen(gbc, loader)
##########################################################################
