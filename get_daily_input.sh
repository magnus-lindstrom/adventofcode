#!/usr/bin/env bash

set -e

if ! $(basename $(pwd) | grep -Pq '20\d{2}'); then
  echo "Must be in a directory named '20XX'."
  exit 1
fi
year=$(basename $(pwd))

if ! [ -f ../.session_cookie ]; then
  echo "No ../.session_cookie file defined. See README.md."
  exit 1
fi

mkdir -p inputs

for day in $(seq 1 25); do
  if ! [ -f "./inputs/${day}" ]; then
    curl --silent -H "Cookie: session=$(cat ../.session_cookie)" \
      -o "inputs/${day}" \
      "https://adventofcode.com/${year}/day/${day}/input"
    if [ "$(head -n1 inputs/${day} | cut -d ' ' -f 1,2)" = "Please don't" ]; then
      echo "Day ${day} and beyond have not been published yet."
      rm "inputs/${day}"
      break
    fi
    echo "Fetched y${year}d${day} input."
  fi
done
echo "Done"
