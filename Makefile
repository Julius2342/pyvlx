
all:
	@echo
	@echo "Available targets"
	@echo ""
	@echo "ci              -- run linting and tests"
	@echo ""
	@echo "test            -- execute test suite"
	@echo ""
	@echo "flake8          -- run flake8 checks"
	@echo ""
	@echo "isort           -- run isort checks"
	@echo ""
	@echo "mypy            -- run mypy checks"
	@echo ""
	@echo "pylint          -- run pylint tests"
	@echo ""
	@echo "pydocstyle      -- run pydocstyle tests"
	@echo ""
	@echo "coverage        -- create coverage report"
	@echo ""
	@echo "build           -- build python package"
	@echo ""
	@echo "requirements    -- generate requirements/*.txt from requirements/*.in"
	@echo ""
	@echo "pypi            -- upload package to pypi"
	@echo ""

test:
	pytest

ci: pydocstyle flake8 pylint isort mypy test

flake8:
	@flake8

isort:
	@isort --check-only test examples pyvlx

mypy:
	@mypy pyvlx

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
	pytest --cov --cov-report html --verbose

requirements:
	@python3 -m pip install pip-tools
	@python3 -m piptools compile --strip-extras requirements/production.in --output-file requirements/production.txt
	@python3 -m piptools compile --strip-extras requirements/testing.in --output-file requirements/testing.txt
	@python3 -m piptools compile --strip-extras requirements/release.in --output-file requirements/release.txt

.PHONY: test build requirements
