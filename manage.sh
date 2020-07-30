#!/usr/bin/env bash


if [ "$command" = "run" ]; then
  docker-compose up --remove-orphans -d apache
elif [ "$command" = "render" ]; then
  command="$1"; shift
  docker-compose run --rm -T renderd python3 /manage.py $@
else
  docker-compose run --rm -T manage $@
fi
