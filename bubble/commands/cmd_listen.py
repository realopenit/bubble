# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import arrow
import click

from ..cli import pass_bubble
# todo remove import and use ctx.GLOBALS['STAGES'] in all cmds
from ..cli import STAGES

from ..util.cli_misc import get_server


@click.command('listen', short_help='listen to pull/push requests(experimental).')
@click.option('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@pass_bubble
def cli(ctx, stage):
    """listen to push requests for src and pull requests from target (experimental)"""

    if not ctx.bubble:
        ctx.say_yellow('There is no bubble present, will not listen')
        raise click.Abort()

    SRC = None
    if stage in STAGES:
        try:
            SRC = ctx.cfg.CFG[stage].SOURCE
        except KeyError:
            pass

    if not SRC:
        ctx.say_red('There is no SOURCE in stage:' + stage)
        ctx.say_yellow('please check configuration in ' +
                       ctx.home + '/config/config.yaml')
        raise click.Abort()

    if 'SERVER' not in SRC:
        ctx.say_red('There is no SOURCE.SERVER in stage:' + stage)
        raise click.Abort()

    src_server = get_server(SRC.SERVER, ctx.home)

    # connect storage / pipeline to target via transform
    # write state listening on port etc into
    def message_handler(**m):
        print(str(arrow.now), str(m))
        return True, 'handled'

    try:
        # TODO: bg &
        # src_listening = src_server.listen(cfg=SRC,
        src_server.listen(cfg=SRC,
                          push_handler=message_handler,
                          pull_handler=message_handler)
    except Exception as e:
        ctx.say_red(
            'cannot listen from source client bubble.clients.' + SRC.SERVER)
        ctx.say_red(str(e))
        raise click.Abort('cannot listen')
