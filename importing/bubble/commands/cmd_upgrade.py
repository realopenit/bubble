# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from .. import metadata

from ..cli import pass_bubble
from ..util.examples import get_example_rule_functions, get_example_rules_bubble
from ..util.cli_misc import create_dir, file_exists


@click.command('upgrade',
               short_help='Upgrade the current bubble(experimental)')
@click.option('--oldversion',
              '-o',
              is_flag=True,
              default=True,
              help='upgrade from version to current verion :' + metadata.version)
@pass_bubble
def cli(ctx, oldversion):
    """Upgrade the current bubble, should mimic init as much as possible(experimental)"""
    # print ctx.bubble
    path = ctx.home
    bubble_file_name = path + '/.bubble'
    config_file = path + '/config/config.yaml'

    if file_exists(bubble_file_name):
        pass
    else:
        with open(bubble_file_name, 'w') as dot_bubble:
            dot_bubble.write('bubble=' + metadata.version)
            dot_bubble.write('\nconfig=' + config_file)

        ctx.say_green('Initialised a  new bubble in [%s]' %
                      click.format_filename(bubble_file_name))

    create_dir(ctx, path + '/config/')
    create_dir(ctx, path + '/logs/')
    create_dir(ctx, path + '/export/')
    create_dir(ctx, path + '/import/')
    create_dir(ctx, path + '/remember/')
    create_dir(ctx, path + '/remember/archive')

    rules_file = path + '/config/rules.bubble'
    if file_exists(bubble_file_name):
        pass
    else:
        with open(rules_file, 'w') as rules:
            rules.write(get_example_rules_bubble())
            ctx.say_green('Created an example rules in [%s]' %
                          click.format_filename(rules_file))

    rule_functions_file = path + '/custom_rule_functions.py'
    if file_exists(rule_functions_file):
        pass
    else:
        with open(rule_functions_file, 'w') as rule_functions:
            rule_functions.write(get_example_rule_functions())
            ctx.say_green('Created an example rule_functions in [%s]' %
                          click.format_filename(rule_functions_file))

    ctx.say_green('Bubble upgraded')
