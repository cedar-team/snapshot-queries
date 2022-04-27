#!/usr/bin/env bash
# Run tests locally against one or more versions of Python, optionally updating
# snapshots

# -e: if any command fails exit immediately
# -u: fail if undefined variable is used
# -o pipefail: return value of a pipeline is the return value of the rightmost command
set -euo pipefail

print_in_cyan() {
    printf "\x1B[36m%b\x1B[0m\n" "$*"
}

PYTHON_VERSIONS=('3.10')
SNAPSHOT_UPDATE="--snapshot-update"

for arg in "$@"; do
  case $arg in
    --python-version=*)
      PYTHON_VERSIONS=("${arg#*=}")
      ;;
    --no-snapshot-update)
      SNAPSHOT_UPDATE=""
      ;;
    *)
      # unknown option
      ;;
  esac
done

for PYTHON_VERSION in "${PYTHON_VERSIONS[@]}"
do
    print_in_cyan "\nTesting Python $PYTHON_VERSION"

    docker-compose build --build-arg PYTHON_VERSION="$PYTHON_VERSION"
    docker-compose run -e --rm testing_environment tox -e django-and-sqlalchemy -- "$SNAPSHOT_UPDATE"
done
