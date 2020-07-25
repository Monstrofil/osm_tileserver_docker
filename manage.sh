#!/usr/bin/env bash

if [ "$1" = "run" ]; then
  docker-compose up --remove-orphans -d apache
else
  docker-compose run -T manage $@
fi
