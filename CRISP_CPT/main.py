import sys

from trace import *
from scrape import *
from graph import *

if __name__ == "__main__":
    fname = sys.argv[1]
    
    scraper = Scaper(fname)
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
    graph.print_cpt()
