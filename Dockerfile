FROM python:3.8.2-buster

RUN apt-get update

COPY . /app 
WORKDIR /app

RUN make env

ENV IS_CI=true
