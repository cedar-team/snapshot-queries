ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION as base
WORKDIR /python

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY test.requirements.txt ./
RUN pip install -r test.requirements.txt

########
# Django
########
FROM base as django
RUN pip install django
COPY . ./
RUN pip install -e .[test]

############
# SqlAlchemy
############
FROM base as sqlalchemy
RUN pip install sqlalchemy
COPY . ./
RUN pip install -e .[test]

