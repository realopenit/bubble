# -*- coding: UTF-8 -*-
"""
before_step(context, step), after_step(context, step)
    These run before and after every step.
    The step passed in is an instance of Step.

before_scenario(context, scenario), after_scenario(context, scenario)
    These run before and after each scenario is run.
    The scenario passed in is an instance of Scenario.

before_feature(context, feature), after_feature(context, feature)
    These run before and after each feature file is exercised.
    The feature passed in is an instance of Feature.

before_tag(context, tag), after_tag(context, tag)

"""

"""
examples to trace behave
"""
from pprint import pprint
DEBUG_BEHAVE_CALLBACKS = False

# -- FILE: features/environment.py
# USE: behave -D BEHAVE_DEBUG_ON_ERROR         (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=yes     (to enable  debug-on-error)
# USE: behave -D BEHAVE_DEBUG_ON_ERROR=no      (to disable debug-on-error)

BEHAVE_DEBUG_ON_ERROR = True


def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")


def before_all(context):
    if DEBUG_BEHAVE_CALLBACKS:
        pprint('EY:b:all:' + str(context))
    setup_debug_on_error(context.config.userdata)


def after_step(context, step):
    if DEBUG_BEHAVE_CALLBACKS:
        pprint('EY:a:step:c:' + str(context))
        pprint('EY:a:step:s:' + str(step))

    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)


# def before_all(context):
#    if DEBUG_BEHAVE_CALLBACKS:
#        print('EY:b:all:'+str(context))

def after_all(context):
    if DEBUG_BEHAVE_CALLBACKS:
        pprint('EY:a:all:' + str(context))


def before_scenario(context, scenario):
    context.execute_steps(u"Given a new working directory")
    #context.execute_steps(u'When I run "rm -rf ./"')
    if DEBUG_BEHAVE_CALLBACKS:
        pprint('EY:b:scenario:c:' + str(context))
        # context.__stack['workdir']+='/'+scenario.name
        pprint('EY:b:scenario:s:' + str(scenario))


def after_scenario(context, scenario):
    if u'workdir' in context._stack[0]:
        fname = 'OopsNoFeature'
        for st_item in context._stack:
            if 'feature' in st_item:
                feature = st_item['feature']
                # pprint(feature)
                if feature:
                    fname = feature.name
                    # fstr=str(feature)
                    # print("fstr:"+fstr)
                    # import code
                    # ic = code.InteractiveConsole({'gl': globals(),
                    #                              'lo': locals(),
                    #                              'c':context,
                    #                              's':scenario,
                    #                              'f':feature})
                    # ic.interact('Bubble >>> Interactive python console>>>')
                    # break
        owd = context._stack[0]['workdir']
        nwd = owd.replace('__WORKDIR__', 'tmp/__WORKDIR__F__' + str(fname + '__S__' + scenario.name))
        nwd = nwd.replace('"', '_')
        nwd = nwd.replace("'", '_')
        nwd = nwd.replace(',', '_')
        nwd = nwd.replace(' ', '_')
        context.execute_steps(u'When I run "rm -rf ' + nwd + u'"')
        context.execute_steps(u'When I run "cp -r ' + owd + u' ' + nwd + u'"')
    if DEBUG_BEHAVE_CALLBACKS:
        pprint('EY:a:scenario:c:' + str(context))
        # context.execute_steps(u"Given a new working directory")
        pprint(context._stack)
        pprint(scenario)


        pprint('EY:b:scenario:s:' + str(scenario))


def before_step(context, step):
    if DEBUG_BEHAVE_CALLBACKS:
        pprint('EY:b:step:c:' + str(context))
        pprint('EY:b:step:s:' + str(step))

# def after_step(context, step):
#    if DEBUG_BEHAVE_CALLBACKS:
#        print('EY:a:step:c:'+str(context))
#        print('EY:a:step:s:'+str(step))


def before_tag(context, tag):
    if DEBUG_BEHAVE_CALLBACKS:
        pprint('EY:b:tag:c:' + str(context))
        pprint('EY:b:tag:s:' + str(tag))


def after_tag(context, tag):
    if DEBUG_BEHAVE_CALLBACKS:
        pprint('EY:a:step:c:' + str(tag))
        pprint('EY:a:step:s:' + str(tag))
