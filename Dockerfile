FROM ubuntu:16.04
MAINTAINER Ben Neely <nigelneely@gmail.com>

RUN apt-get update -y
RUN apt-get install -y \
    python3-pip \
    python3-dev

RUN apt-get install -y \
    build-essential \
    sqlite3 \
    libsqlite3-dev

RUN pip3 install --upgrade pip
ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt