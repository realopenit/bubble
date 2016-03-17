# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import arrow
from .buts import buts
from .flat_dict import flat, unflat, get_flat_path, set_flat_at_path


# TODO: make generator def get_newest_uniq(ctx, luniq_res={}):

def get_uniq_list(ctx, luniq_res={}):
    ctx.gbc.say('get_uniq_list from uniq list',
                stuff=luniq_res, verbosity=1000)
    for item_key in luniq_res['keys_index'].keys():
        item = luniq_res['keys_index'][item_key]
        yield item


def get_newest_uniq(ctx, luniq_res={}):
    ctx.gbc.say('get_newest_uniq from uniq list',
                stuff=luniq_res, verbosity=1000)
    newest = []
    if luniq_res['full_data']:
        # everything, including missing
        full = True
    else:
        # only selection index,amount
        full = False
        selection = luniq_res['processed_keys']

    for item_key in luniq_res['keys_index'].keys():
        item = luniq_res['keys_index'][item_key]
        if full:
            newest.append(get_current(ctx, item))
        else:
            if item_key in selection:
                newest.append(get_current(ctx, item))

    ctx.gbc.say('get_newest_uniq from uniq list:res',
                stuff=newest, verbosity=1000)
    return newest


def get_current(gbc, item):
    gbc.say('get current item', stuff=item, verbosity=100)

    item = flat(gbc, item)
    current = get_flat_path(gbc, item, 'current.*', {})
    gbc.say('current', stuff=current, verbosity=100)

    delta = get_flat_path(gbc, item, 'delta.*', {})
    gbc.say('delta', stuff=delta, verbosity=100)

    current = set_flat_at_path(gbc, '__BTS_DELTA', delta, current)
    current['__BTS_TIMESTAMP'] = get_flat_path(
        gbc, item, 'current.' + buts('storetimestamp'))

    current['__BTS_MISSING'] = get_flat_path(gbc, item, 'missing')
    missing_count = get_flat_path(gbc, item, 'missing_count')
    current['__BTS_MISSING_COUNT'] = missing_count
    if get_flat_path(gbc, item, 'history_amount') > 1:
        current['__BTS_LAST'] = get_flat_path(gbc, item, 'previous.*')
    return current


