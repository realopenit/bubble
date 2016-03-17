'''
Created on Nov 10, 2014

@author: erdal
'''
from behave import given, when, then, step
import json

from bubble.transformer import Transformer
from bubble.functions import register



@when(u'I apply bubble {rules} on {inp} dictionary')
def step_apply_bubble_rule(context, rules, inp):
    jd_input = json.loads(inp)
    register(lambda x: 42,          'the_answer')
    register(lambda x: int(x) + 1,  'adder')
    register(lambda x: len(x),      'len')
    register(lambda x: len(x),      'size')
    register(lambda x: int(x) ** 2, 'square')
    transformer = Transformer(rules,
                              rule_type='bubble',
                              bubble_path=context.workdir)
    context.result = transformer.transform(jd_input)


@then(u'I get {output} dictionary')
def step_get_output(context, output):
    jd_output = json.loads(output)
    return context.result == jd_output
