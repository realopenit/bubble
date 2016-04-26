# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import STAGES

from ..commands.cmd_pull import cli as pull
from ..commands.cmd_transform import cli as transform
from ..commands.cmd_push import cli as push

@click.command('pump', short_help='Pull, Transform, Push.')
@click.option('--amount', '-a', type=int, default=-1, help='set the amount to pump')
@click.option('--index', '-i', type=int, default=-1, help='set the starting index')
@click.option('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@click.pass_context
def cli(ctx, amount, index, stage):
    """Pull, Transform, Push."""
    res_pull = ctx.invoke(pull, amount=amount, index=index, stage=stage)

    do_transform = False
    if stage in STAGES:
        if stage in ctx.obj.cfg.CFG:
            if "TRANSFORM" in ctx.obj.cfg.CFG[stage]:
                do_transform = True

    res_tra = False
    if res_pull:
        # amount to transform can be less (or more)
        if do_transform:
            res_tra = ctx.invoke(transform, amount=amount, index=index, stage=stage)
        else:
            res_tra = True

    if res_tra:
        # amount to push can be less (or more)
        res_push = ctx.invoke(push, amount=amount, index=index, stage=stage)

    if res_pull and res_tra and res_push:
        ctx.obj.say_green('Pumping finsished')
        return True
    return False
