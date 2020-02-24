ARG ELASTIC_VERSION

FROM docker.elastic.co/kibana/kibana:${ELASTIC_VERSION}

COPY config/kibana.yml /usr/share/kibana/config/kibana.yml

# Plugin Installation
COPY config/srirachaiq_jupyter-1.0.0.zip /usr/share/kibana/plugins/srirachaiq_jupyter.zip
RUN /usr/share/kibana/bin/kibana-plugin install file:///usr/share/kibana/plugins/srirachaiq_jupyter.zip \
	&& rm -rf /usr/share/kibana/plugins/srirachaiq_jupyter.zip