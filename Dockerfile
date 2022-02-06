FROM amazonlinux:2

EXPOSE 1935

ENV NGINX_CONFIG_DIRECTORY="/usr/local/nginx/conf/conf.d/"

RUN yum update -y && yum install git tar wget python3 -y

WORKDIR /setup
COPY config/scripts .
RUN ./setup_nginx.sh

RUN mkdir -p /usr/local/nginx/conf/conf.d
COPY config/nginx.conf /usr/local/nginx/conf/nginx.conf

COPY / .
RUN python3 setup.py sdist && pip3 install dist/multistream-*.tar.gz

CMD [ "multistream" ]