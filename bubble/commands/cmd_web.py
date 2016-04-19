# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click
from ..cli import pass_bubble
from ..cli import STAGES
from ..util.cli_misc import get_server


@click.command('web', short_help='Web interface(experimental).')
@click.option('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@click.option('--port', '-p', default='11211', help='set the port')
@pass_bubble
def cli(ctx, stage, port):
    """Web interface(experimental)."""
    if not ctx.bubble:
        ctx.say_yellow('There is no bubble present, will not listen')
        raise click.Abort()
    gbc = ctx.gbc
    WEB = None
    if stage in STAGES:
        STAGE = ctx.cfg.CFG[stage]
        if 'SERVER'  in STAGE:
            SERVER=STAGE.SERVER
            if 'WEB' in SERVER:
                WEB=SERVER.WEB

    if not WEB:
        ctx.say_red('There is no SERVER.WEB in stage:' + stage)
        ctx.say_yellow('please check configuration in ' +
                       ctx.home + '/config/config.yaml')
        raise click.Abort()

    web_server = get_server(gbc, WEB, ctx.home)

    try:
        # TODO: bg &
        # src_listening = web_server.start_web(ctx=gbc,
        web_server.start_web(ctx=gbc,
                             port=port,
                             stage=stage)
    except Exception as e:
        ctx.say_red(
            'cannot start web server e ' + WEB)
        ctx.say_red(str(e))
        raise click.Abort('cannot listen')
