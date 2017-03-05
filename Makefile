
version = 2.7

bin/apitizer: bin/python setup.py
	bin/python setup.py develop
	@touch $@

bin/python bin/pip:
	virtualenv --clear --python=python$(version) .

clean:
	git clean -Xdf

.PHONY: clean
