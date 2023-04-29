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

    def set_parent(self, par):
        self.parent = par

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
    
    def set_prometheus_metrics(self, critical_path_metrics):
        critical_path_metrics.labels(
            service=self.serviceName, operation=self.operationName).set(
                self.end_time - self.start_time)

    def __str__(self):  
        return "span_id = " + self.id + " parent_id = " + self.parent_id + " start_time = " + str(self.start_time) + " end_time = "+str(self.end_time)+"duration = "+ str(self.end_time - self.start_time)

    def pprint(self):
        print("span_id = " + self.id)
        print("parent_id = " + self.parent_id)
        print("start_time = " + str(self.start_time))
        print("end_time = "+str(self.end_time))
        print("duration = "+ str(self.end_time - self.start_time))
        print("process id = " + self.pid)
        print("operationName = " + self.operationName)
        print("serviceName = " + self.serviceName)
        print("------------------------------------------------------------------------------------")