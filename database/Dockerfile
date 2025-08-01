FROM postgres:16.5-alpine

RUN mkdir -p /data

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

# echo the env variables inside the container
CMD ["echo", "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"]

CMD ["postgres"]
