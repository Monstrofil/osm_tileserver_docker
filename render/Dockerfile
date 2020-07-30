FROM ubuntu:20.04 AS builder

# to avoid questions from tzdata
ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

# install node 12 repository
RUN apt update && apt install -y curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -

# install Python, npm and all the mapnik dependencies
RUN apt install -y autoconf apache2-dev libtool libxml2-dev libbz2-dev libgeos-dev \
 libgeos++-dev libproj-dev gdal-bin libmapnik-dev mapnik-utils \
 python3-mapnik python3-psycopg2 git htop nodejs python3-pip libiniparser-dev

# install fonts
RUN apt install -y fonts-noto-cjk fonts-noto-hinted fonts-noto-unhinted ttf-unifont

# install node & python dependencies
RUN npm install -g carto
RUN pip3 install ruamel.yaml

# clone and compile mod_tile module
RUN git clone -b switch2osm git://github.com/SomeoneElseOSM/mod_tile.git \
 && cd mod_tile \
 && ./autogen.sh \
 && ./configure \
 && make -j 4 \
 && make install \
 && make install-mod_tile


FROM builder AS renderd

ARG CARTO_STYLE_TAG=v5.2.0

ENV POSTGRES_HOST=postgres
ENV POSTGRES_DB=default
ENV POSTGRES_USER=default
ENV POSTGRES_PASSWORD=default
ENV RENDERD_CONF_PATH=/usr/local/etc/renderd.conf

# clone and build carto style
RUN git clone -b ${CARTO_STYLE_TAG} --depth=1 git://github.com/gravitystorm/openstreetmap-carto.git

COPY renderd/prepare_style.py .
COPY ne_110m_admin_0_boundary_lines_land.zip openstreetmap-carto/data/ne_110m_admin_0_boundary_lines_land.zip
RUN cd openstreetmap-carto \
  && python3 /prepare_style.py -f project.mml \
  && carto project.mml > mapnik.xml \
  && ls data \
  && python3 scripts/get-shapefiles.py --no-download -u

COPY renderd/run.sh /
COPY renderd/renderd.conf ${RENDERD_CONF_PATH}
COPY renderd/requirements.txt /requirements.txt
COPY renderd/manage.py /manage.py

RUN pip3 install -r /requirements.txt

ENTRYPOINT bash /run.sh


FROM builder AS apache
RUN apt-get install -y apache2

COPY httpd/modules.conf/mod_tile.conf /etc/apache2/conf-available/mod_tile.conf
COPY httpd/mod_tile.conf /etc/mod_tile.conf
COPY httpd/000-tile-server.conf /etc/apache2/sites-available/000-tile-server.conf
COPY httpd/run.sh /run.sh

RUN a2dissite 000-default \
 && rm -f /etc/apache2/sites-available/000-default.conf \
 && a2enconf mod_tile \
 && a2ensite 000-tile-server

ENTRYPOINT bash /run.sh