def make_uniq(ctx, ldict=[], keyed=[], uniqstr='id', tag='PRE', full_data=True, remove_missing_after_seconds=None):
    ctx.gbc.say('make_uniq:lod', stuff=ldict, verbosity=1000)
    ctx.gbc.say('make_uniq:keyed', stuff=keyed, verbosity=1000)

    ukeys = uniqstr.split(',')
    ctx.gbc.say('make_uniq:keyed:ukeys', stuff=ukeys, verbosity=1000)

    keys_index = make_key_index(
        ctx.gbc, keyed, full_data, remove_missing_after_seconds)
    processed_keys = []
    index = 0
    full_data_ldict = None  # peek at first item to see full data for pull/push

    ctx.gbc.say('make_uniq:keyed:keys_index', stuff=keys_index, verbosity=1000)
    for current in ldict:
        new_item = {}
        index += 1
        ctx.gbc.say('make_uniq:current dict:', stuff=current, verbosity=100)
        key = get_ukey(ctx.gbc, current, ukeys)
        if index == 1:
            if buts('fulldata') in current:
                full_data_ldict = current[buts('fulldata')]
        if key not in processed_keys:
            processed_keys.append(key)
        if key not in keys_index:
            # add new item
            delta = {'create': True}
            total = 1
        else:
            keyed_item = keys_index[key]
            ctx.gbc.say('keyed_item', stuff=keyed_item, verbosity=100)
            prev = get_flat_path(ctx.gbc, keyed_item, 'current.*')
            ctx.gbc.say('prev', stuff=prev, verbosity=100)

            sts = buts('storetimestamp')
            if sts in prev and sts in current:
                ctx.gbc.say('storetimestamp: prev[%s] =?= curr[%s]' % (
                    prev[sts], current[sts]), verbosity=10)
                if prev[sts] == current[sts]:
                    # item is in current pull and has previously been processed
                    keys_index[key]['missing_count'] = 0
                    keys_index[key]['touch_count'] += 1
                    current['missing'] = False
                    ctx.gbc.say('sts already processed, skipping',
                                verbosity=20)
                    continue

            cprev = clean_bts(ctx.gbc, prev)
            ctx.gbc.say('cprev val:', stuff=cprev, verbosity=100)

            delta = dict_delta(ctx.gbc, current, cprev)
            delta['create'] = False

            # if DEBUG_DELTA: ...
            # ctx.say('delta:', stuff=delta, verbosity=100)
            # ctx.cry('new', stuff=new_item)

            # ctx.cry('current', stuff=current)
            # total = keys_index[key]['history_amount'] + 1
            # ctx.cry('keys_index[key]', stuff=keys_index[key])
            # ctx.cry('keyed_item', stuff=keyed_item)

            total = keyed_item['history_amount'] + 1

        current['__BTS_UNIQ_' + tag.upper()] = key
        current['__BTS_UNIQ_KEYSTR'] = uniqstr

        new_item['uid'] = key

        new_item['current'] = unflat(ctx.gbc, current)
        new_item['delta'] = delta

        new_item['history_amount'] = total
        new_item['missing_count'] = 0
        new_item['touch_count'] = 0
        new_item['missing'] = False
        new_item['timestamp'] = str(arrow.now())

        keys_index[key] = new_item
        ctx.gbc.say('setting keys_index[{%s}] with new item:' % (key),
                    stuff=new_item,
                    verbosity=1000)

    ctx.gbc.say('keys_index:',
                stuff=keys_index,
                verbosity=1000)

    return {'keys_index': keys_index,
            'processed_keys': processed_keys,
            'full_data': full_data or full_data_ldict}


def make_key_index(ctx, keyed, full_data, remove_missing_after_seconds=None):
    # for now remove_missing_after_seconds in seconds default a week
    # TODO: "7 Days" --> 604800
    ctx.gbc.say('make_key_index:remove_missing_after_seconds:' +
                str(remove_missing_after_seconds), verbosity=100)
    key_index = {}

    # when slicing: index+amount
    # full data should be false.

    ctx.gbc.say('keyed:', stuff=keyed, verbosity=1000)
    for item in keyed:
        ctx.gbc.say('keyed:item:', stuff=item, verbosity=100)

        if 'uid' in item:
            item_key = item['uid']

        item_missing = item['missing']
        ctx.gbc.say('is this item missing:' + str(item_missing), verbosity=100)
        if isinstance(remove_missing_after_seconds, int) and item_missing:
            ctx.gbc.say('item missing and remove seconds set', verbosity=100)
            item_timestamp = item['current.' + buts('storetimestamp')]
            tsdelta = arrow.now() - arrow.get(item_timestamp)
            seconds_in_day = 24 * 60 * 60
            delta_seconds = tsdelta.days * seconds_in_day + tsdelta.seconds
            if delta_seconds > remove_missing_after_seconds:
                ctx.gbc.say('skipping (remove) missing after %d seconds passed > %s ' % (delta_seconds,
                                                                                         remove_missing_after_seconds))
                continue
        if 'touch_count' in item:
            item['touch_count'] += 1
        else:
            item['touch_count'] = 1

        if full_data:
            if 'missing_count' not in item:
                item['missing_count'] = 0
            else:
                item['missing_count'] += 1
            item['missing'] = True
        else:
            item['missing'] = 'UNKNOWN'
        key_index[item_key] = item

    ctx.gbc.say('make_key_index:res:', stuff=key_index, verbosity=1000)
    return key_index


