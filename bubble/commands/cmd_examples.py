# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import pass_bubble
from ..util.examples import all_examples_functions

@click.command('examples',
               short_help='Show example for doing some task in bubble(experimental)')
@click.option('--name',
              '-n',
              default=None,
              help='show the example with the name')
@click.option('--all',
              '-a',
              is_flag=True,
              default=False,
              help='show all the examples')
@pass_bubble
def cli(ctx, name,all):
    """Show example for doing some task in bubble(experimental)"""
    ctx.gbc.say('all_example_functions',stuff=all_examples_functions, verbosity=1000)

    for example in all_examples_functions:
        if all or (name and example['name'] == name):
            if all:
                ctx.gbc.say('example',stuff=example, verbosity=100)
                name = example['name']
            #click.echo_via_pager(example['fun']())
            click.echo("#"*80)
            click.echo("### start of bubble example: "+name)
            click.echo("#"*80)
            click.echo(example['fun']())
            click.echo("#"*80)
            click.echo("### end of bubble example: "+name)
            click.echo("#"*80)
            click.echo()

        else:
            click.echo("available example: " + example['name'])

