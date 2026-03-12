# Development

This document describes local checks, dependency management, and release-related contributor workflows.

## Local code checks

Install development dependencies:

```bash
pip install -e .[dev]
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

`pyproject.toml` is the single source of truth for all dependency declarations:

- **Runtime deps** (`project.dependencies`) use `>=X.Y,<(X+1).0` — flexible for library consumers, capped at the next major version to prevent surprise breakage.
- **Dev deps** (`project.optional-dependencies.dev`, `.release`) are pinned to exact versions (`==X.Y.Z`) so CI builds are reproducible and Dependabot can detect and propose updates.

### How Dependabot updates work

1. Dependabot monitors `pyproject.toml` for outdated `==` pins and creates a PR bumping them.
2. CI runs against the updated pins. You review and merge.

## CI vs manual operations

| Task | Normally handled by CI | Manual equivalent |
|---|---|---|
| Run linting and tests | `.github/workflows/ci.yml` | `make ci` |
| Build distributions | `.github/workflows/publish.yml` | `make build` |
| Publish distributions | `.github/workflows/publish.yml` via `pypa/gh-action-pypi-publish` | `make pypi` |

`make pypi` is a manual/local fallback using Twine. Normal release publishing is handled in CI.