#!/usr/bin/env bash

MAPNIK_XML_PATH="/openstreetmap-carto/mapnik.xml"
IMPORT_DONE_FILE="/var/run/renderd/mod_tile/.import_done1"

if [[ ! -f /var/run/renderd/mod_tile/ ]]; then
  mkdir -p /var/run/renderd/mod_tile/
fi

# replace config stubs with real values
sed -i "s/\${PG_HOSTNAME}/${POSTGRES_HOST}/g" "${MAPNIK_XML_PATH}"
sed -i "s/\${PG_DBNAME}/${POSTGRES_DB}/g" "${MAPNIK_XML_PATH}"
sed -i "s/\${PG_USERNAME}/${POSTGRES_USER}/g" "${MAPNIK_XML_PATH}"
sed -i "s/\${PG_PASSWORD}/${POSTGRES_PASSWORD}/g" "${MAPNIK_XML_PATH}"

cd /mod_tile && renderd -f -c "${RENDERD_CONF_PATH}"
