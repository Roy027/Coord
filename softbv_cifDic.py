#  python script to read cifDic to pandas
# %%
import pandas as pd
import numpy as np
import json

# %%
Angle_table = []
with open("./test/cifDic_0412.json") as json_file:
    cifDic = json.load(json_file)
    for cif in cifDic:
        for site in cifDic[cif]['Sites']:
            if len(cifDic[cif]['Sites'][site]['Angles']) > 6: continue
            Angle_list = (cif,cifDic[cif]['Name'], site, float(cifDic[cif]['Sites'][site]['CN']),\
                          cifDic[cif]['Sites'][site]['OS'],\
                          cifDic[cif]['Sites'][site]['Period'], cifDic[cif]['Sites'][site]['Group'], \
                          cifDic[cif]['Sites'][site]['Angles'])
            Angle_table.append(Angle_list)

            

headers = ['Cif','Name','Site','CN','OS', 'Period', 'Group', 'Angles']
df = pd.DataFrame.from_records(Angle_table,columns=headers)
# %%

CN4_df = df[df['CN']==4]
Angles = CN4_df['Angles'].tolist()

# %%

# %%


# %%
data = np.array([np.array(x,dtype=float) for x in Angles])
import scipy.io
scipy.io.savemat("Angles.mat",{'X':data})
# %%
angle_df = pd.DataFrame(data)
angle_df.to_csv("Angles.csv")
# %%
CN4_df['Angles'].to_csv("Angles.csv")
# %%
CN4_df.to_csv("CN4_Angles.csv")
# %%
