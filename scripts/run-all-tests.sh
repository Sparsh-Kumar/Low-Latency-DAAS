#!/usr/bin/env bash

for project in jobs/* libs/*; do
  [ -f "$project/pyproject.toml" ] || continue

  if find "$project/tests" -type f -name "test_*.py" -print -quit | grep -q .; then
    uv run --project "$project" --locked pytest -s "$project/tests"
  fi
done

