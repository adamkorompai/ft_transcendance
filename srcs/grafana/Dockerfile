FROM grafana/grafana-oss

COPY ./prometheus.yaml /etc/grafana/provisioning/datasources
COPY ./dashboards.yaml /conf/provisioning/dashboards
COPY ./dashboards.yaml /etc/grafana/provisioning/dashboards
COPY ./dashboards/mprofett_dashboard.json /etc/grafana/provisioning/dashboards
COPY ./defaults.ini /usr/share/grafana/conf