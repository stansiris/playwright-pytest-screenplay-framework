# Codex Test Generation Workflow

This project demonstrates that Codex can generate and maintain both test styles on the same Screenplay model:
- BDD (`pytest-bdd` feature + step definitions)
- Direct pytest test modules

## Prompt Pattern: BDD

Use a prompt like:

```text
Create a BDD feature and step definitions for login.
Reuse existing Screenplay tasks/questions only.
Add markers that match pytest.ini.
```

Expected output:
- `tests/features/<flow>.feature`
- `tests/test_<flow>_bdd.py`

## Prompt Pattern: Direct Pytest

Use a prompt like:

```text
Create direct pytest tests for login success/failure using existing Screenplay tasks/questions.
Use smoke/integration markers and keep tests readable.
```

Expected output:
- `tests/test_<flow>.py`

## Validation Commands

```powershell
python -m ruff check tests
python -m black --check tests
pytest -q tests/test_login.py tests/test_login_bdd.py
```

## CI Marker Commands

The CI workflow executes marker-specific suites:
- `pytest -q -m "smoke or e2e"`
- `pytest -q -m "integration and not smoke and not ui"`
- `pytest -q -m "ui"`
- `pytest -q -m "smoke or integration or e2e"` (scheduled/manual full regression)

## Portfolio Talking Point

Both styles are thin orchestration layers over the same `saucedemo/tasks`, `saucedemo/questions`, and `saucedemo/ui` model, which demonstrates framework consistency instead of duplicated automation logic.
