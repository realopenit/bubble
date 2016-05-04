# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import os
import sys
import arrow
import click
import pprint

from . import metadata
from . import Bubble
from .util.cfg import get_config
from .util.cli_misc import utf8_only, file_exists
from .util.profiling import start_profile, write_profile

import six
if six.PY2:
    from __builtin__ import ImportError

# do not show if verbosity is above current verbose on Bubble(), todo USE magic
VERBOSE = 0
# do not show verbosities above the bar, todo USE magic
VERBOSE_BAR = 100


# definitions for configuration files relative to bubble directory
DOT_BUBBLE = '.bubble'
CONFIG_YAML = 'config/config.yaml'

# definitions for possible lists op options
STAGES = ['PROD', 'ACC', 'TEST', 'DEV', 'MOCK']

# also dataset, but that's another kind of 'storage'
STORAGE_TYPES = ['json','jsonl']

STEPS = ['pulled', 'uniq_pull', 'uniq_push',
         'push', 'pushed', 'store', 'stats']


CONTEXT_SETTINGS = dict(auto_envvar_prefix='BUBBLE')


def make_gbc(verbose, verbose_bar):
    general_bubble_ctx = Bubble(name='Bubble(gbc)',
                                verbose=verbose,
                                verbose_bar=verbose_bar)
    general_bubble_ctx.say('gbc here', verbosity=99)
    return general_bubble_ctx

GLOBAL_START_ARROW = arrow.now()
###############################################################################
BUBBLE_CLI_GLOBALS = {}
BUBBLE_CLI_GLOBALS['start_arrow'] = GLOBAL_START_ARROW
BUBBLE_CLI_GLOBALS['dot_bubble'] = DOT_BUBBLE
BUBBLE_CLI_GLOBALS['config_yaml'] = CONFIG_YAML
BUBBLE_CLI_GLOBALS['stages'] = STAGES
BUBBLE_CLI_GLOBALS['storage_types'] = STORAGE_TYPES
BUBBLE_CLI_GLOBALS['steps'] = STEPS
###############################################################################

#todo: magic
greeting = """Hi there,
i'm a inside a Bubble,
my name is %s.

a.k.a: API in the middle

Helps you where two of your "complex" services don't play well with each other.
And where you need get some information from A to B,
while transforming or filtering the information,  simply put:
 >>>A:pull>>>bubble:transform>>>B:push>>>
consider me your "small information" manager in between your big data and ESB(s),ETL(s).

Create a bubble, make the information flow and start bubbling .o.O.o.
"""


class BubbleCli(Bubble):

    """the Bubble for the Command Line Interface,

       this the bubble to be passed around as the 'ctx' for the cli commands"""

    def __init__(self,
                 home=None, verbose=VERBOSE,
                 verbose_bar=VERBOSE_BAR):
        Bubble.__init__(self, 'BubbleCli', verbose, verbose_bar)
        self.GLOBALS = BUBBLE_CLI_GLOBALS
        self.debug = False
        # for general logging purposes
        self.gbc = make_gbc(verbose=verbose,
                            verbose_bar=verbose_bar)

        self.GLOBALS['gbc'] = self.gbc

        self.adaptive_verbose = False

        self.say_green(greeting % (self.name), verbosity=101)
        utf8_only(self)
        if verbose:
            self.gbc.say('current bubble path:' + os.path.abspath(home),
                         verbosity=2)

        self.config = {}  # runtime config (dynamic via options)
        self.cfg = {}     # static config

        self.set_verbose(verbose)
        self.set_verbose_bar(verbose_bar)

        self.debug = False
        self.bubble = False
        if home:
            self.home = home
        else:
            self.home = os.getcwd()

        self.env = os.environ

        if file_exists(self, self.home + '/' + DOT_BUBBLE):
            with open(self.home + '/' + DOT_BUBBLE) as dot_bubble:
                content = dot_bubble.read()
                if content.startswith('bubble='):
                    self.bubble = content
                    self.say('.bubble content:', stuff=content, verbosity=100)
                if not content.startswith('bubble=' + metadata.version):
                    if verbose:
                        self.say_yellow(
                            'This Bubble version does not match current' +
                            ' bubble cli tool version:' + metadata.version,
                            verbosity=2)
                        self.say_yellow(
                            'Please see release notes and check' +
                            'if significant changes content:\n' + content,
                            verbosity=2)
                        self.say_green(
                            'You can run: bubble upgrade <old-version>',
                            verbosity=2)

        if not self.bubble:
            self.say_yellow('There is no Bubble in %s' % home)
            self.say_green('For a  new bubble try: bubble init')
            return

        if self.bubble:
            cfg_file = self.home + '/' + CONFIG_YAML
            if file_exists(self.gbc, cfg_file):
                self.cfg = get_config(self.gbc, cfg_file)
            self.gbc.say('cfg:', stuff=self.cfg, verbosity=10)

        if not self.cfg:
            self.say_red('Could not find or read configuration')

    def set_config(self, key, value):
        self.config[key] = value
        if self.verbose >= VERBOSE:
            click.echo('  config[%s] = %s' % (key, value), file=sys.stderr)

    def say(self, msg, verbosity=1, stuff=None):
        self._msg(msg=msg,
                  verb='cli.say',
                  verbosity=verbosity,
                  stuff=stuff,
                  from_cli=True)
        if verbosity <= self.get_verbose():
            click.echo(msg)
            if stuff:
                click.echo('  stuff:')
                click.echo(pprint.pformat(stuff))

    def _say_color(self, msg, verbosity=0, stuff=None, fgc='green'):
        self._msg(msg=msg,
                  verb='cli._say_color',
                  verbosity=verbosity,
                  stuff=stuff,
                  from_cli=True)
        if verbosity <= self.get_verbose():
            click.secho(msg, fg=fgc)
            if stuff:
                click.echo('  stuff:')
                click.secho(pprint.pformat(stuff), fg=fgc)

    # shortcuts for stoplight colors
    def say_green(self, msg, verbosity=0, stuff=None):
        self._say_color(msg, verbosity, stuff, 'green')

    def say_yellow(self, msg, verbosity=0, stuff=None):
        self._say_color(msg, verbosity, stuff, 'yellow')

    def say_red(self, msg, verbosity=0, stuff=None):
        self._say_color(msg, verbosity, stuff, 'red')

    def __repr__(self):
        return '<BubbleCli %s@%s since: %s>' % (self.name,
                                                self.home,
                                                self.birth)
    def __exit__(self, exit_type=None, value=None, traceback=None):
        self.say('exit',stuff=BUBBLE_CLI_GLOBALS,verbosity=111)
        if BUBBLE_CLI_GLOBALS['profiling']:
            write_profile()



