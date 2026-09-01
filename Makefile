
all:
	@echo
	@echo "Available targets"
	@echo ""
	@echo "ci              -- run linting and tests"
	@echo ""
	@echo "test            -- execute test suite"
	@echo ""
	@echo "mypy            -- run mypy checks"
	@echo ""
	@echo "pylint          -- run pylint tests"
	@echo ""
	@echo "ruff            -- run ruff checks"
	@echo ""
	@echo "coverage        -- create coverage report"
	@echo ""
	@echo "build           -- build python package"
	@echo ""
	@echo "pypi            -- upload package to pypi"
	@echo ""

test:
	pytest

ci: ruff pylint mypy test

mypy:
	@mypy src/pyvlx

build:
	@python3 -m build

pypi:
	@rm -f dist/*
	@python3 -m build
	@twine upload dist/*

pylint:
	@pylint src/pyvlx test/*.py examples/*.py

ruff:
	 @ruff check

coverage:
	pytest --cov --cov-report html --verbose

.PHONY: test build
