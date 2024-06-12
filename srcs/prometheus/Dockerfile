FROM prom/prometheus

COPY ./prometheus.yml /etc/prometheus
COPY ./alert_rules.yml /etc/prometheus
COPY ./launch.sh /usr/local/bin/launch.sh

USER root

RUN chmod +x /usr/local/bin/launch.sh

EXPOSE 9090

ENTRYPOINT [ "/usr/local/bin/launch.sh" ]