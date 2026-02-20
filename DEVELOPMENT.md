# Development

This document describes local checks, dependency management, and release-related contributor workflows.

## Local code checks

Install development dependencies:

```bash
# Fully locked test/lint environment (including package install)
pip install -r requirements/testing.txt
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

- `pyproject.toml` is the source of truth for package dependency intent:
  - `project.dependencies` for runtime requirements
  - `project.optional-dependencies.test` and `project.optional-dependencies.lint` for quality checks
  - `project.optional-dependencies.release` for packaging/release tooling
- `requirements/*.in` describe locked environment inputs for `pip-tools`.
- `requirements/*.txt` are fully pinned lock files for reproducible installs in CI and local development.
- Generated requirements files are committed.

## Requirements handling

Regenerate lock files after dependency intent changes in `pyproject.toml` or updates to `requirements/*.in`:

```bash
make requirements
```

PR checklist:

- If `pyproject.toml` dependency intent changed (runtime or optional dependency groups), run `make requirements` and commit updated `requirements/*.txt` in the same PR.
- If `requirements/*.in` changed, run `make requirements` and commit updated `requirements/*.txt` in the same PR.
- If dependencies did not change, do not modify `requirements/*.txt`.

Equivalent direct commands:

```bash
python3 -m pip install pip-tools
python3 -m piptools compile --strip-extras requirements/production.in --output-file requirements/production.txt
python3 -m piptools compile --strip-extras requirements/testing.in --output-file requirements/testing.txt
python3 -m piptools compile --strip-extras requirements/release.in --output-file requirements/release.txt
```

## CI vs manual operations

| Task | Normally handled by CI | Manual equivalent |
|---|---|---|
| Run linting and tests | `.github/workflows/ci.yml` | `make ci` |
| Regenerate requirements for Dependabot pip PRs | `.github/workflows/dependabot-refresh-requirements.yml` | `make requirements` |
| Build distributions | `.github/workflows/publish.yml` | `make build` |
| Publish distributions | `.github/workflows/publish.yml` via `pypa/gh-action-pypi-publish` | `make pypi` |

`make pypi` is a manual/local fallback using Twine. Normal release publishing is handled in CI.