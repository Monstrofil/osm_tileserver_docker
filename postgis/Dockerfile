FROM mdillon/postgis

COPY ./initdb-hstore.sh /docker-entrypoint-initdb.d/11_init_hstore.sh
COPY ./initdb-custom-settings.sh /docker-entrypoint-initdb.d/99_init_custom.sh
COPY ./postgresql.conf.custom /postgresql.conf.custom