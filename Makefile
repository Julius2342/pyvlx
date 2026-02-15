
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
	pytest

build:
	@python3 -m build

pypi:
	@rm -f dist/*
	@python3 -m build
	@twine upload dist/*

pylint:
	@pylint pyvlx test/*.py examples/*.py

pydocstyle:
	 @pydocstyle pyvlx test/*.py test/*.py examples/*.py

coverage:
	pytest --cov-report html --cov pyvlx --verbose

.PHONY: test build
