#!/usr/bin/env bash

if [[ ! -f /var/run/renderd/mod_tile/ ]]; then
  mkdir -p /var/run/renderd/mod_tile/
fi

/usr/sbin/apache2ctl -DFOREGROUND
