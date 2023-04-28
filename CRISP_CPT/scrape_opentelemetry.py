import json
import trace

class Scaper_opentelemetry:
    def __init__(self, fname):
        self.fname = fname
    
    def parse(self):
        f = open(self.fname, "r")
        inp = f.read()
        arr = inp.split("\"")

        traces = []
        span_ids, parent_ids, start_times, end_times = [], [], [], []
        for i in range(len(arr)):
            match arr[i]:
                case "span_id":
                    span_ids.append(arr[i+2])
                case "parent_id":
                    parent_ids.append(arr[i+2])
                case "start_time":
                    start_times.append(arr[i+2])
                case "end_time":
                    end_times.append(arr[i+2])
                case _:
                    pass
        for i in range(len(parent_ids)):
            if parent_ids[i] == 'start_time':
                parent_ids[i] = "None"
            traces.append(trace.Trace(start_times[i], end_times[i], span_ids[i], parent_ids[i]))

        return traces

        

