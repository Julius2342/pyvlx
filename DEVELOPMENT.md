# Development

This document describes local checks, dependency management, and release-related contributor workflows.

## Local code checks

Install development dependencies:

```bash
# Test and lint dependencies declared in pyproject.toml, pinned by constraints
pip install -e .[test,lint] -c requirements/testing.txt
```

Run the full local check suite:

```bash
make ci
```

Run individual checks when needed:

```bash
make pydocstyle
make flake8
make pylint
make isort
make mypy
make test
```

Generate a local coverage report:

```bash
make coverage
```

## Dependency model

- `pyproject.toml` is the source of truth for dependency intent:
  - `project.dependencies` for runtime requirements
  - `project.optional-dependencies.test` and `project.optional-dependencies.lint` for quality checks
  - `project.optional-dependencies.release` for packaging/release tooling
- `requirements/*.txt` are pinned constraints files for reproducible installs in CI and local development.
- Generated requirements files are committed.

## Requirements handling

Regenerate constraints after dependency intent changes in `pyproject.toml`:

```bash
make requirements
```

Equivalent direct commands:

```bash
python3 -m pip install pip-tools
python3 -m piptools compile --strip-extras pyproject.toml --output-file requirements/production.txt
python3 -m piptools compile --strip-extras pyproject.toml --extra test --extra lint --output-file requirements/testing.txt
python3 -m piptools compile --strip-extras pyproject.toml --extra release --output-file requirements/release.txt
```

## CI vs manual operations

| Task | Normally handled by CI | Manual equivalent |
|---|---|---|
| Run linting and tests | `.github/workflows/ci.yml` | `make ci` |
| Regenerate requirements for Dependabot pip PRs | `.github/workflows/dependabot-refresh-requirements.yml` | `make requirements` |
| Build distributions | `.github/workflows/publish.yml` | `make build` |
| Publish distributions | `.github/workflows/publish.yml` via `pypa/gh-action-pypi-publish` | `make pypi` |

`make pypi` is a manual/local fallback using Twine. Normal release publishing is handled in CI.