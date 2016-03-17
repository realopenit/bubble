# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

'''
# flattten and unflatten dictionaries with some "bubble twists", initial inspiration from:
# http://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys
# we only make also sure list items are naturally indexed and part of the whole key
# {'a':['A','B',{'d':'X'}]}
# becomes:
# {'a.1':'A'
#  'a.2':'B'
#  'a.3.d':'X'
#  'a.___bts_list_':true,
#  'a.___bts_listlen_':3,
#  '___bts_flat_':true
# }
# make index: natural indexing a configuration option
'''

from .buts import buts
from .escapes import escape, unescape

def flat(ctx, init={}, path='', sep='.', level=1):
    ctx.gbc.say('init:', stuff=init, verbosity=200)
    ctx.gbc.say('path:' + path, verbosity=200)
    ctx.gbc.say('sep:' + sep, verbosity=200)
    ctx.gbc.say('level:' + str(level), verbosity=200)
    if not isinstance(init, dict):
        msg = 'don\'t know how to flatten a non-dict'
        ctx.gbc.say(msg, verbosity=200)
        return {buts('flat'): False,
                buts('flat_error'): msg,
                buts('flat_input'): init}
    if level == 1 and buts('flat') in init and init[buts('flat')]:
        ctx.gbc.say(
            'already flattened, nothing to do,return unchanged', verbosity=200)
        return init
    nlevel = level + 1
    ret = {}
    for key, val in init.items():
        key = escape(ctx, key, sep)

        key = path + key
        if isinstance(val, dict):
            ret.update(flat(ctx=ctx,
                            init=val,
                            path=key + sep,
                            level=nlevel))
        elif isinstance(val, list):
            ctx.gbc.say('list', stuff=val, verbosity=200)
            tempd = {}
            tempd[buts('list')] = True
            tempd[buts('listlen')] = len(val)

            # natural index
            index = 1
            for v in val:
                tempd[str(index)] = v
                index += 1
            ctx.gbc.say('tempd', stuff=tempd, verbosity=200)
            ret.update(flat(ctx=ctx,
                            init=tempd,
                            path=key + sep,
                            level=nlevel))
        else:
            ret[key] = val
    if level == 1:
        ret[buts('flat')] = True
    return ret


def process_flk(ctx, k, proc, flktmp):
    ctx.gbc.say('process key:%s' % k, stuff={
                'proc': proc, 'flktmp': flktmp}, verbosity=1001)
    proc.append(k)
    if k in flktmp:
        del(flktmp[k])
    ctx.gbc.say('process res:', stuff={
                'k': k, 'proc': proc, 'flktmp': flktmp}, verbosity=1001)
    return proc, flktmp


def unflat_list(ctx, vals):
    # at leaf level!
    templ = []
    ctx.gbc.say('vals to make a list from:', stuff=vals, verbosity=1001)
    for index in range(vals[buts('listlen')]):
        ik = str(index + 1)
        if ik in vals:
            templ.append(vals[ik])
    ctx.gbc.say('templ', stuff=templ, verbosity=1001)
    return templ


def set_flat_at_path(ctx, path_str, star_dict, data):
    ctx.gbc.say('set_flat_at_path:value at:' + path_str +
                ' in:', stuff=data, verbosity=1001)
    ctx.gbc.say('set_flat_at_path:values:', stuff=star_dict, verbosity=1001)

    for (k, v) in star_dict.items():
        knr = k.replace(path_str + '.', '')
        if knr == k:
            data[path_str + '.' + k] = v
        else:
            ctx.gbc.say('set_flat_at_path:k(%s)->knr(%s)' %
                        (k, knr), verbosity=10)
            data[path_str + '.' + knr] = v
    return data


def set_path(ctx, path_str, value, data):
    """
    Sets the given key in the given dict object to the given value. If the
    given path is nested, child dicts are created as appropriate.
    Accepts either a dot-delimited path or an array of path elements as the
    `path` variable.
    """
    ctx.gbc.say('set_path:value:' + str(value) + ' at:' + path_str + ' in:',
                stuff=data, verbosity=1001)

    path = path_str.split('.')
    ctx.gbc.say('path:', stuff=path, verbosity=100)
    if len(path) > 1:
        destk = '.'.join(path[0:-1])
        lp = path[-1]
        ctx.gbc.say('destk:%s' % destk, verbosity=100)
        ctx.gbc.say('last:%s' % lp, verbosity=100)
        ctx.gbc.say('current keys:', stuff=data.keys(), verbosity=1001)
        if len(path) > 2:
            destk = unescape(ctx, destk)
        if destk not in data.keys():
            ctx.gbc.say('destk not in current keys:',
                        stuff=data.keys(), verbosity=1001)
            data[destk] = {}
            ctx.gbc.say('destk not added:', stuff=data, verbosity=1001)

        lp = unescape(ctx, lp)
        data[destk][lp] = value
        ctx.gbc.say('destk and val added:', stuff=data, verbosity=1001)
    else:
        path_str = unescape(ctx, path_str)
        data[path_str] = value
    ctx.gbc.say('set_path:res:', stuff=data, verbosity=1001)
    return data


