ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION as base
WORKDIR /python
COPY . ./
RUN pip install -e .[test]

########
# Django
########
FROM base as django
RUN pip install django

############
# SqlAlchemy
############
FROM base as sqlalchemy
RUN pip install sqlalchemy
