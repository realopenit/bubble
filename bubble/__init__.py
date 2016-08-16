# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

import os
import sys
import arrow

#orderdict needed for structlog
sys_version_str='.'.join((str(s) for s in sys.version_info[0:3]))
if sys_version_str=='2.6.9':
    import collections
    from ordereddict import OrderedDict
    collections.OrderedDict=OrderedDict
else:
    from collections import OrderedDict


BUBBLE_START_ARROW=arrow.now()

from structlog import get_logger
blog = get_logger()

from . import metadata

"""bubble information from one to another service,
with rule based transformations"""
BUBBLE_SIMPLE_LOGO = """
#:
#:                            .........
#:                     ....:::::::::::::::....
#:                 ...::::::''''''''''''':::::...
#:              ..::::''''                 '''':::..
#:            .::::''                          '':::::.
#:          .:::''  |                          |   '':::.
#:         .::''    |                          |      ''::.
#:       .:::'      |------>--TRANSFORM-->-----|       ':::.
#:      .:::'       |in:                       |        ':::.
#:      .::'        |{"hello":"greetings!"}    |          '::.
#:     .:::         |                          |          :::.
#:     :::.  PULL > |>>> hello >>> >>> hi >>>  |  >PUSH   .:::
#:     :::.         |     out:                 |          .:::
#:      :::.        |     {"hi":"greetings!"}  |          .:::
#:      ':::        |------>--TRANSFORM-->-----|         :::'
#:       ':::.      |                          |       .:::'
#:        ':::.     |                          |      .:::'
#:          ':::.   |                          |    .:::'
#:           '':::..|                          | ..:::''
#:             ''::::....                   ...::::''
#:                ''::::::.................:::::''
#:                    '''':::::::::::::::::''''
#:                         '''''''''''''''
#:
"""

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright


