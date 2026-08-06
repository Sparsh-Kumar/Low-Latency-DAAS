# Low-Latency Data as a Service

Low-Latency Data as a Service is an open project for collecting market data for quantitative research.

The goal is to provide a reusable data platform that allows researchers and developers to consume low-latency market data without building every ingestion component from scratch.

The project currently supports cryptocurrency market data delivered over WebSocket connections. Its job-based architecture is intended to support additional low-latency market-data protocols, including ITCH and FIX, in the future.

## Current Scope

The repository contains independent jobs for collecting:

- Live tickers
- Live trades
- Live order books

Each job manages its dependencies with uv and can be developed, linted, tested, and deployed independently.

## Project Structure

```text
.
├── config/                 Shared application configuration
├── jobs/                   Independent market-data jobs
│   ├── live_orderbooks/
│   ├── live_tickers/
│   └── live_trades/
├── libs/                   Reusable Python libraries
│   ├── lib-exception/
│   └── lib-logger/
├── scripts/                Repository automation scripts
├── terraform/              Development and production infrastructure
└── .githooks/              Shared Git hooks
```

## Requirements

- Python 3.12
- uv
- Git
- Docker, when building or running container images

## Setting Up a Job

Each job has its own `pyproject.toml`, `uv.lock`, and virtual environment.

From the repository root, synchronize a job environment:

```bash
uv sync --project jobs/live_tickers --locked
```

Run the job inside its managed environment:

```bash
uv run \
  --project jobs/live_tickers \
  --locked \
  python jobs/live_tickers/job.py
```

Replace `live_tickers` with `live_trades` or `live_orderbooks` to work with another job.

## Linting and Formatting

Every job defines its Ruff configuration in its own `pyproject.toml`. The repository lint script iterates through every directory under `jobs/` and runs that job's lint and formatting checks.

For a job to be checked, it must contain:

- `pyproject.toml`
- A `[tool.ruff]` configuration section
- Ruff in its development dependencies
- `uv.lock`

The lint script runs the equivalent of:

```bash
ruff check <job-directory>
ruff format --check <job-directory>
```

These commands validate the code without modifying it.

### Configure the Git Hook

Run the following commands once from the repository root:

```bash
git config core.hooksPath .githooks
sudo chmod +x ./.githooks/pre-commit
sudo chmod +x ./scripts/lint-jobs.sh
```

The commands perform the following setup:

1. `git config core.hooksPath .githooks` tells Git to load hooks from the committed `.githooks` directory instead of `.git/hooks`.
2. `sudo chmod +x ./.githooks/pre-commit` makes the pre-commit hook executable.
3. `sudo chmod +x ./scripts/lint-jobs.sh` makes the job lint script executable.

If you own the repository files and already have permission to modify them, `sudo` is not required:

```bash
chmod +x ./.githooks/pre-commit
chmod +x ./scripts/lint-jobs.sh
```

### Run Linting Manually

Run all job checks from the repository root:

```bash
./scripts/lint-jobs.sh
```

The script checks every job and returns a non-zero exit code if any lint rule, formatting rule, project configuration, or lockfile check fails.

### Run Linting Before a Commit

After configuring the Git hook, linting runs automatically when creating a commit:

```bash
git commit
```

If a check fails, the commit is stopped and Ruff prints the files and rules that require attention.

### Fix Ruff Issues

Apply safe lint fixes to a job:

```bash
uv run \
  --project jobs/live_tickers \
  --locked \
  ruff check --fix jobs/live_tickers
```

Format the job using its Ruff configuration:

```bash
uv run \
  --project jobs/live_tickers \
  --locked \
  ruff format jobs/live_tickers
```

Run the repository lint script again after applying fixes:

```bash
./scripts/lint-jobs.sh
```

## Extending the Platform

The current jobs focus on cryptocurrency WebSocket feeds, but the architecture is designed around independent ingestion jobs and reusable libraries. New jobs can extend the platform to other exchanges, asset classes, and low-latency protocols such as ITCH and FIX while retaining the same dependency, linting, containerization, and deployment patterns.
