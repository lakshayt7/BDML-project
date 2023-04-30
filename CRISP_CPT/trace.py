import helper

class Trace:
    def __init__(self, start_time, end_time, id, parent_id):
        open = False
        if open:
            self.start_time = helper.parse_time(start_time)
            self.end_time = helper.parse_time(end_time)
        else:
            self.start_time = start_time
            self.end_time = end_time
        self.id = id
        self.parent_id = parent_id
        self.parent = None
        self.children = []
        self.pid = "None"
        self.operationName = "None"
        self.serviceName = "None"
        self.traceID = "None"
        self.call_path = ""
        
    def set_call_path(self, path):
        self.call_path = path

    def set_parent(self, par):
        self.parent = par

    def set_traceID(self, id):
        self.traceID = id

    def set_processID(self, pid):
        self.pid = pid
    
    def set_operationName(self, operationName):
        self.operationName = operationName

    def set_serviceName(self, serviceName):
        self.serviceName = serviceName

    def add_child(self, child):
        self.children.append(child)

    def sort_children(self):
        self.children.sort(key=lambda x: x.end_time)

    def print_children(self):
        for u in self.children:
            print(u)
    
    def get_exclusive_time(self):
        exclusive_time = self.end_time - self.start_time
        ed = self.end_time

        if len(self.children) > 0:
            for child in reversed(self.children):
                #print(f"{child.start_time} {child.end_time} {child.end_time - child.start_time}")
                exclusive_time -= max(min(child.end_time,ed) - max(child.start_time, self.start_time), 0)
                ed = min(ed, child.start_time)
        
        return exclusive_time
    
    def set_prometheus_metrics(self, critical_path_metrics):
        critical_path_metrics.labels(
            service=self.serviceName, operation=self.operationName).inc(
                self.get_exclusive_time())

    def __str__(self):  
        return "span_id = " + self.id + " parent_id = " + self.parent_id + " start_time = " + str(self.start_time) + " end_time = "+str(self.end_time)+"duration = "+ str(self.end_time - self.start_time)

    def pprint(self):
        print("trace_id = " + self.traceID)
        print("span_id = " + self.id)
        print("parent_id = " + self.parent_id)
        print("start_time = " + str(self.start_time))
        print("end_time = "+str(self.end_time))
        print("inclusive_time = "+ str(self.end_time - self.start_time))
        print("exclusive_time = "+ str(self.get_exclusive_time()))
        print("process_id = " + self.pid)
        print("operationName = " + self.operationName)
        print("serviceName = " + self.serviceName)
        print("call path = " + self.call_path)
        print("------------------------------------------------------------------------------------")