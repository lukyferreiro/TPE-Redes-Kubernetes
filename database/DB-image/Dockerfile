FROM postgres:15-alpine

COPY init.sql /docker-entrypoint-initdb.d/
COPY load_data.sql /docker-entrypoint-initdb.d/
COPY players.csv /docker-entrypoint-initdb.d/

CMD ["postgres"]