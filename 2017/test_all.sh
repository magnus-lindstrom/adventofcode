#!/usr/bin/env bash

set -e

# find all files individually and test them (not having 'test_' in the name
# excludes them from being found by pytest otherwise)
fdfind --max-depth=1 '\d{1,2}\.py' src/ | xargs pytest

