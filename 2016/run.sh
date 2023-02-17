#!/usr/bin/env bash

set -e

POSITIONAL_ARGS=()

mode=Release

while [[ $# -gt 0 ]]; do
	case $1 in
		-d|--debug)     mode=Debug; shift;;
		-*|--*)         echo "Unknown option $1"; exit 1;;
		*)              POSITIONAL_ARGS+=("$1"); shift;;
	esac
done

set -- "${POSITIONAL_ARGS[@]}"

rm -r build
mkdir -p build
cmake --config "${mode}" -B build -S src

cd build
make

cd ..
echo
build/aoc2016
