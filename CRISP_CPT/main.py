import sys
from flask import Flask
from prometheus_client import generate_latest, Gauge

from trace import *
from scrape_jaegar import *
from scrape_opentelemetry import *
from graph import *

app = Flask(__name__)

critical_path_metrics = Gauge('critical_path', 'Critical Path', ['service', 'operation', 'trace_id'])

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == "__main__":
    fname = sys.argv[2] 
    match sys.argv[1]:
        case "o":
            scraper = Scaper_opentelemetry(fname)
        case "j":
            scraper = Scaper_jaegar(fname)

    traces = scraper.parse()

    '''
    for trace in traces:
        print(trace)
    '''

    id2trace = {}

    for trace in traces:
        id2trace[trace.id] = trace

    roots = []

    for trace in traces:
        if trace.parent_id != 'None':
            par = id2trace[trace.parent_id]
            trace.set_parent(par)
            par.add_child(trace)

        else:
            trace.set_parent(None)
            roots.append(trace)

    graph = Graph(id2trace, traces, roots)
    graph.cpt()
    graph.set_prometheus_metrics(critical_path_metrics)
    graph.print_cpt()

    app.run()