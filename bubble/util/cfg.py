# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

"""yaml based configuration, with a dotted access of configuration """
import yaml
from bubble.util.inside_try import inside_try

# TODO move to configuration, options
CFG_UTIL_CFG_DEBUG = False


class BubbleDoct(dict):
    def __init__(self, org_dict, d=0, p=None, k=None):
        self.__dict__ = self
        for item in org_dict.items():
            key = item[0]
            value = item[1]
            if isinstance(value, dict):
                self.say('converting to doct:', stuff=d)
                value = BubbleDoct(value, d + 1, self, key)
            if key != '_doct_parent':
                self.__setitem__(key, value)

    def __setitem__(self, key, value):
        self.say('set item:' + key, stuff=value, verbosity=100)
        return dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        self.say('del item:' + key, stuff=None, verbosity=100)
        return dict.__delitem__(self, key)

    # just emulate Bubble.say for now:(
    def say(self, msg='something', stuff=None, verbosity=100):
        if CFG_UTIL_CFG_DEBUG:
            print('BubbleDoct', msg, stuff, verbosity)

    def export_dict(self):
        self.say('exporting:self:',
                 stuff=self, verbosity=100)
        export = {}
        for (k, v) in self.items():
            if k not in ['_doct_level', '_doct_as_key']:
                if isinstance(v, BubbleDoct):
                    export[k] = v.export_dict()
                else:
                    export[k] = v
        self.say('exporting:self:export', stuff=export, verbosity=100)
        return export


@inside_try
def get_config(ctx, yaml_cfg_file='config/config.yaml'):
    ctx.say('get_config:config_file:' + yaml_cfg_file, verbosity=50)
    ycfg = yaml.load(open(yaml_cfg_file))
    ctx.say('get_config::ycfg', stuff=ycfg, verbosity=50)
    BCFG = BubbleDoct(ycfg)
    ctx.say('get_config::BCFG', stuff=BCFG, verbosity=50)
    return BCFG


@inside_try
def put_config(ctx, yaml_cfg_file='config/config.yaml', YCFG={'CFG': {}}):
    ctx.say('put_config:config_file:' + yaml_cfg_file, verbosity=50)
    ctx.say('put_config::YCFG', stuff=YCFG, verbosity=50)
    if isinstance(YCFG, BubbleDoct):
        ycfg = YCFG.export_dict()
    else:
        ycfg = YCFG
    ctx.say('put_config::ycfg', stuff=ycfg, verbosity=50)

    ystr = yaml.dump(ycfg,
                     indent=4,
                     default_flow_style=False)
    with open(yaml_cfg_file, 'w') as yaml_file:
        res = yaml_file.write(ystr)

    ctx.say('put_config::ycfg:res', stuff=res, verbosity=50)
    BCFG = BubbleDoct(ycfg)
    ctx.say('put_config::BCFG:returning', stuff=BCFG, verbosity=50)
    return BCFG
