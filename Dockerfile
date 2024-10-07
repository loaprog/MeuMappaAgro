ARG PG_VERSION=15
ARG TAG=latest

FROM quay.io/tembo/standard-cnpg:${PG_VERSION}-${TAG}
USER root

WORKDIR /

# Install dependencies for running postgis and mobilitydb
RUN apt-get update && \
    apt-get install -y \
    postgis \
    postgresql-15-postgis-scripts \
    git \
    cmake \
    libgeos-dev \
    libproj-dev \
    libprotobuf-c-dev \
    protobuf-c-compiler \
    libgdal-dev \
    libgsl-dev \
    libjson-c-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone and build MobilityDB
RUN git clone https://github.com/MobilityDB/MobilityDB && \
    cd MobilityDB && \
    git checkout v1.1.0rc1 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

# Cache all extensions
RUN set -eux; \
      cp -r $(pg_config --pkglibdir)/* /tmp/pg_pkglibdir; \
      cp -r $(pg_config --sharedir)/* /tmp/pg_sharedir;

ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV XDG_CACHE_HOME=/var/lib/postgresql/data/tembo/.cache

# Revert the postgres user to id 26
RUN usermod -u 26 postgres
USER 26
