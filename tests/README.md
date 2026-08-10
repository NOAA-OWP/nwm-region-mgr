# Tests README

This directory contains the unit, integration, and slow tests for the package. The test suite is designed to validate 
configuration handling, data processing logic, and workflow components such as formulation and parameter regionalization.

The following types of tests are included currently:
* **Unit tests**: check individual functions or methods in isolation, using small inputs and mocked dependencies. 
They run quickly and are designed to verify core logic and edge cases. These tests should run frequently during 
local development and on every CI commit/PR.
* **Integration tests**: verify that multiple components work correctly together, focusing on data flow and interfaces 
  between modules. They may use lightweight I/O and are moderately fast. These should run on every PR or merge to 
  development (or at least daily in CI)
* **Slow tests**: tests exercise end-to-end workflows with realistic configurations and data. They validate overall 
  system behavior and are typically slower so can be run less frequently, such as nightly, before releases, or for 
  major refactors or PRs.


## Overview

Tests are written using **pytest** and organized by feature area. They focus on:

* Configuration validation (YAML + Pydantic models)
* Pipeline component behavior
* Data and schema validation
* Error handling and edge cases
* Regression and smoke tests for workflows

---

## Directory Structure

```
tests/
├── parreg/
├── formreg/
├── conftest.py
└── README.md
```

* `parreg/`, `formreg/`, etc. — feature-specific test modules
* `conftest.py` — shared pytest fixtures

---

## Requirements

Install test dependencies:

```
pip install pytest
```
---

## Test Markers

Tests can be marked with custom markers to categorize them. Currently used markers (as defined in `pyproject.toml`) 
include:
* `@pytest.mark.unit` — for unit tests
* `@pytest.mark.integration` — for integration tests
* `@pytest.mark.slow` — for slow end-to-end tests. Currently these include tests that run the full `formreg` and 
  `parreg` pipelines (for each of the seven supported algorithms) using the sample configs defined in `configs/`.

---

## Running Tests

Run all tests (unit, integration, and slow):

```
pytest
```

Run only unit tests (assuming they are marked with `@pytest.mark.unit`):

```
pytest -m unit
```
Run only integration tests:

```
pytest -m integration
```
Run only slow tests:

```
pytest -m slow
```

Run all non-slow tests:

```
pytest -m "not slow"
```

Run with verbose output:

```
pytest -v
```

Run a specific file:

```
pytest tests/parreg/test_parreg_process_config.py
```

Run a directory:

```
pytest tests/parreg/
```

Run a single test:

```
pytest tests/parreg/test_parreg_process_config.py::test_parreg_pipeline_smoke
```
---

## Fixtures

Shared fixtures are defined in `conftest.py`. Others are defined in the test modules themselves. 

---

## Test Data Guidelines

* Keep test datasets **small**
* Use synthetic or reduced samples
* Avoid large binary files
* Do not include sensitive or licensed data
* Prefer generated temporary data when possible

---

## Writing New Tests

Follow these conventions:

**Naming**

```
test_<module>.py
test_<function>_<condition>()
```

**Pattern**

```
arrange → act → assert
```

Example:

```
def test_config_missing_field_raises():
    cfg = build_invalid_config()
    with pytest.raises(ValueError):
        validate_config(cfg)
```

---

## Smoke Tests

Smoke tests verify that a full workflow step runs without crashing using minimal inputs. They should:

* use smallest valid config
* avoid heavy computation
* run quickly
* not depend on external systems unless mocked

---

## Temporary Files

Use pytest temporary directories instead of writing to the repo:

```
def test_output(tmp_path):
    out = tmp_path / "result.yaml"
```

---

## Debugging Failures

Show print/log output:

```
pytest -s
```

Stop on first failure:

```
pytest -x
```

Drop into debugger:

```
pytest --pdb
```

---

## Continuous Integration Notes

Tests should:

* run without network access
* avoid external services
* not require Docker or SLURM unless explicitly marked and skipped by default
* complete within reasonable time

Use markers or skips for environment-dependent tests.

---

## Contributing Test Cases

When fixing a bug:

1. Add a failing test first (if possible)
2. Implement the fix
3. Verify the test passes
4. Ensure no regressions


