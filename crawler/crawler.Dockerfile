FROM python:3.9


RUN apt-get update \
    && apt-get -y install libpq-dev gcc && apt-get install -y gettext
RUN pip install --no-cache-dir pipenv
ENV PYTHONUNBUFFERED $PWD
WORKDIR /crawler
COPY crawler/Pipfile* /crawler
RUN pipenv install --deploy --system
COPY crawler /crawler

EXPOSE 6801
