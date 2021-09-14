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
SNAPSHOT_UPDATE="--snapshot-update"

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
    --no-snapshot-update)
      SNAPSHOT_UPDATE=""
      ;;
    *)
      # unknown option
      ;;
  esac
done

for PYTHON_VERSION in $PYTHON_VERSIONS
do
    print_in_cyan "\nTesting Python $PYTHON_VERSION"
    export PYTHON_VERSION=$PYTHON_VERSION

    if [ "$TEST_DJANGO" = true ]; then
        docker-compose build test-django
        docker-compose run --rm test-django tests/test_django/test.sh $SNAPSHOT_UPDATE
    fi

    if [ "$TEST_SQLALCHEMY" = true ]; then
        docker-compose build test-sqlalchemy
        docker-compose run --rm test-sqlalchemy tests/test_sqlalchemy/test.sh $SNAPSHOT_UPDATE
    fi
done
