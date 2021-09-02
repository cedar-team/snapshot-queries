#!/usr/bin/env bash
print_in_cyan() {
    printf "\x1B[36m%b\x1B[0m\n" "$*"
}

print_in_cyan "Testing Python 3.6"
PYTHON_VERSION=3.6 docker-compose run --rm  test ./manage.py test --snapshot-update

print_in_cyan "\nTesting Python 3.7"
PYTHON_VERSION=3.7 docker-compose run --rm  test ./manage.py test --snapshot-update

print_in_cyan "\nTesting Python 3.8"
PYTHON_VERSION=3.8 docker-compose run --rm  test ./manage.py test --snapshot-update

print_in_cyan "\nTesting Python 3.9"
PYTHON_VERSION=3.9 docker-compose run --rm  test ./manage.py test --snapshot-update
