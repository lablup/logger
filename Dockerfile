FROM ubuntu:14.04
MAINTAINER Joongi Kim "joongi@lablup.com"

ENV HOME /logger
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /logger
WORKDIR /logger
RUN apt-get update && apt-get build-dep -y python3
RUN apt-get install -y git-core wget libbz2-dev libssl-dev libreadline-dev libsqlite3-dev libzmq-dev
RUN git clone https://github.com/lablup/logger /logger
RUN git clone https://github.com/yyuu/pyenv /logger/.pyenv
RUN chmod +x /logger/*.sh
RUN /logger/install-python.sh
RUN /logger/install.sh

# The config filename is "logger.conf" in the mounted volume.
VOLUME ["/logger/conf"]

# Default ZMQ subscriber port.
EXPOSE 2120

CMD /logger/run.sh
