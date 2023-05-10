#!/bin/bash

vm_running() {
  local token=$1
  local instance_id=$2
  vm_info=$(curl -s -H "Authorization: Bearer ${token}" https://compute.api.cloud.yandex.net/compute/v1/instances/${instance_id})
  vm_status=$(echo "$vm_info" | python -c "import sys, json; print(json.load(sys.stdin)['status'])")
  if [ "$vm_status" = RUNNING ]
  then  return 0
  else return 1
  fi
}

if vm_running "$1" "$2";
then
  echo "VM with id ${2} already running"
  exit 0
fi

echo "Starting VM with id ${2}"
curl -X POST -H "Authorization: Bearer ${1}" https://compute.api.cloud.yandex.net/compute/v1/instances/${2}:start

until vm_running "$1" "$2"; do
  >&2 echo "Waiting for VM with id ${2} to become available..."
  sleep 5
done
>&2 echo "VM with id ${2} is available"
