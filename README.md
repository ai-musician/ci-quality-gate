# cicd-demo

A tiny Python project demonstrating a **CI/CD pipeline with GitHub Actions**.

- `cidr_utils.py` — three small CIDR/IP helper functions (standard library only).
- `test_cidr_utils.py` — pytest tests for them.
- `.github/workflows/ci.yml` — the GitHub Actions workflow: on every push and
  pull request it lints with `ruff` and runs the tests against Python 3.11 and
  3.12, in parallel.

## Run it locally

```bash
cd cicd-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

ruff check .      # lint
pytest -v         # tests
```

## Push it to GitHub (so the Actions tab lights up)

```bash
git init
git add .
git commit -m "CI/CD demo with GitHub Actions"
git branch -M main
# create an empty repo on github.com first, then:
git remote add origin https://github.com/<your-username>/cicd-demo.git
git push -u origin main
```

Open the repo's **Actions** tab — the `CI` workflow runs automatically and shows
a green check when lint + tests pass on both Python versions.

## What this demonstrates

- **CI (Continuous Integration):** every change is automatically linted and
  tested before it can be merged — a quality gate, not a manual step.
- **Matrix builds:** the same suite runs against multiple Python versions to
  catch version-specific breakage.
- **Hermetic tests:** the tests have no external dependencies (no network, no
  services), so they run identically on a laptop and in CI — reproducible by
  construction.
