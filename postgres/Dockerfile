FROM postgres:11.2

RUN apt-get update && apt-get install -y postgresql-contrib postgresql-plpython3-11

COPY init_db.sh /docker-entrypoint-initdb.d/init_db.sh
