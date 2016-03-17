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

CODE_DIRECTORY = '.'
metadata = imp.load_source(
    'metadata', os.path.join(CODE_DIRECTORY, 'metadata.py'))


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
    py_modules=['mydumboclient.mydumboclient'],
    install_requires=requirements,
    license="GPL-3.0",
    zip_safe=False,
    keywords='bubble-client',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)

