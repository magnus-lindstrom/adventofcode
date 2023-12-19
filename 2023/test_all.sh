#!/usr/bin/env bash

set -e

# find all files individually and test them (not having 'test_' in the name
# excludes them from being found by pytest otherwise)
#
# 'files' is an array, which is later expanded into separate arguments for
# pytest
files=( $(fdfind --max-depth=1 '\d{1,2}\.py' src/) )
pytest -n 4 --durations=0 --durations-min='0.1' "${files[@]}"
