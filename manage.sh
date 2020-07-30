#!/usr/bin/env bash


if [ "$1" = "run" ]; then
  docker-compose up --remove-orphans -d apache
elif [ "$1" = "render" ]; then
  command="$1"; shift
  docker-compose run --rm -T renderd python3 /manage.py $@
else
  docker-compose run --rm -T manage $@
fi
