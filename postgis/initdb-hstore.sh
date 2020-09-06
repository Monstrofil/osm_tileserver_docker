#!/bin/sh

set -e
# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

# Load hstore into all databases
echo "Loading PostGIS extensions into $DB"
psql -U "${PGUSER}" -d "${POSTGRES_DB}" -c "CREATE EXTENSION IF NOT EXISTS hstore;"
psql -U "${PGUSER}" -d "${POSTGRES_DB}" -f /postgis-vt-util.sql