class Bubble(object):

    """ puts a tiny bubble of reality into existence """
    name = None
    _parent = None
    _children = []

    birth = None
    home = None

    _bubble_lib_dir = None

    debug = False

    _verbose = 0
    _verbose_bar = 0

    adaptive_verbose = True
    _msg_stats = {}
    _total_verbose = 0
    _total_verbose_bar = 0
    _total_verbose_self = 0

    def __init__(self,
                 name='NoName',
                 verbose=0,
                 verbose_bar=1,
                 parent=None,
                 logfile='',
                 statistics=False):
        self.say('base.Bubble:name=' + str(name) + ', verbose=' + str(verbose))
        self.name = name

        # very tricky!!
        self.gbc = self

        self.birth = arrow.now()
        self._verbose = verbose
        self._verbose_bar = verbose_bar


        self._msg_stats['___init_verbose'] = verbose
        self.set_parent(parent)
        self._bubble_lib_dir = os.path.dirname(__file__)
        self._log_file = os.path.dirname(logfile)

        self.say(self.name + ':here!', verbosity=101)
        self.say(self.name + ':config',
                 stuff={'verbose': self._verbose,
                        'verbose_bar': self._verbose_bar,
                        'bubble_lib_dir': self._bubble_lib_dir,
                        'logfile': self._log_file,
                        'parent': self._parent
                        },
                 verbosity=101)

    def __enter__(self):
        if not self.debug:
            return

        print('entering:Bubble.name:' + str(self.name))
        print('entering:Bubble.birth:' + str(self.birth))

        if self._parent:
            print('entering:Bubble.parent.name:' + str(self._parent.name))
            print('entering:Bubble.parent.birth:' + str(self._parent.birth))

    def __exit__(self, exit_type=None, value=None, traceback=None):
        if not self.debug:
            return
        print('exiting:Bubble.name:' + str(self.name))
        print('exiting:Bubble.birth:' + str(self.birth))

        if self._parent:
            print('exiting:Bubble.parent.name:' +
                  str(self.name) + "::" + str(self._parent.name))
            print('exiting:Bubble.parent.birth:' +
                  str(self.birth) + "::" + str(self._parent.birth))

        if exit_type:
            print('exiting:Bubble:type:' + str(exit_type))

        if value:
            print('exiting:Bubble:value:' + str(value))
        if traceback:
            print('exiting:Bubble:traceback' + str(traceback))
        if self._parent:
            pass
            # print('p:' + self._parent)
            # print('p:' + self._parent.name)

    def __del__(self):
        return self.__exit__()

    def _update_stat(self, stat_key):
        if stat_key not in self._msg_stats:
            self._msg_stats[stat_key] = 1
        else:
            self._msg_stats[stat_key] += 1

    def set_verbose(self, verbose=0):
        self._update_stat('___set_verbose')
        self._verbose = int(verbose)

    def get_verbose(self):
        return self._verbose

    def set_verbose_bar(self, verbose_bar=0):
        self._update_stat('___set_verbose_bar')
        self._verbose_bar = int(verbose_bar)

    def get_verbose_bar(self):
        return self._verbose_bar

    #: TODO: adaptive bar raising lowering, do we want/need this?
    def verbose_plus(self, amount=1):
        self._update_stat('___verbose_plus')
        if self.adaptive_verbose:
            verbose = self.get_verbose()
            self.set_verbose(verbose + amount)

    def verbose_minus(self, amount=1):
        #: TODO: never drop below 1, move to a magic value
        self._update_stat('___verbose_minus')
        if self.adaptive_verbose and self.get_verbose() > 1:
            verbose = self.get_verbose()
            if verbose > amount:
                self.set_verbose(verbose - amount)
            else:
                self.set_verbose(1)
        else:
            self._update_stat('___verbose_minus_already_below_one')

    def _msg(self, msg='Msg',
             stuff=None,
             verb='SAY',
             verbosity=1,
             child_level=0,
             child_name='',
             from_cli=False):
        self._total_verbose += verbosity
        self._update_stat('___verb_' + verb)

        if isinstance(self._parent, Bubble):
            if child_name:
                child_name = str(self.name) + '::' + child_name
            else:
                child_name = str(self.name)
            self._parent._msg(msg=msg,
                              stuff=stuff,
                              verb=verb,
                              verbosity=verbosity,
                              child_level=child_level + 1,
                              child_name=child_name)
            return
        else:
            self._total_verbose_self += verbosity

        if verbosity > self.get_verbose() or \
           verbosity > self.get_verbose_bar():
            if self.debug:
                print("_msg: below verbose or verbose_bar,no show")
            return
        else:
            if self.debug:
                print("_msg: NOT below verbose or verbose_bar,continue")

        ignore_line = ['_msg','_say_color',
                       'say','say_green','say_yellow','say_yellow']
        f=sys._getframe(2)
        ff=f
        i=0
        while ff.f_back:
            i+=1
            c=ff.f_code
            if c.co_name not in ignore_line:
                break
            ff=ff.f_back
        # print('keeping:',i,c.co_filename,c.co_firstlineno,c.co_name)
        file_line = c.co_filename+':'+str(c.co_firstlineno)

        tl_item = {'attime': arrow.now()-BUBBLE_START_ARROW,
                   'name': self.name,
                   'msg': msg,
                   'stuff': stuff,
                   'verb': verb,
                   'verbosity': verbosity,
                   'child_level': child_level,
                   'child_name': child_name,
                   'from': file_line,
                   'curr_verbose': self.get_verbose(),
                   'curr_verbose_bar':self.get_verbose_bar()
                   }
        #if not from_cli:
        blog.info(**tl_item)


    def tl_from_child(self, exported_timeline=[]):
        for tli in exported_timeline:
            tli['name'] = self.name + ':parent of:' + tli['name']
            self._timeline.append(tli)

    def cry(self, msg='Crying', stuff=None, verbosity=1):
        self.verbose_plus(verbosity)
        self._msg(msg=msg, stuff=stuff, verb='CRY', verbosity=verbosity)

    def mumble(self, msg='Mumbling', stuff=None, verbosity=1):
        self.verbose_minus(verbosity)
        self._msg(msg=msg, stuff=stuff, verb='MUMBLE', verbosity=verbosity)

    def say(self, msg='Saying', stuff=None, verbosity=1):
        self._msg(msg=msg, stuff=stuff, verb='SAY', verbosity=verbosity)
        self.verbose_minus(verbosity)

    def set_parent(self, parent=None):
        if isinstance(parent, Bubble):
            self._parent = parent
            self.set_verbose(parent.get_verbose())
            self.set_verbose_bar(parent.get_verbose_bar())
            parent.add_child(self)

    def add_child(self, child=None):
        if isinstance(child, Bubble):
            self._children.append(child)
            # self.say('added child: '+child.name, verbosity=100)
            self.say('number of children:%d' %
                     len(self._children), verbosity=100)

    def get_total_verbose(self):
        return self._total_verbose

    def get_total_verbose_bar(self):
        return self._total_verbose_bar
