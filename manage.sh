#!/usr/bin/env bash

command="$1"; shift

if [ "$command" = "run" ]; then
  docker-compose up --remove-orphans -d apache
elif [ "$command" = "render" ]; then
  docker-compose run -T renderd python3 /manage.py $@
else
  docker-compose run -T manage $@
fi
