FROM postgres:12.2

ENV POSTGRES_PASSWORD=devpass \
    POSTGRES_DB=laserpiente
COPY 01_create.sql /docker-entrypoint-initdb.d/