# Verification

Verified on 2026-11-03 with Python 3.14.3, pytest 9.2.0, mypy 2.4.1 and pyflakes 4.1.0.

## Tests

Command: `.venv/bin/python -m pytest -q`

```text
28 passed in 0.03s
```

Tests cover all five payment methods and an additional provider; abstract notifier failures and per-channel truncation; VAT changes; audit mutation restrictions; role identity and historical pay; three structurally compatible write targets; immutable money, unsupported operands and currency mismatch; filtered/unfiltered search; original, fixed and reordered MRO; payment-name normalization and unknown names.

## Valid Protocol usage

Command: `.venv/bin/python -m mypy task06.py`

```text
Success: no issues found in 1 source file
```

## Intentionally invalid Protocol usage

Command: `.venv/bin/python -m mypy --no-incremental experiments/bad_target.py`

Expected exit code 1:

```text
experiments/bad_target.py:3: error: Argument 2 to "export_report" has incompatible type "object"; expected "Writable"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

## Original duplicate method

Command: `.venv/bin/python -m pyflakes experiments/original_search.py`

Expected exit code 1:

```text
experiments/original_search.py:10:5: redefinition of unused 'search' from line 6
```

## Working files

Command: `.venv/bin/python -m pyflakes task*.py`

Exit code 0; no findings.

The two expected static-analysis failures are isolated in experiments. They are evidence of the bugs described in the assignment, not failures in the working solutions. Optional E1–E5 are not implemented.
