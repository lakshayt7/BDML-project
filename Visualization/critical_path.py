from flask import Flask
from prometheus_client import Counter, generate_latest, Gauge

app = Flask(__name__)

critical_path = Gauge('critical_path', 'Critical Path', ['service'])

@app.route('/inc/<id>')
def inc(id):
    critical_path.labels(service=id).inc()
    return "Inc %s\n" % id

@app.route('/dec/<id>')
def dec(id):
    critical_path.labels(service=id).dec()
    return "Dec %s\n" % id

@app.route('/metrics')
def metrics():
    return generate_latest()

app.run()
