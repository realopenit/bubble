# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import pass_bubble
from ..util.cfg import put_config, BubbleDoct
from ..util.flat_dict import flat, unflat, get_flat_path


@click.command('config',
               short_help='show or set the configuration')
@click.option('--setkv',
              '-s',
              nargs=2,
              multiple=True,
              metavar='KEY VALUE',
              help='Sets  a config key/value pair.')
@click.option('--copyk',
              '-c',
              nargs=2,
              multiple=True,
              metavar='SRCKEY DESTKEY',
              help='Copies a config key to a dest key.')
@click.option('--delk',
              '-d',
              nargs=1,
              multiple=False,
              metavar='KEY',
              help='Deletes  a config key, or key.* "branch"')
@pass_bubble
def cli(ctx, setkv, copyk, delk):
    """Show or change the configuration"""

    if not ctx.bubble:
        ctx.say_yellow(
            'There is no bubble present, will not show or set the config')
        raise click.Abort()

    new_cfg = flat(ctx, ctx.cfg)
    ctx.say('current config', stuff=ctx.cfg, verbosity=10)
    ctx.say('current flat config with meta', stuff=new_cfg, verbosity=100)
    new_cfg_no_meta = {}
    meta_ends = ['_doct_as_key',
                 '_doct_level',
                 '___bts_flat_',
                 '___bts_flat_star_path_',
                 '___bts_flat_star_select_']

    lkeys = list(new_cfg.keys())
    for k in lkeys:
        addkey = True
        # ctx.say('k:'+k)
        if k.startswith('___bts_'):
            addkey = False
        for meta_end in meta_ends:
            if k.endswith(meta_end):
                addkey = False
        if addkey:
            # ctx.say('adding k:'+k)
            new_cfg_no_meta[k] = new_cfg[k]
        else:
            pass
            # ctx.say('not adding meta k:'+k)
    ctx.say('current flat config without metakeys',
            stuff=new_cfg_no_meta,
            verbosity=3)
    if not setkv and not copyk and not delk:
        ctx.say('current configuration')
        for k, v in new_cfg_no_meta.items():
            ctx.say(' '+k+': '+str(v))

    modified = 0
    if setkv:
        for key, value in setkv:
            new_cfg[str(key)] = str(value)
            modified += 1
    if copyk:
        for srckey, destkey in copyk:
            if srckey.endswith('.*'):
                src_val = get_flat_path(ctx, new_cfg, srckey)
                for k in src_val:
                    # TODO: use magic for sep
                    sep = '.'
                    new_cfg[str(destkey + sep + k)] = str(src_val[k])
                modified += 1
            else:
                if srckey in new_cfg:
                    new_cfg[str(destkey)] = new_cfg[srckey]
                    modified += 1

    if delk:
        if delk.endswith('.*'):
            # fix PY3: RuntimeError: dictionary changed size during iteration
            lkeys = list(new_cfg.keys())
            for k in lkeys:
                if k.startswith(delk[:-2]):
                    del(new_cfg[k])
                    modified += 1

        else:
            if delk in new_cfg:
                del(new_cfg[delk])
                modified += 1

    if modified:
        ctx.say('new flat config', stuff=new_cfg, verbosity=100)
        fat_cfg = unflat(ctx, new_cfg)
        ctx.say('new config, #changes:'+str(modified), verbosity=3)
        ctx.say('new config', stuff=fat_cfg, verbosity=30)
        fat_cfg = unflat(ctx, new_cfg)
        doct_fat_cfg = BubbleDoct(fat_cfg)
        ctx.say('new config fat doct', stuff=doct_fat_cfg, verbosity=100)
        res = put_config(ctx, YCFG=BubbleDoct(doct_fat_cfg))
        ctx.say('put config res:', stuff=res, verbosity=10)

    return True
