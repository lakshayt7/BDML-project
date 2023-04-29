import pandas as pd
import os

def parse(inp):
    sps = inp.split("----------")
    spans = []
    for sp in sps:
        det = sp.split('\n')
        span = {}
        pd.DataFrame()
        if len(det) > 2:
            for l in det:
                if len(l) > 0 and l[0] != '-':
                    key, value = l.split('=')
                    key = key[:-1]
                    value = value[1:]
                    span[key] = value
                
            spans.append(span)
    df = pd.DataFrame(spans)
    return df

def parse_dir(inp_dir):
    files = os.listdir(inp_dir)
    dfs = []
    for file in files:
        file = inp_dir + file
        inp = open(file).read()
        df = parse(inp)
        dfs.append(df)
    return dfs