FROM ubuntu:20.04

RUN apt update
RUN apt install -y netcat

COPY tegola /opt/tegola
RUN chmod +x /opt/tegola
WORKDIR /opt
ENTRYPOINT ["/opt/tegola"]