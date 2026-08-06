#!/usr/bin/env bash

# git config core.hooksPath .githooks

set -uo pipefail

SCRIPT_DIRECTORY="$(
  cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &&
  pwd
)"

PROJECT_ROOT="$(
  cd -- "$SCRIPT_DIRECTORY/.." &&
  pwd
)"

JOBS_DIRECTORY="$PROJECT_ROOT/jobs"

overall_status=0
jobs_checked=0

for job_directory in "$JOBS_DIRECTORY"/*; do
  [[ -d "$job_directory" ]] || continue

  job_name="$(basename "$job_directory")"
  pyproject_file="$job_directory/pyproject.toml"
  lock_file="$job_directory/uv.lock"

  echo
  echo "Checking job: $job_name"

  if [[ ! -f "$pyproject_file" ]]; then
    echo "ERROR: $job_name does not contain pyproject.toml"
    overall_status=1
    continue
  fi

  if ! grep -q '^\[tool\.ruff\]' "$pyproject_file"; then
    echo "ERROR: $job_name does not contain Ruff configuration"
    overall_status=1
    continue
  fi

  if [[ ! -f "$lock_file" ]]; then
    echo "ERROR: $job_name does not contain uv.lock"
    overall_status=1
    continue
  fi

  jobs_checked=$((jobs_checked + 1))

  if ! uv run \
    --project "$job_directory" \
    --locked \
    ruff check "$job_directory"; then
    overall_status=1
  fi

  if ! uv run \
    --project "$job_directory" \
    --locked \
    ruff format --check "$job_directory"; then
    overall_status=1
  fi
done

if [[ "$jobs_checked" -eq 0 ]]; then
  echo
  echo "ERROR: No jobs were checked."
  exit 1
fi

exit "$overall_status"

