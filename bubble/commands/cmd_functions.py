# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import pass_bubble
from ..cli import STAGES

from ..util.cli_misc import load_rule_functions

from ..functions import get_registered_rule_functions


@click.command('functions', short_help='Functions.')
@click.option('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@pass_bubble
def cli(ctx, stage):
    """Show the functions that are available, bubble system and custom."""
    if not ctx.bubble:
        ctx.say_yellow(
            'There is no bubble present, will not show any transformer functions')
        raise click.Abort()
    rule_functions = get_registered_rule_functions()
    ctx.gbc.say('before loading functions:' + str(len(rule_functions)))
    load_rule_functions(ctx)
    ctx.gbc.say('after loading functions:' + str(len(rule_functions)))
    ctx.gbc.say('rule_functions:', stuff=rule_functions, verbosity=10)
    rule_functions.set_parent(ctx.gbc)
    for f in rule_functions:
        ctx.say('fun: ' + f, verbosity=1)
    ctx.gbc.say('funs: ', stuff=rule_functions.get_rule_functions(), verbosity=100)

    return True
