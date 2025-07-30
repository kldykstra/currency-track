FROM postgres:16.5-alpine

RUN mkdir -p /data

COPY init.sql /docker-entrypoint-initdb.d/
COPY eurofxref-hist.csv /data/eurofxref-hist.csv

EXPOSE 5432

CMD ["postgres"]
