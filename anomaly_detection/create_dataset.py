import Span
import parse_cpt

import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":
    fname = sys.argv[-1]
    spans = parse_cpt.parse_dir(fname)
    call_paths = []
    for span in spans:
        call_paths.extend(span['call path'].tolist())
    call_paths = list(set(call_paths))[1:]

    vals = []
    for span in spans:
        dic = {}
        for call_path in call_paths:
            dic[call_path] = -1
        cps = list(span['call path'])
        
        durations = list(span['inclusive_time'])
        for cp, dur in zip(cps, durations):
            dic[cp] = dur
        
        val = list(dic.values())
        vals.append(val)
    
    vals = np.array(vals)
    df = pd.DataFrame(vals)

    di = {}

    for i in range(len(call_paths)):
        di[i] = call_paths[i]

    df = df.rename(columns = di)
    df.to_csv('processed_data.csv', index = False)

  