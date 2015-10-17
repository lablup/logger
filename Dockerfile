FROM ubuntu:14.04
MAINTAINER Joongi Kim "joongi@lablup.com"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get build-dep -y python3
RUN apt-get install -y curl git-core
RUN curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash 

RUN mkdir /logger
RUN git clone https://github.com/lablup/logger /logger
RUN chmod +x /logger/install.sh /logger/run.sh
RUN /logger/install.sh

# The config filename is "logger.conf" in the mounted volume.
VOLUME ['/logger/conf']

# Default ZMQ subscriber port.
EXPOSE 2120

ENTRYPOINT ['/logger/run.sh']
