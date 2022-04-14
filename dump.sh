#!/bin/bash

if [ -z "$1" ]; then
  echo "No date given"
  exit 1
fi

docker exec --user postgres -it jaws-db pg_dump jaws-db > "./jaws-${1}.sql"
