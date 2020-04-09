ARG ELASTIC_VERSION

FROM docker.elastic.co/logstash/logstash:${ELASTIC_VERSION}

COPY --chown=logstash config/logstash.yml /usr/share/logstash/config/logstash.yml
COPY --chown=logstash config/pipelines.yml /usr/share/logstash/config/pipelines.yml
COPY --chown=logstash pipeline /usr/share/logstash/pipeline