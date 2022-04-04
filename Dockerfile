ARG PYTHON_VERSION

FROM python:$PYTHON_VERSION as base

WORKDIR /python

RUN pip install tox==3.24.5

FROM base as development

# Add the bare minimum just so tox can set up the venv
ADD pyproject.toml /python
ADD setup.cfg /python
ADD tox.ini /python
ADD snapshot_queries /python/snapshot_queries

ENV PATH=/venv-tox/bin:$PATH

RUN tox --devenv /venv-tox -e django-and-sqlalchemy


