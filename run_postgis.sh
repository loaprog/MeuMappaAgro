#!/bin/bash

docker run --name postgis \
  -e POSTGRES_DB=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=rrh44valDBinB7r1 \
  -p 5433:5432 \
  -v $(pwd)/data/postgis:/var/lib/postgresql/data \
  -d postgis/postgis
