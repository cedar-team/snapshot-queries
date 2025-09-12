# Contributing

Contributions are welcome. For all non-trivial changes, please create an issue first to help us track what is being worked on. PR commits should follow the angular style for compatibility with our automated release tool. See [here](https://www.conventionalcommits.org/en/v1.0.0/) for an explanation of the allowable commit message format.

Breaking changes will cause the major version number of the library to be incremented.
`feat` changes will cause the minor version number to be incremented.
`fix` and `perf` changes will cause the patch version number to be incremented.
The commit messages for the foregoing will be automatically added to the changelog upon release.

No other change types will cause a release or be added to the changelog.

## Local Development

### Running tests

First, make sure your images are up to date by running `docker compose build`.

The docker compose setup can be used for local development and testing. It specifies two services, `local_development`, and `testing_environment`. `testing_environment` is used to run tests in CI. For fast iteration during local development, you can run the `local_development` container like so:

```
docker compose run --rm -w /python local_development bash
```

From this shell, you can run the tests using the test scripts in the `tests` directory. To run an entire suite of tests, you can use tox from within the container.

### Running Matrix tests and updating snapshots

If you'd like to run a matrix build, you can use `test.sh` at the top level of the repo. You can specify a specific python version or run it on the default set of python versions. If you make a change to a test that may change snapshots, you should regenerate snapshots using the `--snapshot-update` argument.

## Formatting & Linting

We format all of our code using `isort` and `black` and run some `flake8` lints. These are all checked in CI. To update your code to conform to our standards, you can run

```
docker compose run --rm -w /python local_development tox -e format
```

If you'd like to run the lint checks only, you can run

```
docker compose run --rm -w /python local_development tox -e lint
```
