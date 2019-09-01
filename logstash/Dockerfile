ARG ELK_VERSION

FROM docker.elastic.co/logstash/logstash:${ELK_VERSION}

# Switch to privleged user for installing packages
USER root

# Install EPEL repository for python
RUN yum install -y epel-release

# Install python for usage by logstash modules
RUN yum install -y \
 python36 \
 python36-pip \
 && yum clean all

# Install python packages required by logstash modules
COPY requirements.txt /tmp/requirements.txt
RUN pip3.6 install -r /tmp/requirements.txt

# Copy in helper scripts
COPY scripts/ /usr/share/logstash/scripts
 
# Switch back to non-priveleged user for normal operations
#USER logstash