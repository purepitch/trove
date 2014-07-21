.PHONY: clean unittest cover api tags accept

REDNOSE_EXISTS = $(shell nosetests --plugins | grep rednose)
ifneq "$(REDNOSE_EXISTS)" ""
    NOSE_OPTS = --rednose
endif
COVER_OPTS = --with-coverage --cover-package=$(LIB_NAME) --cover-erase \
	     --cover-html --cover-branches

LIB_NAME = modules

test: unittest codingstd accept

# just run the unit tests
unittest:
	nosetests $(NOSE_OPTS)

# run the coding standards tests
codingstd:
	nosetests $(NOSE_OPTS) tests/codingstd

# run the acceptance tests
accept:
	behave -t ~wip

# show how well the test suite exercises the code
cover:
	rm -rf cover
	nosetests $(NOSE_OPTS) $(COVER_OPTS)

# build the API documentation
api:
	cd api; make html

# display coding standard and code quality metrics
lint:
	-pylint $(LIB_NAME) trove.py

# generate the tags file for easier code navigation
tags:
	ctags $(LIB_NAME)/*.py

clean:
	rm -f tags $(LIB_NAME)/*.pyc tests/*.pyc $(LIB_NAME)/*.pyo tests/*.pyo
