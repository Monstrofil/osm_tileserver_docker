FROM ubuntu:20.04

RUN apt update
RUN apt install -y wget python3 netcat

RUN wget https://github.com/omniscale/imposm3/releases/download/v0.10.0/imposm-0.10.0-linux-x86-64.tar.gz
RUN tar xvf imposm-0.10.0-linux-x86-64.tar.gz

COPY manage.py /bin/manage

WORKDIR imposm-0.10.0-linux-x86-64