#!/usr/bin/env sh

# shellcheck disable=SC2155
echo "replacing vars"
export EXISTING_VARS=$(awk 'BEGIN {for (k in ENVIRON) { print k }}' | sed 's/^/\$/g' | paste -sd,)
file=/usr/share/nginx/html/envs.js
echo $EXISTING_VARS
cat $file | envsubst $EXISTING_VARS | tee $file
cat $file
