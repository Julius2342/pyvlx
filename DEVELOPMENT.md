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

- `pyproject.toml` is the **single source of truth** for all dependency declarations:
  - `project.dependencies` — runtime requirements with capped major versions (`>=X.Y,<(X+1).0`), keeping the library flexible for consumers.
  - `project.optional-dependencies.test`, `.lint`, `.release` — dev/CI dependencies pinned to exact versions (`==X.Y.Z`) so builds are reproducible and Dependabot can detect and propose updates.
- `requirements/*.in` describe locked environment inputs for `uv pip compile`.
- `requirements/*.txt` are fully resolved lock files (including transitive dependencies) for reproducible installs in CI and local development.
- Generated requirements files are committed.

## Requirements handling

Regenerate lock files after dependency changes in `pyproject.toml` or updates to `requirements/*.in`:

```bash
make requirements
```

PR checklist:

- If `pyproject.toml` dependency versions changed, run `make requirements` and commit updated `requirements/*.txt` in the same PR.
- If `requirements/*.in` changed, run `make requirements` and commit updated `requirements/*.txt` in the same PR.
- If dependencies did not change, do not modify `requirements/*.txt`.
- For Dependabot PRs, this is handled automatically by the refresh workflow, see below.

Equivalent direct commands:

```bash
python3 -m pip install uv
uv pip compile --strip-extras requirements/production.in --output-file requirements/production.txt
uv pip compile --strip-extras requirements/testing.in --output-file requirements/testing.txt
uv pip compile --strip-extras requirements/release.in --output-file requirements/release.txt
```

### How Dependabot updates work

1. Dependabot monitors `pyproject.toml` for outdated `==` pins and creates a PR bumping them.
2. The `dependabot-refresh-requirements` workflow auto-triggers on the PR, regenerates `requirements/*.txt` lock files via `uv pip compile`, and pushes the updated files.
3. CI runs against the fully locked environment. You review and merge.

## CI vs manual operations

| Task | Normally handled by CI | Manual equivalent |
|---|---|---|
| Run linting and tests | `.github/workflows/ci.yml` | `make ci` |
| Regenerate requirements for Dependabot pip PRs | `.github/workflows/dependabot-refresh-requirements.yml` | `make requirements` |
| Build distributions | `.github/workflows/publish.yml` | `make build` |
| Publish distributions | `.github/workflows/publish.yml` via `pypa/gh-action-pypi-publish` | `make pypi` |

`make pypi` is a manual/local fallback using Twine. Normal release publishing is handled in CI.