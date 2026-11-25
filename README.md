# ci-quality-gate

A CI quality gate built twice: as a **GitLab CI** pipeline and as a **GitHub Actions** workflow, running the same
checks on a small Python library. Every push runs lint, the tests on several Python versions and the Terraform checks;
any failure turns the pipeline red.

## The GitLab pipeline (`.gitlab-ci.yml`)

```
lint             test                          infra
ruff  ───────►   pytest [3.11]   ──────────►   terraform-validate
                 pytest [3.12]                 (fmt -check, init -backend=false, validate)
                 └─ JUnit report → Tests tab
```

- **Stages run in order; jobs in a stage run in parallel.** If a stage fails, the later ones don't start.
- **`parallel: matrix`** runs the test job once per Python version, as two parallel jobs.
- **JUnit report:** `pytest --junitxml` plus `artifacts: reports: junit`. GitLab shows each test's result in the
  pipeline's **Tests** tab and in merge requests, so you don't read logs to find a failure. `when: always` keeps
  the report when tests fail, which is when it's needed.
- **pip cache:** `PIP_CACHE_DIR` inside the project, cached per job image, so later pipelines don't download
  every package again.
- Each job starts in a fresh container (`image:`), so nothing leaks from one job to the next.

**Seen working:** a test broken on purpose made both `pytest` jobs fail; `ruff` passed and `terraform-validate` was
skipped, because the stage before it failed. After the fix the pipeline is green: 24 test results (12 tests × 2
Python versions), all passed.

## The same gate in GitHub Actions (`.github/workflows/ci.yml`)

| | GitLab CI | GitHub Actions |
|---|---|---|
| File | `.gitlab-ci.yml` | `.github/workflows/ci.yml` |
| Order | stages: lint → test → infra | two jobs in parallel: `test` (lint + tests), `terraform` |
| Python versions | 3.11, 3.12 with `parallel: matrix` | 3.11, 3.12, 3.13 with `strategy: matrix` |
| Runs in | a container per job (`image:`) | a VM per job (`runs-on: ubuntu-latest`) |
| Test results | JUnit report in the Tests tab | job log |
| Dependency cache | `cache:` | none yet |
| Terraform | the `hashicorp/terraform` image | a pinned version installed in a shell step |

## What's tested

- `cidr_utils.py`: three IP/CIDR helpers (`ip_in_cidr`, `cidrs_overlap`, `num_usable_hosts`), standard library only.
- `test_cidr_utils.py`: 12 pytest cases. No network or services, so they run the same on a laptop and in CI.
- `terraform/`: a reproducible test-environment definition. Each `apply` gets a unique name (e.g. `ci-test-4c6e73b0`)
  and writes an environment manifest. It uses the `random` and `local` providers, so it runs offline with no cloud
  account. CI checks formatting and validity on every change, so broken infrastructure code is caught like broken
  Python.

## Run it locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ruff check .      # lint
pytest -v         # tests

cd terraform
terraform init && terraform fmt -check && terraform validate   # what CI checks
terraform apply   # create a uniquely named test environment manifest
terraform destroy # remove it
```

`confluence-howto.md` is a step-by-step guide to setting up the GitHub Actions workflow.