def unflat(ctx, flattened, sep='.', index=1):
    ctx.gbc.say('unflattening', stuff=flattened, verbosity=101)
    proc = []
    flktmp = flattened
    if buts('flat') not in flattened:
        ctx.gbc.say('not a trace of a flat dict', verbosity=101)
        return flattened

    if not flattened[buts('flat')]:
        ctx.gbc.say('not a flat dict', verbosity=101)
        return flattened

    flat_left = True

    while flat_left:
        deep = 0
        keys = flktmp.keys()
        deep_keys = {}
        for k in keys:
            if k in proc:
                continue
            kl = len(k.split(sep))
            kls = str(kl)
            if kls not in deep_keys:
                deep_keys[kls] = []
            deep_keys[kls].append(k)
            if kl > deep:
                deep = kl
                deeps = kls
        ctx.gbc.say('deep:%d' % deep, verbosity=200)
        ctx.gbc.say('deep_keys:', stuff=deep_keys, verbosity=200)
        ctx.gbc.say('proc:', stuff=proc, verbosity=200)

        if deep == 1:
            # done
            flat_left = False
            break

        for k in deep_keys[deeps]:
            if not flat_left:
                continue
            if k in proc:
                continue
            if k.endswith(buts('listlen')):
                continue
            if k.endswith(buts('list')):
                list_base = k.replace(sep + buts('list'), '.*')
                destk = k.replace(sep + buts('list'), '')
                lval = get_flat_path(ctx, flktmp, list_base, [])
                templ = unflat_list(ctx, lval)
                ctx.gbc.say('list selected as dict "' + sep +
                            '*":', stuff=lval, verbosity=1001)
                ctx.gbc.say('list list from "' + sep + '*":',
                            stuff=templ, verbosity=1001)
                flktmp = set_path(ctx, destk, templ, flktmp)
                proc, flktmp = process_flk(ctx, k, proc, flktmp)
                list_lenk = k.replace(sep + buts('list'),
                                      sep + buts('listlen'))
                proc, flktmp = process_flk(ctx, list_lenk, proc, flktmp)
                list_len = lval[buts('listlen')]
                for index in range(int(list_len)):
                    list_item = k.replace(
                        sep + buts('list'), sep + str(index + 1))
                    proc, flktmp = process_flk(ctx, list_item, proc, flktmp)

        for k in deep_keys[deeps]:
            if not flat_left:
                continue
            if k in proc:
                continue
            if not k.endswith(buts('list')):
                # non lists
                flktmp = set_path(ctx, k, flktmp[k], flktmp)
                proc, flktmp = process_flk(ctx, k, proc, flktmp)

        count = 0
        new_keys = flktmp.keys()
        for k in new_keys:
            kl = k.split(sep)
            if len(kl) == 1:
                count += 1
        if count == len(new_keys):
            flat_left = False

    flktmp[buts('flat')] = False
    # WA: last part dest keeps exploding, maybe give deep to set path!?
    fat_res = {}
    for k in flktmp.keys():
        fat_res[unescape(ctx, k)] = flktmp[k]

    ctx.gbc.say('unflattening:res:', stuff=fat_res, verbosity=101)

    return fat_res


def get_flat_path(ctx, current, kpath, default_not_existing=None, sep='.'):
    ctx.gbc.say('get_flat_path:' + kpath, verbosity=10)
    ctx.gbc.say('get_flat_path:' + kpath, stuff=current, verbosity=101)
    flattened = flat(ctx, current)
    if kpath in flattened:
        res = flattened[kpath]
        ctx.gbc.say('get_flat_path:res:' + str(res), verbosity=10)
        return res
    else:
        if kpath.endswith(sep + '*'):
            select = {}
            for k in flattened.keys():
                ctx.gbc.say('get flat path:k:' + k, verbosity=102)
                if k.startswith(kpath[:-2]) and k != kpath:
                    ctx.gbc.say('selecting path:' + kpath +
                                ' k:' + k, verbosity=101)
                    kpath_esc_last_dot = kpath.replace(
                        sep + '*', '___bts_escsep')
                    kpath_last_dot = kpath.replace(sep + '*', sep)

                    restk = k.replace(kpath_esc_last_dot, '')
                    restk = restk.replace(kpath_last_dot, '')
                    select[restk] = flattened[k]
            if select:
                select[buts('flat')] = True
                select[buts('flat_star_select')] = True
                select[buts('flat_star_path')] = kpath
                ctx.gbc.say('get_flat_path:star:' + kpath,
                            stuff=select, verbosity=101)
                return select
    return default_not_existing
