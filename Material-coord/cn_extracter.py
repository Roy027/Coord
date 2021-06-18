#%%
import subprocess
import os
from pathlib import Path
import glob
import numpy as np
import pandas as pd
import json
import time

JsonDir = os.path.abspath(os.path.join('..','test/json'))
jsonFile = []
for (r,d,f) in os.walk(JsonDir):
    for fi in f:
        if r.endswith(('A2BX4','ABX4','ABX3')):
            jsonFile.append(os.path.join(r,fi))
# %%
jsonDic = {}
for i,js in enumerate(jsonFile):
    fileName = js.split('\\')[-1][:-5]
    with open(js) as j:
        data = json.load(j)
        siteSet = set()
        for site in data['sites']:
            siteSet.add((site['label'],sum([x[1] for x in site['properties']['coordination'].items()])))
            #print(sum([x[1] for x in site['properties']['coordination'].items()]))
            #print(site['label'])
            #print(site['properties']['coordination'])
        jsonDic[fileName] = siteSet
        
jsondf = pd.DataFrame(list(jsonDic.items()),columns=['File','Material-Coord Standard'])
# %%
