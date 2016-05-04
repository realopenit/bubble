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
	@echo "upload_to_pypi - upload a release"
	@echo "upload_to_testpypi - upload a release to testpypi"
	@echo "compile_requirements - pip compile the requirements"
	@echo "version - upDATE version"
	@echo "dist - package"
	@echo "compile_requirements - pip compile  *requirement.txt files from the *.in files"


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

behavepyenvs: dist
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



version:
	echo `date +%Y.%m.%d` >VERSION.txt
	sed -i "s/^version =.*/version = \"`date +%Y.%m.%d`\"/" bubble/metadata.py

dist: clean docs
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py bdist_wheel
	pip install ./dist/bubble-*-py2.py3-none-any.whl

upload_to_testpypi: clean dist
	twine upload dist/* -r testpypi
	echo "please checkout https://testpypi.python.org/pypi/bubble/"
	echo "for testing: first install the requirements from pypi"
	echo "pip install -r requirements.txt"
	echo "pip install  bubble --index https://testpypi.python.org/pypi --upgrade"
	echo "looking good? continue with make upload_to_pypi"



upload_to_pypi:
	twine upload dist/*
	echo "please checkout https://pypi.python.org/pypi/bubble/"
	echo "for testing:"
	echo "pipsi install  bubble --upgrade"
	echo "pip install  bubble --upgrade"

compile_requirements:
	pip-compile requirements.in >requirements.txt
	pip-compile dev_requirements.in >dev_requirements.txt
	pip-compile requirements.in dev_requirements.in --output-file travis_requirements.txt
	pip-compile requirements.in optional_requirements.txt --output-file requirements_plus_dataset.txt

