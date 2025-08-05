FROM grafana/grafana

# Copy custom configuration
COPY grafana.ini /etc/grafana/grafana.ini
COPY dashboards/ /var/lib/grafana/dashboards/
COPY provisioning/ /etc/grafana/provisioning/

EXPOSE 3000

ENV GF_LOG_LEVEL=debug

CMD ["grafana-server", "web"]