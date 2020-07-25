#!/usr/bin/env bash

set -e

# Load hstore into all databases
echo "Loading PostGIS extensions into $DB"
"${psql[@]}" --dbname="$POSTGRES_DB" <<-'EOSQL'
  CREATE EXTENSION IF NOT EXISTS hstore;
EOSQL