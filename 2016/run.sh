#!/usr/bin/env bash

set -e

rm -r build
mkdir -p build
cmake --config Release -B build -S src

cd build
make

cd ..
echo
build/aoc2016
