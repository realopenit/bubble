# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import STAGES

from ..commands.cmd_pull import cli as pull
from ..commands.cmd_transform import cli as transform
from ..commands.cmd_push import cli as push


@click.command('pipe', short_help='Pull, Transform, Push, streaming inside a pipe(experimental).')
@click.option('--amount', '-a', type=int, default=-1, help='set the amount to pump')
@click.option('--index', '-i', type=int, default=-1, help='set the starting index')
@click.option('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@click.pass_context
def cli(ctx, amount, index, stage):
    """Pull, Transform, Push,streaming inside a pipe(experimental)."""
    ctx.obj.say_green('Starting Streaming Pipe')
    res_pull = ctx.invoke(pull, amount=amount, index=index, stage=stage)
    res_tra = False
    if res_pull:
        # amount to transform can be less (or more)
        res_tra = ctx.invoke(
            transform, amount=amount, index=index, stage=stage)
    if res_tra:
        # amount to push can be less (or more)
        res_push = ctx.invoke(push, amount=amount, index=index, stage=stage)
    if res_pull and res_tra and res_push:
        ctx.obj.say_green('Streaming Pipe finsished')
        return True
    return False
