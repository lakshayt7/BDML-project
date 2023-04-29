class Graph:

    def __init__(self, id2trace, traces, roots):
        self.id2trace = id2trace
        self.traces = traces
        self.roots = roots
        for trace in self.traces:
            trace.sort_children()
        self.pth = []

    def cpt_call(self, trace):
        #print('cpt_call for trace ')
        #print(trace)
        #print('children of trace')
        #trace.print_children()
        self.pth.append(trace)
        idx = len(trace.children) - 1
        #trace.print_children()
        while idx >= 0:
            self.cpt_call(trace.children[idx])
            tmr = trace.children[idx].start_time
            while idx >=0 and trace.children[idx].end_time >= tmr:
                idx-=1

    def cpt(self):
        for root in self.roots:
            self.cpt_call(root)
    
    def set_prometheus_metrics(self, critical_path_metrics):
        rev = self.pth#self.pth.reverse()
        for i, t in enumerate(rev):
            t.set_prometheus_metrics(critical_path_metrics)

    def print_cpt(self):
        rev = self.pth#self.pth.reverse()
        for i, t in enumerate(rev):
            print(f"span = {i}")
            t.pprint()

    