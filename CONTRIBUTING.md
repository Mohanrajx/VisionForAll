# Contributing to VisionForAll

Thanks for your interest in improving accessible offline AI tooling.

## Development Setup
1. Create Python 3.11+ virtual environment.
2. Install dependencies: `pip install -e .[dev]`
3. Install hooks: `pre-commit install`
4. Run checks: `ruff check . && pytest -q`

## Pull Requests
- Keep changes scoped and documented.
- Add or update tests when behavior changes.
- Do not introduce cloud calls without explicit opt-in config.

## Review & OSPS Baseline Notes
- At least one maintainer review before merge.
- CI must pass lint + tests.
- Dependency updates should be pinned or bounded and justified in PR notes.
