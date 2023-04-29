class Span:
    def __init__(self, pos, id, par_id, inclusive_time, exclusive_time, pid, operationName, serviceName):
        self.pos = pos
        self.id = id
        self.par_id = par_id
        self.inclusive_time = inclusive_time
        self.exclusive_time = exclusive_time
        self.pid = pid
        self.operationName = operationName
        self.serviceName = serviceName