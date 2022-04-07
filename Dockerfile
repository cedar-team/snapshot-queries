ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION as base

WORKDIR /python

RUN pip install tox==3.24.5

FROM base as development
# Configures a venv with django and sqlalchemy installed to facilitate local development
# and testing

# Add the bare minimum just so tox can set up the venv
COPY pyproject.toml /python
COPY setup.cfg /python
COPY tox.ini /python
COPY snapshot_queries /python/snapshot_queries/

ENV PATH=/venv-tox/bin:$PATH

RUN tox --devenv /venv-tox -e django-and-sqlalchemy
