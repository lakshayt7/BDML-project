
Steps:

Python setup:
sudo pip install Flask
sudo pip install prometheus_client

python critical_path.py

This will start the application and by default, the flask application will be running on 5000 port.


Install and Start Prometheus:

Installation:
wget https://github.com/prometheus/prometheus/releases/download/v2.37.6/prometheus-2.37.6.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*

The Flask application will expose /metrics endpoint which Prometheus can scrape periodically to get metrics from the app. Below config can be added to Prometheus for this purpose.

- job_name: critical_path
    static_configs:
      - targets: ["localhost:5000"]


We can also configure alert rules in the prometheus config file.
rule_files:
  - "alert_rules.yaml"


Start Prometheus.
./prometheus --config.file=prometheus.yml


Install and Start Grafana:

sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/enterprise/release/grafana-enterprise_9.4.7_amd64.deb
sudo dpkg -i grafana-enterprise_9.4.7_amd64.deb

sudo systemctl daemon-reload
sudo systemctl start grafana-server

Once Grafana is started, it can be accessed on the 3000 port by default (http://localhost:3000). After that, we can set the datapoint to Prometheus and direct Grafana to pull data from Prometheus and dislay in its dashboard.

We can then import Critical path dashboard in Grafana.