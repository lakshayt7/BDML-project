import pandas as pd
import numpy as np
import random

import sys

df = pd.read_csv(sys.argv[-1])

try:
    numexample = int(sys.argv[-2])
except:
    numexample = 100

exs = []

while numexample > 0:
    numexample-=1
    ex =np.squeeze( df.sample().to_numpy().T)
    idxs = np.argwhere(ex!=-1)
    vals  = np.squeeze(np.array([ex[idx] for idx in idxs]))
    np.random.shuffle(vals)
    np.random.shuffle(idxs)
    vals = vals[int(0.25*len(vals)):]
    ex = np.array([-1 for i in range(len(ex))])
    for i in range(len(vals)):
        ex[int(idxs[i])] = vals[i] 
    exs.append(ex)

di = {}

call_paths = list(df.columns)

for i in range(len(call_paths)):
    di[i] = call_paths[i]

df_ex = pd.DataFrame(exs)

df_ex = df_ex.rename(columns = di)
df_ex.to_csv('anomaly_data.csv')


df_good = pd.read_csv('processed_data.csv')

df_good['label'] = 1
df_ex['label'] = 0

df_complete = pd.concat([df_good, df_ex])
df_final = df_complete.sample(frac=1, random_state=1).reset_index()
df_final = df_final.rename(columns = di)
df_final.to_csv('combined_data.csv')
