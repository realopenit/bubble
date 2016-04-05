# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

'''rule functions, these can be attached to rules and run by the rule'''
import os
import sys
from functools import wraps
import six
import arrow

from . import Bubble

##########################################################################
FUN_TYPE = 'system'
# FUN_TYPE='USER'


class RuleFunction(Bubble):
    name = None
    fun = None
    fun_type = None
    stats = None

    def __init__(self, name=None, fun=None, fun_type=None, verbose=1):
        Bubble.__init__(self, name='Rule Function', verbose=verbose)
        self.name = name
        self.fun = fun
        self.fun_type = fun_type
        # self.say('RuleFunction present:%s %s'%(str(name),str(fun)))
        # self.set_verbose(0)

    def run(self, *a):
        self.say('running function:' + str(self.name) +
                 '(' + str(a) + ')', verbosity=100)
        try:
            res = self.fun(*a)
            # res = self.fun(**k)
        except Exception as e:
            self.cry(e)
            res = 'cannot run:' + self.name + ' with:' + str(a)
        return res

    def __repr__(self):
        return '<RuleFunction 0x%d %s %s %s>' % (id(self),
                                                 self.name,
                                                 self.fun,
                                                 self.fun_type)


class NoRuleFunction(Bubble):
    name = None
    fun = None
    fun_type = None
    stats = None

    def __init__(self, name=None):
        Bubble.__init__(self, name='NoRule Function')
        self.name = name
        self.fun = self.no_fun
        # self.say('NoRuleFunction present:%s %s'%(str(name),str(fun)))
        # self.set_verbose(0)

    def run(self, *a):
        res = self.fun(*a)  # k
        return res

    def no_fun(self, *a):
        if len(a) == 1:
            res = str(a[0])
        else:
            # TODO move joiner to config, rule??
            joiner = ' '  # join args with space
            string_values = [str(item) for item in a]
            res = joiner.join(string_values)
        self.say('no function, return joined items as:' + res, verbosity=100)
        return res


class RuleFunctions(Bubble):
    _rule_functions = {}

    def __init__(self):
        Bubble.__init__(self, name='Rule Functions Manager')

    def get_function(self, fun=None):
        """get function as RuleFunction or return a NoRuleFunction function"""
        sfun = str(fun)
        self.say('get_function:' + sfun, verbosity=100)

        if not fun:
            return NoRuleFunction()  # dummy to execute via no_fun

        if sfun in self._rule_functions:
            return self._rule_functions[sfun]
        else:
            self.add_function(name=sfun,
                              fun=self.rule_function_not_found(fun))
            self.cry('fun(%s) not found, returning dummy' %
                     (sfun), verbosity=10)
            if sfun in self._rule_functions:
                return self._rule_functions[sfun]
            else:
                self.rule_function_not_found(fun)

    def add_custom_function(self,
                            fun=None,
                            name=None,
                            fun_type="custom"):
        return self.add_function(fun=fun,
                                 name=name,
                                 fun_type=fun_type)

    def add_function(self,
                     fun=None,
                     name=None,
                     fun_type=FUN_TYPE):
        """actually replace function"""
        if not name:
            if six.PY2:
                name = fun.func_name
            else:
                name = fun.__name__

        self.say('adding fun(%s)' % name, verbosity=50)
        self.say('adding fun_type:%s' % fun_type, verbosity=50)

        if self.function_exists(name):
            self.cry('overwriting :fun(%s)' % name, verbosity=10)

        self.say('added :' + name, verbosity=10)
        self._rule_functions[name] = RuleFunction(name, fun, fun_type)
        return True

    def function_exists(self, fun):
        """ get function's existense """
        res = fun in self._rule_functions
        self.say('function exists:' + str(fun) + ':' + str(res),
                 verbosity=10)
        return res

    def functions_count(self):
        """ get number of functions"""
        return len(self._rule_functions)

    def rule_function_not_found(self, fun=None):
        """ any function that does not exist will be added as a
        dummy function that will gather inputs for easing into
        the possible future implementation
        """
        sfun = str(fun)
        self.cry('rule_function_not_found:' + sfun)

        def not_found(*a, **k):
            return(sfun + ':rule_function_not_found', k.keys())
        return not_found

    def get_rule_functions(self):
        return self._rule_functions

    def __len__(self):
        return len(self._rule_functions)

    def __iter__(self):
        self.say('acting as a list rule functions', verbosity=101)
        for item in self._rule_functions:
            self.say('fun item:', stuff=item, verbosity=101)
            yield item

##########################################################################
# register
##########################################################################
# rule functions list manager
rule_functions = RuleFunctions()


def get_registered_rule_functions():
    """ get the function registry """
    return rule_functions

register_system_function = rule_functions.add_function
register = rule_functions.add_custom_function

##########################################################################


def trace(fun, *a, **k):
    """ define a tracer for a rule function
    for log and statistic purposes """
    @wraps(fun)
    def tracer(*a, **k):
        ret = fun(*a, **k)
        print('trace:fun: %s\n ret=%s\n a=%s\nk%s\n' %
              (str(fun), str(ret), str(a), str(k)))
        return ret
    return tracer


def timer(fun, *a, **k):
    """ define a timer for a rule function
    for log and statistic purposes """
    @wraps(fun)
    def timer(*a, **k):
        start = arrow.now()
        ret = fun(*a, **k)
        end = arrow.now()
        print('timer:fun: %s\n start:%s,end:%s, took [%s]' % (
            str(fun), str(start), str(end), str(end - start)))
        return ret
    return timer


# TODO make all importing absolute or relative "./" inside a bubble
# and move loading to something like util.loader
# "python import" -> "bubble loading"
def load_custom_functions(ctx,
                          custom_rule_functions_py='./custom_rule_functions.py'):
    ctx.say('functions:load_custom_rule_functions:'+custom_rule_functions_py, verbosity=100)

    # this "feels" wrong, functions system should be loaded
    from . import functions_system
    ctx.say('imported functions_system:'+functions_system.__name__, verbosity=100)
    abs_path = ctx.home
    custom_functions_py = ctx.home + os.sep + custom_rule_functions_py
    ctx.gbc.say("trying to load:" + custom_functions_py, verbosity=100)
    if os.path.exists(custom_functions_py) and \
       os.path.isfile(custom_functions_py):
        sys.path.insert(0, abs_path)
        import custom_rule_functions
        ctx.say('imported custom rule functions:'+custom_rule_functions.__name__, verbosity=100)
