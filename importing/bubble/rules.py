# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

''' bubble rules have a simple notation,
with a line based rule format and a single rule definitions seperator ">>>"
every line starting and ending with the rule separator,
becomes a rule for the bubble transformer.
anything else is treated as comment.
'''
from . import Bubble
from .functions import get_registered_rule_functions
from .util.cli_misc import load_rule_functions

rule_functions = get_registered_rule_functions()


##########################################################################


class Rule(Bubble):
    input = None
    fun = None
    output = None
    depend = []
    src_nr = 0

    def __init__(self,
                 input=None,
                 output=None,
                 fun=None,
                 depend=None,
                 name=None,
                 src_nr=0):

        self.say('Rule init :' + str(id(self)) +
                 '>i>' + str(input) +
                 '>f>' + str(fun) +
                 '>o>' + str(output) +
                 '>d>' + str(depend) +
                 '>n>' + str(name) + '>>>',
                 verbosity=100)
        super(Bubble, self).__init__()
        self.input = input

        # function without input??
        # for example:date / time

        self.fun = rule_functions.get_function(fun)
        self.fun.set_parent(self)

        if output:
            self.output = output
        else:
            self.output = input  # just copy single ok, (structure?) #todo
        self.depend = depend
        self.name = name
        self.src_nr = src_nr

    def __repr__(self):
        srep = '<Rule '
        srep += str(self.src_nr)
        srep += ' >>> ' + str(self.input)
        srep += ' >>> ' + str(self.fun)
        srep += ' >>> ' + str(self.output)
        srep += ' >>> ' + str(self.depend)
        srep += ' >>> ' + str(self.name) + ' >>>'
        return srep

    def run(self, *a):
        self.say('running my function, with:', stuff=a, verbosity=100)
        return self.fun.run(*a)


class Rules(Bubble):
    _rules = []

    def __init__(self, rules=None, rule_type='bubble', home='', verbose=0):
        Bubble.__init__(self, name='Rules', verbose=verbose)
        self.home = home
        self.say('home:' + home, verbosity=10)
        self.say('init, no functions yet', verbosity=100)
        load_rule_functions(self)

        self.say('after loading functions:' +
                 str(len(get_registered_rule_functions())), verbosity=100)

        self._rule_type = rule_type
        if rule_type == 'bubble':
            self._rules = self._convert_rules_bubble(rules)

    def _convert_rules_bubble(self, srules=''):
        """srules, a string containing the rules in bubble format will be
        converted to the internal list of dictonary based rules.
        '>>>': seperator  : a rule has only certain amount of seperators
        a rule is built like: >>>input>>>function>>>output>>>
        for example:
        >>>i>>>adder>>>o>>>>
        >>>42>>>is_it_the_answer>>>the_answer>>>

        is converted to:
        [{'in':'i','fun':'adder','out':'o'},
         {'in':'42','fun':'is_it_the_answer','out':'the_answer'}]

        a rule withhout a name, but with a depency on rule_one
        >>>panic>>>is_there_an_answer>>>dont_panic>>>rule_one>>>

        a rule without depencies and a name
        >>>42>>>is_it_the_answer>>>the_answer>>>nodeps>>rule_one>>>
        """

        if not isinstance(srules, str):
            self.cry('convert_rules_bubble: cannot convert srules of type,' +
                     'list of rules ==> [] :' + str(type(srules)),
                     stuff=srules,
                     verbosity=10)
            return []

        if not srules:
            self.say('convert_rules_bubble: cannot convert empty srules',
                     verbosity=10)
            return []  # no rules

        lines = srules.splitlines()
        self.say('convert_rules_bubble:lines', stuff=lines, verbosity=10)

        line_number = 0
        rules = []
        for r in lines:
            line_number += 1
            # todo: do we wan't this in a configuration, yes! add magic!
            # in util.escaped it's defined as an escape
            # but for rules it is best to define a magic value something like
            # BMGC.TRANSFORMER.RULES_SEPERATOR  #seems better option for
            # or
            # BMGC.TRANSFORMER_RULES_SEPERATOR  #seems simpler
            # BMGC should implement a sane default magic for undefined values.

            r = r.strip()
            if not r.endswith('>>>'):
                continue
            if not r.startswith('>>>'):
                continue

            parts = [p.strip() for p in r.split('>>>')]

            rule = None
            lp = len(parts)
            if lp == 3:
                rule = Rule(input=parts[1],
                            src_nr=line_number)
            if lp == 4:
                rule = Rule(input=parts[1],
                            fun=parts[2],
                            src_nr=line_number)
            if lp == 5:
                rule = Rule(input=parts[1],
                            fun=parts[2],
                            output=parts[3],
                            src_nr=line_number)
            if lp == 6:
                rule = Rule(input=parts[1],
                            fun=parts[2],
                            output=parts[3],
                            depend=parts[4],
                            src_nr=line_number)
            if lp == 7:
                rule = Rule(input=parts[1],
                            fun=parts[2],
                            output=parts[3],
                            depend=parts[4],
                            name=parts[5],
                            src_nr=line_number)

            if rule:
                rules.append(rule)
            else:
                self.cry(
                    'parts not 3..7 rule with parts[' + str(lp) +
                    '] from line:[' + str(line_number) + ']\n\'' + r + '\'',
                    verbosity=10)

        for r in rules:
            r.set_parent(self)
        self._rules = rules
        self.say('convert_rules_bubble:res:rules', stuff=rules, verbosity=10)
        return rules

    def has_rules(self):
        return len(self._rules) > 0

    def get_rules(self):
        return self._rules
