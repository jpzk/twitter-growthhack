FROM ubuntu

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y  software-properties-common && \
    apt-get update && \
    apt-get install -y python-pip python-dev libsqlite3-dev

RUN apt-get install -y -f git wget unzip 
RUN pip install pysqlite TwitterAPI influxdb
RUN pip install --upgrade requests

RUN mkdir /root/.ssh/

# Copy over private key, and set permissions
ADD id_rsa /root/.ssh/id_rsa

# Create known_hosts
RUN touch /root/.ssh/known_hosts
# Add bitbuckets key
RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts

WORKDIR /
RUN git clone git@bitbucket.org:jpzk/growthhack.git
WORKDIR /growthhack
RUN mv docker/start.sh /
RUN chmod +x /start.sh

WORKDIR /
ENTRYPOINT ["/bin/bash", "/start.sh"]

