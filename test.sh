#!/usr/bin/env bash
# -e: if any command fails exit immediately
# -u: fail if undefined variable is used
# -o pipefail: return value of a pipeline is the return value of the rightmost command
set -euo pipefail

print_in_cyan() {
    printf "\x1B[36m%b\x1B[0m\n" "$*"
}

for PYTHON_VERSION in 3.6  3.7  3.8  3.9
do
    print_in_cyan "\nTesting Python $PYTHON_VERSION"
    PYTHON_VERSION=$PYTHON_VERSION docker-compose run --rm  test ./test.sh
done
