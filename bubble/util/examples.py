# -*- coding: utf-8 -*-
# Part of bubble. See LICENSE file for full copyright and licensing details.

def get_example_configuration():
    """an example configuration"""
    example = """---
CFG:
    BUBBLE:
        DEBUG: True
        VERBOSE: True
        STORAGE_TYPE: json
    DEV:
        SOURCE:    #pull
            CLIENT: ./mysrcclient.py
        TRANSFORM:
            RULES: config/rules.bubble
        TARGET:    #push
            CLIENT: ./mytgtclient.py
...
#please see bubble/docs/configuration
"""
    return example


def get_example_rules_bubble():
    """an example in .bubble format"""
    example = """
>>> is the separator for rule configurations

only lines containing two,three,for,five or six '>>>' are parsed as rules
everthing else is ignored and can be used as comments

like to transform this:
 {
            "in": "Hello, Pulling in Hello:0"
 },
to:
 {
            "out": "Hello, Pulling in Hello:0"
 },

with a rule function, see [[rule_functions]].

you just have to create this rule
>>>in>>>replace_hello_with_goodbye>>>out>>>

>>>in,'1','10','2'>>>slicing>>>slice_1_10_2>>>
>>>in,'3' >>>slicing>>>slice_3>>>
>>>in,'4','8' >>>slicing>>>slice_4-8>>>
>>>'42',in>>>in>>>.we have found the answer>>>
>>>.we have found the answer:"what's the question?">>> >>>answer_found>>>

this is not a rule, but rules can be represent like this
>i> >f> >o> >d> >n> >>>
i=input
f=function
o=output
d=depend
n=name
for more on writing rules, [[rule_definitions]]
"""
    return example


def get_example_rule_functions():
    """some example rule functions"""
    example = """
#custom functions to be used in rules
def replace_hello_with_goodbye(input):
    #val=input['k']['in.1']
    #print('rf:replace_hello_with_goodbye:k:in.1',val)
    ret=input.replace('Hello','Goodbye')
    return ret

#to override a function delivered with bubble, just redefine and register.
#def equal(a,b):
#    r=False
#    if str(a)==str(b):
#        r=True
#    #print('Rule:equal:',a,type(a),b,type(b),'>>>',r)
#    return r


def substring(sub,string):
    r=False
    if str(sub) in str(string):
        r=True
    #print('Rule:substring:',sub,type(sub),string,type(string),'>>>',r)
    return r

def slicing(mystr,start=0,stop=-1,step=1):
    return mystr[int(start):int(stop):int(step)]
    #return str[slice(start,stop,step)]



################################################################################
#register
################################################################################
from bubble.functions import register
#, trace,timer

register(replace_hello_with_goodbye)
register(replace_hello_with_goodbye,'say_goodbye') #alias

#register(equal)
register(substring)
register(slicing)

# this module will imported during the transformation process,
# and all the functions in rule_functions will be added to the transformer
# the functions should return base python types, any other objects,
# will be string represented with repr(object) as value
# you can use all python functions,
# as long as the returned value is json dumpable
"""
    return example


def get_example_client_pull():
    """dummy client with pull method"""
    example = """
from bubble import Bubble
class MyFancyHelloPuller(Bubble):
    def say_hello(self,i=0):
        return 'Hello, ' + str(i)

# alias for the bubble client to be found by the bubble machinery
class BubbleClient(Bubble):
    def __init__(self,cfg={}):
        self.CFG=cfg
        self.client=MyFancyHelloPuller()

class BubbleClient(Bubble):
    def __init__(self,cfg={}):
        self.CFG=cfg
        self.client=MyFancyHelloPuller()
    def pull(self, amount=42+1, index=0):
        self.say('BC: %d,%d'%(amount,index))
        for i in range(amount):
           hello_pull=self.client.say_hello('Pulling in Hello:' + str(i));
           yield {'in': hello_pull}


if __name__ == '__main__':
    from bubble.util.cfg import get_config
    BCFG = get_config()
    HELLO = BCFG.CFG.DEV.SOURCE
    puller = BubbleClient(HELLO)
    print(puller)
    print(puller.pull())

"""
    return example


def get_example_client_push():
    """dummy client with push method"""
    example = """
from bubble import Bubble
class MyFancyGoodbyePusher(Bubble):
    def say_goodbye(self,i=0):
        return 'Goodbye, '+str(i)

class BubbleClient(Bubble):
    def __init__(self,cfg={}):
        self.CFG=cfg
        self.client=MyFancyGoodbyePusher()
    def push(self, d={}):
        return self.client.say_goodbye(d)

if __name__ == '__main__':
    from bubble.util.cfg import get_config
    BCFG = get_config()
    GOODBYE = BCFG.CFG.DEV.TARGET
    pusher = BubbleClient(GOODBYE)
    print(pusher)
    print(pusher.push())

"""
    return example



all_examples_functions=[{'name':'configuration',
                         'fun': get_example_configuration},
                        {'name': 'rule_functions',
                         'fun': get_example_rules_bubble},
                        {'name': 'configuration',
                         'fun': get_example_rule_functions},
                        {'name': 'client_pull',
                         'fun': get_example_client_pull},
                        {'name': 'client_push',
                         'fun': get_example_client_push}]



if __name__ == '__main__':
    print('#############get_example_configuration################')
    print(get_example_configuration())

    print('#############get_example_rules_bubble#################')
    print(get_example_rules_bubble())

    print('#############get_example_rule_functions###############')
    print(get_example_rule_functions())

    print('#############get_example_client_pull##################')
    print(get_example_client_pull())

    print('#############get_example_client_push##################')
    print(get_example_client_push())


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
