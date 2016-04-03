FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  software-properties-common && \
    apt-get update && \
    apt-get install -y python-pip python-dev libsqlite3-dev

RUN apt-get install -y -f git wget unzip 
RUN pip install pysqlite TwitterAPI influxdb
RUN pip install --upgrade requests

WORKDIR /
RUN git clone https://github.com/jpzk/twitter-growthhack.git 
WORKDIR /growtthhack
RUN mv docker/start.sh /
RUN chmod +x /start.sh

WORKDIR /
ENTRYPOINT ["/bin/bash", "/start.sh"]

