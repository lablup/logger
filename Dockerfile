FROM ubuntu:14.04
MAINTAINER Joongi Kim "joongi@lablup.com"

ENV HOME /logger
ENV DEBIAN_FRONTEND noninteractive

RUN mkdir /logger
WORKDIR /logger
RUN apt-get update && apt-get build-dep -y python3
RUN apt-get install -y git-core wget libbz2-dev libssl-dev libreadline-dev libsqlite3-dev libzmq3-dev
RUN git clone https://github.com/yyuu/pyenv /logger/.pyenv

ADD install-python.sh /logger/install-python.sh
RUN chmod +x /logger/install-python.sh
RUN /logger/install-python.sh

ADD install.sh /logger/install.sh
RUN chmod +x /logger/install.sh

ADD dist/logger-0.1.0-py3-none-any.whl /logger/logger-0.1.0-py3-none-any.whl
RUN /logger/install.sh

ADD run.sh /logger/run.sh
RUN chmod +x /logger/run.sh

# The config filename is "logger.conf" in the mounted volume.
VOLUME ["/logger/conf"]

# Default ZMQ subscriber port.
EXPOSE 2120

CMD /logger/run.sh
