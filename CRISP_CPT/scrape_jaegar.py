import json
import trace

class Scaper_jaegar:
    def __init__(self, fname):
        self.fname = fname
    
    def get_num(self, inp):
        s =  inp.split(":")[1].split(',')[0]
        return s.strip()

    def parse(self):
        f = open(self.fname, "r")
        inp = f.read()
        spans = inp.split('warnings')

        traces = []
        for span in spans:
            arr = span.split("\"")
            start_time, parent_id, span_id, end_time= None, "None", None, None
            ctr = 0
            for i in range(len(arr)):
                #print(arr[i])
                match arr[i]:
                    case "spanID":
                        if ctr == 0:
                            span_id = arr[i+2]
                            ctr+=1
                        else:
                            parent_id = arr[i+2]
                    case "startTime":
                        start_time = int(self.get_num(arr[i+1]))
                    case "duration":
                        end_time = start_time + int(self.get_num(arr[i+1]))
                    case _:
                        pass
            if span_id is not None and end_time is not None:
                traces.append(trace.Trace(start_time, end_time, span_id, parent_id))



        return traces

        

