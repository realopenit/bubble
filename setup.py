#!/usr/bin/env python
# -*- coding: utf-8 -*-

import imp
import os
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
curr_path = os.path.dirname(os.path.realpath(__file__))
deps = os.path.join(curr_path, 'requirements.txt')
dev_deps = os.path.join(curr_path, 'dev_requirements.txt')

requirements = open(deps).read()
test_requirements = open(dev_deps).read()

CODE_DIRECTORY = 'bubble'
metadata = imp.load_source(
    'metadata', os.path.join(CODE_DIRECTORY, 'metadata.py'))

#orderdict needed for structlog
sys_version_str='.'.join((str(s) for s in sys.version_info[0:3]))

if sys_version_str == '2.6.9':
    #on 2.6.9 ssl will not work so pip will not work also :(
    #totally depracated but luckily easy_install will still kind of work
    #https://pypi.python.org/pypi/setuptools
    #os.system('wget https://bootstrap.pypa.io/ez_setup.py -O - | python')
    #os.system('easy_install importlib') #drop in replacement from 2.7
    #os.system('easy_install ordereddict') #backported from PY3
    #in issue 9: easy_install will be mentioned as an alternative
    
    print('BUBBLE setup.by: 2.6.9: installing ordereddict and importlib')
    print('BUBBLE setup.by: 2.6.9: https://github.com/realopenit/bubble/issues/9 for more info')
    os.system('pip install importlib') #backported from 2.7
    os.system('pip install ordereddict') #drop in replacement from 2.7
    


setup(
    name=metadata.package,
    version=metadata.version,
    author=metadata.authors[0],
    author_email=metadata.emails[0],
    maintainer=metadata.authors[0],
    maintainer_email=metadata.emails[0],
    url=metadata.url,
    description=metadata.description,
    long_description=readme + '\n\n' + history,
    packages=[
        'bubble',
        'bubble.util',
        'bubble.util.dataset',
        'bubble.util.store',
        'bubble.commands',
        'bubble.clients',
    ],
    package_dir={'bubble':
                 'bubble'},
    py_modules=['bubble'],
    include_package_data=True,
    install_requires=requirements,
    license="GPL-3.0",
    zip_safe=False,
    keywords='bubble, api2api, transform',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points='''
        [console_scripts]
        bubble = bubble.cli:cli
    '''
)
