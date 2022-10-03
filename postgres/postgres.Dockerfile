FROM postgres:14-alpine3.14

WORKDIR postgres
COPY postgres /postgres

EXPOSE 5432
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
