# Release & Publish Checklist

Use this checklist when preparing to push and publish a new VisionForAll release.

## 1) Local repository hygiene
- [ ] Ensure branch is up to date with target base branch.
- [ ] Ensure working tree is clean: `git status`.
- [ ] Ensure version in `pyproject.toml` is correct.

## 2) Quality gates
- [ ] Run lint: `PYTHONPATH=visionforall python -m ruff check .`
- [ ] Run tests: `PYTHONPATH=visionforall python -m pytest -q`
- [ ] Smoke CLI help: `PYTHONPATH=visionforall python -m visionforall.main --help`

## 3) Packaging checks
- [ ] Create isolated venv and run `pip install -e .`
- [ ] Validate entrypoint: `visionforall --help`
- [ ] Optionally verify extras install:
  - `pip install -e .[vision]`
  - `pip install -e .[stt]`
  - `pip install -e .[tts]`
  - `pip install -e .[rag]`

## 4) Documentation checks
- [ ] README reflects current capabilities and known limitations.
- [ ] SECURITY policy and CONTRIBUTING docs are up to date.
- [ ] Changelog/release notes drafted.

## 5) Push & PR
- [ ] Push branch: `git push -u origin <branch>`
- [ ] Open PR using `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] Confirm CI passes on PR.

## 6) GitHub release (optional)
- [ ] Tag release: `git tag vX.Y.Z && git push origin vX.Y.Z`
- [ ] Create GitHub release notes with install + migration notes.

## 7) PyPI publish (optional)
- [ ] Build artifacts:
  - `python -m pip install build twine`
  - `python -m build`
- [ ] Check artifacts: `python -m twine check dist/*`
- [ ] Upload: `python -m twine upload dist/*`

> Keep offline/privacy defaults unchanged unless explicitly documented.
