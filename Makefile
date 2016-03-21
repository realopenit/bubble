.PHONY: clean-pyc clean-build docs clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "behave - behave tests"
	@echo "behavepyenvs - behave tests in different pyenv enverionments"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "release-test - package and upload a release to testpypi"
	@echo "dist - package"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 bubble
	# flake8 bubble tests

behave:
	behave

behavepyenvs:
	bin/behave_pyversions_in_pyenv.sh

test:
	#python setup.py test
	echo "no unit tests yet :( use behave :)"

coverage:
	coverage run --source bubble -m behave
	# coverage run --source bubble setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs:
	rm -f docs/bubble.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ bubble
	$(MAKE) -C docs clean html singlehtml man -b
	echo "open file://`pwd`/build/docs/html/index.html"
	echo "open file://`pwd`/build/docs/singlehtml/index.html"
	echo "man have a look: man build/docs/man/Bubble.1"
	cp build/docs/man/Bubble.1 bubble/extras/
	gzip  -f bubble/extras/Bubble.1


release-test: clean
	python setup.py sdist upload -r https://testpypi.python.org/pypi
	python setup.py bdist_wheel upload -r https://testpypi.python.org/pypi

release: clean dist
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean docs
	echo `date +%Y.%m.%d` >VERSION.txt
	sed -i "s/^version =.*/version = \"`date +%Y.%m.%d`\"/" bubble/metadata.py
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py bdist_wheel
	pip install ./dist/bubble-*-py2.py3-none-any.whl
