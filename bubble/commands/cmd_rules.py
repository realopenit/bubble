# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import click

from ..cli import pass_bubble
from ..cli import STAGES

from ..util.store import get_bubble
from ..transformer import Transformer


@click.command('rules', short_help='Rules.')
@click.option('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@pass_bubble
def cli(ctx, stage):
    """Show transformer rules"""
    if not ctx.bubble:
        ctx.say_yellow('There is no bubble present, ' +
                       'will not show any transformer rules')
        raise click.Abort()

    path = ctx.home + '/'
    RULES = None
    ctx.say('Stage:'+stage, verbosity=10)
    if stage in STAGES:
        if stage in ctx.cfg.CFG:
            STAGE = ctx.cfg.CFG[stage]
            ctx.say('Stage found:', stuff=STAGE,verbosity=100)


        if 'TRANSFORM' in STAGE:
            TRANSFORM = STAGE.TRANSFORM
            ctx.say('Transform found:', stuff=TRANSFORM, verbosity=100)

            if 'RULES' in TRANSFORM:
                RULES = TRANSFORM.RULES
                ctx.say('Rules found:', stuff=RULES, verbosity=100)


    if not RULES:
        ctx.say_red('There is no TRANSFORM.RULES in stage:' + stage)
        ctx.say_yellow('please check configuration in ' +
                       ctx.home + '/config/config.yaml')
        raise click.Abort()

    if type(RULES) == str and RULES.endswith('.bubble'):
        ctx.say('loading rules',verbosity=10)
        rules = get_bubble(ctx, path + RULES)
        rule_type = 'bubble'
        transformer = Transformer(rules=rules,
                                  rule_type=rule_type,
                                  bubble_path=path,
                                  verbose=ctx.get_verbose())
        rules = transformer._rules.get_rules()
        ctx.say('current number of rules:' + str(len(rules)),
                verbosity=1)
        for r in rules:
            ctx.say('rule: ' + str(r), verbosity=1)

        ctx.gbc.say('rules: ', stuff=rules, verbosity=100)
    else:
        ctx.say('no rules!')

    return True
