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
ADD . /ihc-image-analysis
RUN pip3 install -r /ihc-image-analysis/requirements.txt
RUN python3 /ihc-image-analysis/manage.py makemigrations analytics
RUN python3 /ihc-image-analysis/manage.py migrate
CMD ["python3", "/ihc-image-analysis/manage.py", "runserver", "0.0.0.0:8000"]
