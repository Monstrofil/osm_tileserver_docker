FROM ubuntu:20.04 AS builder

ARG CARTO_STYLE_TAG=v5.2.0

# to avoid questions from tzdata
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

RUN apt update
RUN apt install -y make cmake g++ libboost-dev libboost-system-dev \
  libboost-filesystem-dev libexpat1-dev zlib1g-dev \
  libbz2-dev libpq-dev libproj-dev lua5.3 liblua5.3-dev git python3

RUN git clone git://github.com/openstreetmap/osm2pgsql.git
RUN cd osm2pgsql \
 && mkdir build \
 && cd build \
 && cmake .. \
 && make \
 && make install

RUN apt install -y netcat
RUN git clone -b ${CARTO_STYLE_TAG} --depth=1 git://github.com/gravitystorm/openstreetmap-carto.git

COPY manage.py /
