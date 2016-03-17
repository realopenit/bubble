# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import os

import click
import arrow

from .. import metadata
from ..cli import pass_bubble

from ..util.cli_misc import create_dir


from ..util.examples import (get_example_rules_bubble,
                             get_example_configuration,
                             get_example_rule_functions,
                             get_example_client_pull,
                             get_example_client_push)

default_given_name = 'BoB'  # Bubble of Bubbles


@click.command('init', short_help='Initializes a new bubble.')
@click.argument('given_name', '-n', required=False, type=str, default=default_given_name)
@click.option('--demo', '-d', is_flag=True, default=True, help='Create a demo bubble from examples.')
@pass_bubble
def cli(ctx, given_name, demo):
    """Initializes a bubble."""
    path = None
    if path is None:
        path = ctx.home
        bubble_file_name = path + '/.bubble'
        config_file = path + '/config/config.yaml'

        if os.path.exists(bubble_file_name) and os.path.isfile(bubble_file_name):
            ctx.say_yellow(
                'There is already a bubble present, will not initialize bubble in:' + path)
            return
        else:
            given_name = '(((' + given_name + ')))'
            with open(bubble_file_name, 'w') as dot_bubble:
                dot_bubble.write('bubble=' + metadata.version + '\n')
                dot_bubble.write('name=' + given_name + '\n')
                dot_bubble.write('home=' + ctx.home + '\n')
                dot_bubble.write(
                    'local_init_timestamp=' + str(arrow.utcnow()) + '\n')
                # aka date_of_birth
                dot_bubble.write(
                    'local_creator_user=' + str(os.getenv('USER')) + '\n')
                dot_bubble.write(
                    'local_created_in_env=' + str(os.environ) + '\n')
                ctx.say_green('Initialised a  new bubble in [%s]' %
                              click.format_filename(bubble_file_name))

        create_dir(ctx, path + '/config/')
        create_dir(ctx, path + '/logs/')
        create_dir(ctx, path + '/export/')
        create_dir(ctx, path + '/import/')
        create_dir(ctx, path + '/remember/')
        create_dir(ctx, path + '/remember/archive')

        with open(config_file, 'w') as cfg_file:
            cfg_file.write(get_example_configuration())
            ctx.say_green('Created an example configuration in %s' %
                          click.format_filename(config_file))

        rules_file = path + '/config/rules.bubble'
        with open(rules_file, 'w') as rules:
            rules.write(get_example_rules_bubble())
            ctx.say_green('Created an example rules in [%s]' %
                          click.format_filename(rules_file))

        rule_functions_file = path + '/custom_rule_functions.py'
        with open(rule_functions_file, 'w') as rule_functions:
            rule_functions.write(get_example_rule_functions())
            ctx.say_green('Created an example rule_functions in [%s]' %
                          click.format_filename(rule_functions_file))

        src_client_file = path + '/mysrcclient.py'
        with open(src_client_file, 'w') as src_client:
            src_client.write(get_example_client_pull())
            ctx.say_green('Created source example client with pull method [%s]' %
                          click.format_filename(src_client_file))
        tgt_client_file = path + '/mytgtclient.py'
        with open(tgt_client_file, 'w') as tgt_client:
            tgt_client.write(get_example_client_push())
            ctx.say_green('Created an target example client with push method [%s]' %
                          click.format_filename(src_client_file))

        ctx.say_green(
            'Bubble initialized, please adjust your configuration file')
