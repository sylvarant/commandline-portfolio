PYTHON=`which python`
NAME=`python setup.py --name`
VERSION=`python setup.py --version`
SDIST=dist/$(NAME)-$(VERSION).tar.gz
VENV=/tmp/venv


all: check test 

test:
	python -m unittest discover .

check:
	find . -name \*.py | grep -v "^test_" | xargs pylint --errors-only --reports=n

init:
	pip install -r requirements.txt 

clean:
	find . -name '*.pyc' -delete

