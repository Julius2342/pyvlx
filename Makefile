
all:
	@echo
	@echo "Available targets"
	@echo ""
	@echo "build           -- build python package"
	@echo ""
	@echo "pypi            -- upload package to pypi"
	@echo ""
	@echo "test            -- execute test suite"
	@echo ""
	@echo "pylint          -- run pylint tests"
	@echo ""
	@echo "pydocstyle      -- run pydocstyle tests"
	@echo ""
	@echo "coverage        -- create coverage report"
	@echo ""

test:
	PYTHONPATH="${PYTHONPATH}:/" python3 -m unittest discover -s test -p "*_test.py" -b

build:
	@python3 setup.py sdist
	@python3 setup.py egg_info

pypi:
	# python3 setup.py register -r pypi
	#@python3 setup.py sdist upload -r pypi
	@rm dist/*
	@python setup.py sdist
	@twine upload dist/*

pylint:
	@pylint -j 8 --rcfile=.pylintrc pyvlx test/*.py *.py examples/*.py

pydocstyle:
	 @pydocstyle pyvlx test/*.py test/*.py *.py examples/*.py

coverage:
	py.test --cov-report html --cov pyvlx --verbose

.PHONY: test build
