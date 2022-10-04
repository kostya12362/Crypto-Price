FROM python:3.9


RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install --no-cache-dir pipenv
ENV PYTHONUNBUFFERED $PWD
WORKDIR /tasks
COPY tasks/Pipfile* /tasks
RUN pipenv install --deploy --system
COPY tasks /tasks