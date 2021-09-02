#!/usr/bin/env bash
# cd to the directory this script lives in
cd "$( dirname "${BASH_SOURCE[0]}" )"

nosetests -s . "$@"
