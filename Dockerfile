FROM python:3
MAINTAINER Ben Neely <nigelneely@gmail.com>
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y nginx
ADD nginx_conf /etc/nginx
ADD .aws/ /root/.aws
WORKDIR /ihc-image-analysis
CMD ["./start_docker.sh"]
