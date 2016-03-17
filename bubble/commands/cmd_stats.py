# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

from pprint import pformat as pf

import click
from ..cli import pass_bubble
# from ..cli import general_bubble_ctx as gbc
from ..cli import STAGES
from ..util.cli_misc import bubble_lod_load, _find_lod_gen


def k0(d, k):
    if k in d:
        return d[k]
    return 0

@click.command('stats', short_help='Basic statistics and monitoring.')
@click.option('--stage', '-s', default='DEV', help='set the staging :' + ','.join(STAGES))
@click.option('--monitor', '-m', default=None, help='set the monitoring output format')
@click.option('--full', '-f', is_flag=True, default=False, help='set the full statistics option')
@pass_bubble
def cli(ctx, monitor, full, stage):
    """Basic statistics"""
    if not ctx.bubble:
        msg = 'There is no bubble present, will not search stats'
        if monitor:
            ctx.say_yellow('Unknown - ' + msg, 0)
            raise SystemExit(3)
        else:
            ctx.say_yellow(msg)
        raise click.Abort()

    stats = {}
    stats_found = False
    flowing_full = False
    flowing_decrease = False
    flowing_increase = False
    errors = False

    loader = bubble_lod_load(ctx, 'stats', stage)
    lod_gen = _find_lod_gen(ctx, loader)
    if lod_gen:
        last_stats = {}
        ctx.say('lod_gen', stuff=lod_gen)
        for stats_data in lod_gen:
            last_stats = stats_data
        if last_stats:
            ctx.say('found last_stats:', stuff=last_stats, verbosity=10)

    try:
        ctx.say('trying:last stats:', stuff=last_stats, verbosity=10)
        if last_stats:
            l = last_stats
            stats['pull_err'] = k0(l, 'pulled_stat_error_count')
            stats['pull_total'] = k0(l, 'pulled_stat_total_count')

            stats['trans_err'] = k0(l, 'transformed_stat_error_count')
            stats['trans_total'] = k0(l, 'transformed_stat_total_count')

            stats['push_err'] = k0(l, 'pushed_stat_error_count')
            stats['push_total'] = k0(l, 'pushed_stat_total_count')
            stats_found = True
        else:
            stats_found = False

        ctx.say('stats:', stuff=stats, verbosity=10)

        if stats_found and stats['pull_err'] > 0 or \
                stats['trans_err'] > 0 or \
                stats['push_err'] > 0:
            errors = True
        if stats_found and stats['pull_total'] == stats['trans_total'] and \
                stats['trans_total'] == stats['push_total']:
            flowing_full = True
        if stats_found and stats['pull_total'] >= stats['trans_total'] >= stats['push_total']:
            flowing_decrease = True
        if stats_found and stats['pull_total'] <= stats['trans_total'] <= stats['push_total']:
            flowing_increase = True
    except KeyError as stat_key_error:
        errors = True
        ctx.gbc.cry('cannot create status from last stats', stuff=stat_key_error)

    if full:
        ctx.say_yellow('Stats full')
        ctx.say_yellow('Full flow:' + str(flowing_full))
        ctx.say_yellow('Flowing decrease:' + str(flowing_decrease))
        ctx.say_yellow('Flowing increase:' + str(flowing_increase))
        ctx.say_yellow('Errors:' + str(errors))
        ctx.say_yellow('totals:')
        ctx.say_yellow(pf(stats, indent=8))

    if monitor == 'nagios' or full:

        """
        for Numeric Value Service Status Status Description, please see:
        https://nagios-plugins.org/doc/guidelines.html#AEN78
        0 OK The plugin was able to check the service and
          it appeared to be functioning properly
        1 Warning The plugin was able to check the service,
          but it appeared to be above some "warning" threshold or did not appear to be working properly
        2 Critical The plugin detected that either the service was not running or
          it was above some "critical" threshold
        3 Unknown Invalid command line arguments were supplied to the plugin or
          low-level failures internal to the plugin (such as unable to fork, or open a tcp socket)
          that prevent it from performing the specified operation. Higher-level errors (such as name resolution errors,
          socket timeouts, etc) are outside of the control of plugins and
          should generally NOT be reported as UNKNOWN states.

        http://nagios.sourceforge.net/docs/3_0/perfdata.html
        http://nagios.sourceforge.net/docs/3_0/pluginapi.html
        """
        if stats_found:
            templ_nagios = 'pull: %d %d transform: %d  %d push: %d %d '
            res_nagios = templ_nagios % (stats['pull_total'],
                                         stats['pull_err'],
                                         stats['trans_total'],
                                         stats['trans_err'],
                                         stats['push_total'],
                                         stats['push_err']
                                         )
        else:
            res_nagios = 'Cannot find or read stats'

        if not stats_found:
            print('Unknown - ' + res_nagios)
            raise SystemExit(3)
            # return

        if not errors and flowing_full:
            print('Ok - ' + res_nagios)
            return

        # magister and databyte with amount
        if not errors and flowing_decrease:
            print('Ok - ' + res_nagios)
            return

        if not errors and not flowing_full:
            print('Warning - ' + res_nagios)
            raise SystemExit(1)
            # return

        if errors:
            print('Critical - ' + res_nagios)
            raise SystemExit(2)
            # return
    return False
