#!/usr/bin/env bash

# git config core.hooksPath .githooks
# chmod +x ./.githooks/pre-commit
# chmod +x ./scripts/lint-projects.sh

set -uo pipefail

SCRIPT_DIRECTORY="$(
  cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &&
  pwd
)"

PROJECT_ROOT="$(
  cd -- "$SCRIPT_DIRECTORY/.." &&
  pwd
)"

PROJECT_DIRECTORIES=(
  "$PROJECT_ROOT/jobs"
  "$PROJECT_ROOT/libs"
)

overall_status=0
projects_checked=0

for parent_directory in "${PROJECT_DIRECTORIES[@]}"; do
  if [[ ! -d "$parent_directory" ]]; then
    echo "ERROR: Directory does not exist: $parent_directory"
    overall_status=1
    continue
  fi

  project_type="$(basename "$parent_directory")"

  for project_directory in "$parent_directory"/*; do
    [[ -d "$project_directory" ]] || continue

    project_name="$(basename "$project_directory")"
    pyproject_file="$project_directory/pyproject.toml"
    lock_file="$project_directory/uv.lock"

    echo
    echo "Checking $project_type project: $project_name"

    if [[ ! -f "$pyproject_file" ]]; then
      echo "ERROR: $project_name does not contain pyproject.toml"
      overall_status=1
      continue
    fi

    if ! grep -q '^\[tool\.ruff\]' "$pyproject_file"; then
      echo "ERROR: $project_name does not contain Ruff configuration"
      overall_status=1
      continue
    fi

    if [[ ! -f "$lock_file" ]]; then
      echo "ERROR: $project_name does not contain uv.lock"
      overall_status=1
      continue
    fi

    projects_checked=$((projects_checked + 1))

    if ! uv run \
      --project "$project_directory" \
      --locked \
      ruff check "$project_directory"; then
      overall_status=1
    fi

    if ! uv run \
      --project "$project_directory" \
      --locked \
      ruff format --check "$project_directory"; then
      overall_status=1
    fi
  done
done

if [[ "$projects_checked" -eq 0 ]]; then
  echo
  echo "ERROR: No jobs or libraries were checked."
  exit 1
fi

exit "$overall_status"

