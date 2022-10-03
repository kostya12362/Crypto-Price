FROM python:3.9


RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN pip install --no-cache-dir pipenv
ENV PYTHONUNBUFFERED $PWD
WORKDIR /api
COPY api/Pipfile* /api

RUN pipenv install --deploy --system
COPY api /api
CMD ['chmod', '+x', 'db.sh']

CMD ["python", "db.py"]

EXPOSE 5007

ENTRYPOINT ["python", "main.py"]