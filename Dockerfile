FROM python:3
MAINTAINER Ben Neely <nigelneely@gmail.com>
ADD requirements.txt /requirements.txt
WORKDIR /
RUN pip install -r requirements.txt