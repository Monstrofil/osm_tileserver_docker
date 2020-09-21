FROM ubuntu:20.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

RUN apt update
RUN apt install npm nodejs -y

RUN mkdir /application
WORKDIR /application


RUN npm install @angular/cli

COPY app/package-lock.json .
COPY app/package.json .

RUN npm i
COPY app/ ./

RUN ls -la

RUN npm run-script ng version
RUN npm run-script build --production

FROM nginx:latest AS nginx
COPY --from=builder /application/dist/web/ /usr/share/nginx/html
