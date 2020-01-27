FROM centos:7

WORKDIR /app

COPY scripts scripts/
COPY extras extras/

RUN chmod +x scripts -R
RUN chmod +x extras -R

ENTRYPOINT ["/app/scripts/setup-kibana.sh"]