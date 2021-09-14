#!/usr/bin/env bash
# -e: if any command fails exit immediately
# -u: fail if undefined variable is used
# -o pipefail: return value of a pipeline is the return value of the rightmost command
set -euo pipefail

print_in_cyan() {
    printf "\x1B[36m%b\x1B[0m\n" "$*"
}

PYTHON_VERSIONS="3.6  3.7  3.8  3.9"
TEST_SQLALCHEMY=true
TEST_DJANGO=true

for i in "$@"; do
  case $i in
    --python-version=*)
      PYTHON_VERSIONS="${i#*=}"
      shift # past argument=value
      ;;
    --django)
      TEST_SQLALCHEMY=false
      shift
      ;;
    --sqlalchemy)
      TEST_DJANGO=false
      shift
      ;;
    *)
      # unknown option
      ;;
  esac
done

for PYTHON_VERSION in $PYTHON_VERSIONS
do
    print_in_cyan "\nTesting Python $PYTHON_VERSION"

    if [ "$TEST_DJANGO" = true ]; then
        PYTHON_VERSION=$PYTHON_VERSION docker-compose up --build test-django
    fi

    if [ "$TEST_SQLALCHEMY" = true ]; then
        PYTHON_VERSION=$PYTHON_VERSION docker-compose up --build test-sqlalchemy
    fi
done
