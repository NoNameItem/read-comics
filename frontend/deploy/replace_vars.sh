#!/usr/bin/env sh

# shellcheck disable=SC2155
export EXISTING_VARS=$(awk 'BEGIN {for (k in ENVIRON) { print k }}' | sed 's/^/\$/g' | paste -sd,)
file=/usr/share/nginx/html/envs.js
cat $file | envsubst $EXISTING_VARS > $file
cat $file
