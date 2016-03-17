# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

"""internal magic values, like the configuration"""

from .cfg import get_config, put_config, BubbleDoct
magic = {'BMGC': {}}
MAGIC = BubbleDoct(magic)


def get_magic(ctx, yaml_mgc_file='config/magic.yaml'):
    ctx.gbc.say('getting magic')
    MGC = get_config(ctx, yaml_cfg_file=yaml_mgc_file)
    ctx.gbc.say('getting magic:MGC:', stuff=MGC)
    return MGC


def save_magic(ctx, yaml_mgc_file='config/magic.yaml', MGC={'BMGC': {}}):
    ctx.gbc.say('saving magic')
    res = put_config(ctx, yaml_cfg_file=yaml_mgc_file, YCFG=MGC)
    ctx.gbc.say('saving magic:res', stuff=res)


if __name__ == '__main__':
    print(MAGIC)
    MAGIC.BMGC.hello = 'Hello There!'
    print(MAGIC)
    del(MAGIC.BMGC.hello)
    MAGIC.BMGC.goodbye = {}
    MAGIC.BMGC.goodbye['msg'] = 'Goobye too!!'
    MAGIC.BMGC.goodbye['cruel'] = {}
    MAGIC.BMGC.goodbye['cruel']['world'] = 'deep thought'
    MAGIC.BMGC.goodbye['favorite_fruits'] = ['orange', 'pear', 'banana']
    MAGIC.BMGC.something = {}

    # MAGIC.BMGC.something['completely.different'] = 'you can store any kind of thing in this'#but still not finished yet
    # need to do some esccaping also

    MAGIC.BMGC.something['answer'] = 42
    MAGIC.BMGC.something['answer_str'] = 'forty two'
    MAGIC.BMGC.something[
        'not_the_question'] = "I may be a sorry case, but I don't write jokes in base 13. (DNA)"

    print(MAGIC)
    from bubble import Bubble
    save_magic(Bubble(), 'magic.yaml', MAGIC)
    rM = get_magic(Bubble(), 'magic.yaml')
    # print(rM.BMGC.something.completely.different)
    print(rM.BMGC.something.not_the_question)


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
