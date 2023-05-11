#!/bin/bash

vm_running() {
  local token=$1
  local instance_id=$2
  vm_info=$(curl -s -H "Authorization: Bearer ${token}" "https://compute.api.cloud.yandex.net/compute/v1/instances/${instance_id}")
  vm_status=$(echo "$vm_info" | python -c "import sys, json; print(json.load(sys.stdin)['status'])")
  echo "${vm_status}"
  if [ "$vm_status" = RUNNING ]
  then  return 0
  else return 1
  fi
}

ssh_test() {
  if nc -z $1 22 2>/dev/null; then
    echo "$1 ✓"
    return 0
  else
    echo "$1 ✗"
    return 255
  fi
}

if vm_running "$1" "$2";
then
  echo "VM already running"
  exit 0
fi

echo "Starting VM"
curl -X POST -s -H "Authorization: Bearer ${1}" "https://compute.api.cloud.yandex.net/compute/v1/instances/${2}:start"

until vm_running "$1" "$2"; do
  >&2 echo "Waiting for VM  to become available..."
  sleep 5
done
>&2 echo "VM is available"

>&2 echo "Waiting for ssh..."
until ssh_test "${3}"; do
  >&2 echo "Waiting for ssh..."
  sleep 5
done

>&2 echo "ssh is available"
