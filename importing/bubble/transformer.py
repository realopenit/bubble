# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.
''' the bubble transformer takes a dictionary and applies transforming rules(with functions)
and returns the resulting dictionary.
'''
from . import Bubble
from .rules import Rules
from .util.value_path import ValuePath
from .util.flat_dict import unflat, get_flat_path


##########################################################################

##########################################################################


class Transformer(Bubble):
    name = None
    _rules = []
    _store = None
    _value_path = None

    def __init__(self, rules=None, rule_type='bubble', store={}, config={}, bubble_path=None, verbose=1):
        Bubble.__init__(self,
                        name='Transformer',
                        verbose=verbose)

        self.say('before loading rules',
                 verbosity=10)
        self.home = bubble_path
        self._rules = Rules(rules=rules,
                            rule_type=rule_type,
                            verbose=verbose,
                            home=bubble_path)
        self._rules.set_parent(self)

        self.say('after loading rules:has rules:' +
                 str(self._rules.has_rules()),
                 verbosity=10)

        self._stored_dict = store
        self._config_dict = config
        self._bubble_path = bubble_path
        self._value_path = ValuePath()

    def transform(self, indict):
        # self.say('rules_can_be_executed',self.rules_can_be_executed())
        self.say('transform:enter:indict', stuff=indict, verbosity=20)

        if not self._rules.has_rules():
            return indict  # no rules return 'null' transformation

        outdict = {}
        tempdict = {}

        # BTS: bubble transformer source
        indict['__BTS_NAME'] = 'IN'
        outdict['__BTS_NAME'] = 'OUT'
        tempdict['__BTS_NAME'] = 'INTERNAL'
        self.say('getting store', verbosity=20)
        storeddict = self._stored_dict
        storeddict['__BTS_NAME'] = 'PERSISTANT'
        cfgdict = self._config_dict
        cfgdict['__BTS_NAME'] = 'CONFIGURATION'

        for r in self._rules.get_rules():
            self.say('current rule: ' + str(r),
                     verbosity=10)

            source_key = r.input
            if len(source_key) == 0:
                # say? print 'cannot do magic, need input'
                continue

            target_key = r.output
            if len(target_key) == 0:
                # say ? print 'cannot do magic, need output'
                continue

            conds_keys = source_key.split(':')
            if len(conds_keys) == 2:
                conds_str = conds_keys[0]
                conds = conds_str.split(',')
                keys_str = conds_keys[1]
                keys = keys_str.split(',')
            else:
                conds = []
                keys_str = conds_keys[0]
                keys = keys_str.split(',')
                self.say('keys:' + str(keys), verbosity=10)

            if len(conds) >= 1:
                cond_ak = self.create_ak(
                    conds, indict, tempdict, outdict, storeddict, cfgdict)
                if not self.all_conds(cond_ak['a']):
                    self.say('conds:' + str(conds) + ' ak:' + str(cond_ak) +
                             ' skip rule execution, not all conditions met',
                             verbosity=10)
                    continue

            src_ak = self.create_ak(
                keys, indict, tempdict, outdict, storeddict, cfgdict)

            # run the fun on the rule
            res = r.run(*src_ak['a'])  # expanded argument list
            # res = r.run(**src_ak['k'])  # keyword arguments

            self.say('rule run res:' + str(res), verbosity=10)

            if target_key == '!SKIP' and res is True:
                self.say('skipping', verbosity=10)
                return 'BUBBLE_SKIPPING'

            if target_key.startswith('.'):
                self.say('temping:' + target_key, verbosity=10)
                tempdict = self.set_key_path(tempdict, target_key[1:], res)
            elif target_key.startswith(';'):
                self.say('persisting:' + target_key, verbosity=10)
                storeddict = self.set_key_path(storeddict, target_key[1:], res)
                self.storeddict = storeddict

            else:
                outdict = self.set_key_path(outdict, target_key, res)

            self.say('transform:memory',
                     stuff={'in': indict,
                            'temp': tempdict,
                            'out': outdict},
                     verbosity=99)
            self.say('transform:memory persistant',
                     stuff={'persistant': storeddict},
                     verbosity=999)

        self.say('transform:exit:tempict:discarding', verbosity=10)
        self.say('transform:exit:keep persistent', verbosity=10)
        self._stored_dict = storeddict
        self.say('transform:exit:outdict', outdict, verbosity=10)
        del(outdict['__BTS_NAME'])
        return outdict

    def create_ak(self, keys, indict, tempdict, outdict, storeddict, cfgdict):
        src_ak = {'a': [],
                  'k': {}}

        for k in keys:
            k = k.strip()
            self.say('current key:' + k, verbosity=10)

            # when quoted, key is value
            # todo: quoting magic
            quote = "'"
            if k.startswith(quote) and k.endswith(quote):
                src_ak['a'].append(k[1:-1])
                continue

            quote = '"'
            if k.startswith(quote) and k.endswith(quote):
                src_ak['a'].append(k[1:-1])
                continue

            if k.startswith('.'):
                v = self.key_path(tempdict, k[1:])
            elif k.startswith(';'):
                v = self.key_path(storeddict, k[1:])
            elif k.startswith(':'):
                v = self.key_path(outdict, k[1:])
            elif k.startswith('~'):
                v = self.key_path(cfgdict, k[1:])
            else:
                v = self.key_path(indict, k)

            src_ak['a'].append(v)
            # we have never use the keywords yet, removing
            src_ak['k'][k] = v

            self.say(
                'create_ak:found >>> ' +
                str(keys) + ' >>> as  value array or dict ',
                verbosity=10)
        return src_ak

    def key_path(self, data, path):
        if path.endswith('**'):
            flat_data = get_flat_path(self, data, path[:-1])
            # return self._value_path.get_path(data, path[:-3])
            fat_data = unflat(self, flat_data)
            return fat_data
        # return flat_data
        return get_flat_path(self, data, path)

    def key_path_exists(self, data, path):
        # return self._value_path.get_path(data, path)
        res = get_flat_path(self, data, path, 'NOT_EXISTING')
        if isinstance(res, str) and res == 'NOT_EXISTING':
            return ''
        else:
            return res

    def set_key_path(self, data, path, value):
        return self._value_path.set_path(data, path, value)

    def all_conds(self, conditions):
        trues = [i for i in conditions if i]
        return len(trues) == len(conditions)

    def get_store(self):
        return self._stored_dict


