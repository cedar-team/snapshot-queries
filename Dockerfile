ARG PYTHON_VERSION
FROM python:$PYTHON_VERSION
WORKDIR /python
COPY . ./
RUN pip install -e .[test]