pass_bubble = click.make_pass_decorator(BubbleCli, ensure=True)

bubble_lib_dir = os.path.dirname(__file__)
commands_path = os.path.join(bubble_lib_dir, 'commands')
cmd_folder = os.path.abspath(commands_path)


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        # ctx.say('list_commands', verbosity=100)
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and \
               filename.startswith('cmd_'):
                rv.append(filename[4:-3])
                # ctx.say('list_commands:'+filename, verbosity=100)

        rv.sort()
        return rv

    def get_command(self, ctx, name):
        # ctx.say('get_command:'+name, verbosity=100)
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__('bubble.commands.cmd_' + name,
                             None, None, ['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI,
               context_settings=CONTEXT_SETTINGS)
@click.option('--bubble-home',
              '-h',
              envvar='BUBBLE_HOME',
              default='.',
              metavar='PATH',
              help='sets bubble home location.')
@click.option('--config',
              '-c',
              nargs=2,
              multiple=True,
              metavar='KEY VALUE',
              help='overrides a config key/value pair.')
@click.option('--verbose',
              '-v',
              type=int,
              default=1,
              help='sets verbose, bigger is more detail')
@click.option('--barverbose',
              '-b',
              type=int,
              default=-1,
              help='sets a bar, only show messages up to the bar')
@click.option('--profile',
              '-p',
              envvar='BUBBLE_PROFILE',
              is_flag=True,
              default=False,
              help='run bubble with profiling.')
@click.version_option(metadata.version)
@click.pass_context
def cli(ctx, bubble_home, config, verbose, barverbose, profile):
    """Bubble: command line tool for bubbling information between services

    .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.\n
    Making single point to point API connections:\n
    _________________>>>>>>>>>pump>>>>>>>>>>>>>_____________________\n
    (source-service)->pull->(transform)->push->(target-service)\n
    _________________>>>>>>>>>pump>>>>>>>>>>>>>_____________________\n
    bubble can:\n
    * pull data from the source client\n
    * transform the data with flexible mapping and filtering rules\n
    * rules can use (custom) rule functions\n
    * push the result to  the target client\n

    A Bubble can process a list of basic python dicts(LOD),
    which are persisted in files or a database,
    for each step and stage that produced it.

    The only requirement for the service clients is that they have a:\n
    * source sevice: pull method which provides a LOD\n
    * target sevice: push method which accepts a dict\n


    A Bubble tries hard not to forget any step that has taken place,
    the results of any completed step is stored in a file,
    in the remember directory inside the Bubble.

    Without rules and bubble will "just" copy.\n

    Commands marked with (experimental) might work,
    but have not fully "behave" tested yet.

    For help on a specific command you can use:
        bubble <cmd> --help

    Create a bubble, make the information flow and start bubbling.\n
    .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.\n
    """

    # Create a bubble object and remember it as the context object.
    # From this point onwards other commands can refer to it by using the
    # @pass_bubble decorator.

    cis = ctx.invoked_subcommand
    initing = False

    if cis == 'stats':
        nagios = False
        try:
            monitor = ctx.args[ctx.args.index('--monitor') + 1]
            if monitor == 'nagios':
                nagios = True
        except (ValueError, IndexError):
            pass
        if nagios:
            verbose = 0

    BUBBLE_CLI_GLOBALS['profiling'] = profile
    if profile:
        start_profile()

    global VERBOSE
    VERBOSE = verbose

    global VERBOSE_BAR
    VERBOSE_BAR = barverbose

    if bubble_home != '.':
        bubble_home_abs = os.path.abspath(bubble_home)
    else:
        bubble_home_abs = os.path.abspath(os.getcwd())

    if cis == 'init':
        initing = True
    if initing:
        if not os.path.exists(bubble_home_abs):
            os.makedirs(bubble_home_abs)

    if os.path.exists(bubble_home_abs):
        os.chdir(bubble_home_abs)
        ctx.obj = BubbleCli(home=bubble_home_abs,
                            verbose=verbose,
                            verbose_bar=barverbose)
    else:
        click.echo('Bubble home path does not exist: ' + bubble_home_abs)
        raise click.Abort()

    BUBBLE_CLI_GLOBALS['full_command'] = ' '.join(sys.argv)

    for key, value in config:
        ctx.obj.set_config(key, value)
    if not ctx.obj.bubble and not initing:
        ctx.obj.say_yellow('There is no bubble in %s' %
                           bubble_home_abs, verbosity=10)
        ctx.obj.say('You can start one with: bubble init', verbosity=10)