if __name__ == '__main__':
    from pprint import pprint as pp
    import re
    inp = {'hello': 'world',
           'goodbye': 'universe',
           'apple': 'i like to eat a juicy apple!'}

    # rules with names of functions: functions must be present or loadable
    # from current bubble
    rules = []
    rules.append({'input': 'hello', 'fun': 'len', 'output': 'hello_len'})
    # rules.append({'input': 'hello','fun':'str.capitalize','output':'HelloCapitalized'})
    rules.append({'input': 'hello', 'fun': 'rcap',
                  'output': 'hello_reversed_capitalized'})
    rules.append({'input': 'apple', 'fun': 'peachify', 'output': 'peach'})

    from .functions import register

    def rcap(s):
        return ''.join([c for c in reversed(s.lower())]).capitalize()

    def peachify(s):
        return re.sub('apple', 'peach', s)

    register(len, 'len')
    register(str.capitalize, 'str.capitalize')
    register(rcap, 'rcap')
    register(peachify, 'peachify')

    t2 = Transformer(rules, rule_type='list_of_dicts')
    # print get_registered_rule_functions()
    # t2.set_functions(get_registered_rule_functions())

    print('in')
    pp(inp)
    print('rules')
    pp(rules)
    print('result')
    t2.verbose = 10000
    pp(t2)
    pp(t2.transform(inp))