def find_key_index(ctx, key_index, key):
    ctx.gbc.say('find_key_index:looking for key [%s] in:' % key,
                stuff=key_index,
                verbosity=1000)

    if key in key_index:
        ctx.gbc.say('found:key[%s] at index[%d]' % (key, key_index[key]),
                    verbosity=100)
        return key_index[key]

    return None


def get_ukey(ctx, current={}, keys=[]):
    kvs = []
    flcurrent = flat(ctx, current)

    ctx.gbc.say('get_ukey %s' % str(keys),
                stuff=flcurrent.keys(), verbosity=1000)

    for kpath in keys:
        if kpath in flcurrent:
            kval = flcurrent[kpath]
            kval = str(kval)
            kvs.append(kval)
        else:
            kvs.append('NoKeyPathValue')
    key = ']_['.join(kvs)
    key = '[' + key + ']'
    ctx.gbc.say('get_ukey res:%s' % key, verbosity=100)
    return key


def dict_delta(ctx, new={}, old={}):
    left = flat(ctx, new)
    right = flat(ctx, old)

    ctx.gbc.say('dict_delta:::left=', stuff=left, verbosity=100)
    ctx.gbc.say('dict_delta:::right=', stuff=right, verbosity=100)
    ctx.gbc.say('dict_delta:::left==right=' +
                str(left == right), verbosity=100)

    delta = {}

    lkl = left.keys()
    lks = set(lkl)

    rkl = set(right.keys())
    rks = set(rkl)
    added = lks - rks
    removed = rks - lks

    add_or_remove = set.union(added, removed)

    lvl = left.values()
    rvl = right.values()

    lvs = set(lvl)
    rvs = set(rvl)
    if lvs == rvs:
        value_sets_same = True
    else:
        value_sets_same = False

    modified = []
    for k in lks:
        ctx.gbc.say('dict_delta:::k=' + k, verbosity=100)
        if k == buts('storetimestamp'):
            continue
        if k == buts('index'):
            continue
        if k in add_or_remove:
            ctx.gbc.say('dict_delta:::skip', verbosity=100)
        else:
            mod = {}
            mod['key'] = k
            lv = left[k]
            rv = right[k]
            ctx.gbc.say('dict_delta:::lv=', stuff=lv, verbosity=100)
            ctx.gbc.say('dict_delta:::rv=', stuff=rv, verbosity=100)

            if lv == rv:
                continue
            if type(lv) != type(rv):
                mod['from_type'] = type(rv)
                mod['to_type'] = type(lv)
                ctx.gbc.say('dict_delta:::types=' + str(type(lv)) +
                            '!=' + str(type(rv)), verbosity=100)

            mod['from'] = rv
            mod['to'] = lv
            modified.append(mod)

    delta['added'] = list(added)
    delta['removed'] = list(removed)
    delta['modified'] = modified

    delta['diffs_total'] = len(delta['added']) + \
        len(delta['modified']) + len(delta['removed'])
    delta['lk_amount'] = len(lkl)
    delta['rk_amount'] = len(rkl)
    delta['lks_amount'] = len(lks)
    delta['rks_amount'] = len(rks)
    delta['lv_amount'] = len(lvl)
    delta['rv_amount'] = len(rvl)
    delta['lvs_amount'] = len(lvs)
    delta['rvs_amount'] = len(rvs)
    if len(added) == 0 and len(removed) == 0 and len(modified) == 0:
        delta['equal'] = True
        delta['drifting'] = False
    else:
        delta['equal'] = False
        if value_sets_same:
            delta['drifting'] = True

        ctx.gbc.say('dict_delta:::delta=', stuff=delta, verbosity=100)
    return delta


def clean_bts(ctx, data={}):
    clean = {}
    for (k, v) in data.items():
        if k.startswith('__BTS_'):
            ctx.say('skipping bts key'+k, verbosity=100)
        else:
            clean[k] = v

    return clean
