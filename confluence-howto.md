# How To: CI/CD with GitHub Actions (a hands-on demo)

A short, practical walkthrough of setting up a CI/CD pipeline using GitHub
Actions, using a tiny Python project as the example. Built to be demoable.

---

## What is CI/CD (in one paragraph)

**CI (Continuous Integration)** means every code change is automatically built,
linted, and tested the moment it's pushed — so problems are caught in minutes,
by a machine, instead of later, by a person. **CD (Continuous Delivery/
Deployment)** extends that: once the checks pass, the change is automatically
packaged and (optionally) released. **GitHub Actions** is GitHub's built-in
automation engine that runs these steps for you, defined in a YAML file in your
repo. No separate CI server to maintain.

---

## The example project

Three files do the real work:

- `cidr_utils.py` — three small CIDR/IP helper functions (standard library only).
- `test_cidr_utils.py` — pytest tests for them (12 test cases).
- `.github/workflows/ci.yml` — the pipeline definition.

---

## The pipeline, explained line by line

```yaml
name: CI

on:                          # WHEN the pipeline runs
  push:
    branches: [main]         #   - on every push to main
  pull_request:              #   - and on every pull request

jobs:
  test:
    runs-on: ubuntu-latest   # a fresh Linux VM, provisioned per run
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]   # run everything on BOTH versions

    steps:
      - uses: actions/checkout@v4          # 1. pull the repo's code
      - uses: actions/setup-python@v5      # 2. install the Python version
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install -r requirements.txt  # 3. install deps
      - run: ruff check .                  # 4. lint  (fails the build if messy)
      - run: pytest -v                     # 5. test  (fails the build if red)
```

Key ideas to call out:

- **`on:`** is the trigger. This pipeline is a *gate* — it runs before code
  merges, so broken code can't reach `main` unnoticed.
- **`matrix:`** runs the entire job once per Python version, in parallel. One
  config, multiple environments — catches version-specific breakage cheaply.
- **Each `run:` step fails the whole job on a non-zero exit code.** A lint
  warning or a single failing test turns the run red and blocks the merge.

---

## How to demo it (the 90-second version)

1. **Show it green:** open the repo's **Actions** tab — the latest run shows a
   green check, with the matrix expanded into `test (3.11)` and `test (3.12)`.
2. **Break it on purpose:** change one test's expected value (e.g. `254` → `999`),
   commit, push.
3. **Watch CI catch it:** the Actions tab shows a new run going red within a
   minute, with the exact failing assertion in the logs. On a pull request,
   the merge button is now blocked.
4. **Fix and re-push:** revert the change; the run goes green again.

That break-it/fix-it loop is the whole point of CI in one gesture: a machine
enforces quality on every change, automatically.

---

## Run it locally first (same commands CI runs)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ruff check .      # lint
pytest -v         # tests
```

Running the *same* commands locally that CI runs is the habit that keeps the
pipeline green: if it passes on your laptop, it passes in CI — because the
tests are **hermetic** (no network, no external services, reproducible
anywhere).
