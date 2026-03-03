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

The CI workflow executes:
- `pytest -q -m "smoke or integration or e2e or ui"` (push/PR fast lane)
- `pytest -q -m "smoke or integration or e2e or ui"` (scheduled/manual full regression, matrix-expanded)

## Portfolio Talking Point

Both styles are thin orchestration layers over the same `saucedemo/tasks`, `saucedemo/questions`, and `saucedemo/ui` model, which demonstrates framework consistency instead of duplicated automation logic.
