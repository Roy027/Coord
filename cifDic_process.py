#  python script to read cifDic to pandas
# %%
import pandas as pd
import numpy as np
import json

# Return the distinct normal vector of planes given by the coordinates from cifDic
def CoordinatesToPlanes(xyz):
    xyzList = []
    res = set()
    for i in xyz:
        xyzList.append(i[1])
    num = len(xyzList)
    for i in range(num-2):
        for j in range(i+1,num-1):
            for k in range(j+1,num):
                p1 = np.array(xyzList[i])
                p2 = np.array(xyzList[j])
                p3 = np.array(xyzList[k])
                v1 = p3 - p1
                v2 = p2 - p1
                vn = np.around(np.cross(v1,v2),2)
                res.add(tuple(vn))
    return res
# %%
max_angle = 15
cn_num = 6.0

Angle_table = []
with open("./output/cifDic_0413.json") as json_file:
    cifDic = json.load(json_file)
    for cif in cifDic:
        for site in cifDic[cif]['Sites']:
            if ('Period' or 'Group') not in cifDic[cif]['Sites'][site]: continue
            if len(cifDic[cif]['Sites'][site]['Angles']) > max_angle: continue
            xyz = cifDic[cif]['Sites'][site]["Coordinates"]
            planes = CoordinatesToPlanes(xyz[1:])
            Angle_list = (cif,cifDic[cif]['Name'], site, float(cifDic[cif]['Sites'][site]['CN']),\
                          float(cifDic[cif]['Sites'][site]['OS']),\
                          cifDic[cif]['Sites'][site]['Period'], cifDic[cif]['Sites'][site]['Group'], \
                          cifDic[cif]['Sites'][site]['SDofBV'], \
                          cifDic[cif]['Sites'][site]['Angles'], planes)
            Angle_table.append(Angle_list)

headers = ['Cif','Name','Site','CN','OS', 'Period', 'Group','SDofBV','Angles','Planes']
df = pd.DataFrame.from_records(Angle_table,columns=headers)

CN6_df = df[df['CN']==cn_num]
Angles = CN6_df['Angles'].tolist()


Angle_table1 = []
with open("./output/Na_Y2020_cifDic.json") as json_file:
    cifDic = json.load(json_file)
    for cif in cifDic:
        for site in cifDic[cif]['Sites']:
            if ('Period' or 'Group') not in cifDic[cif]['Sites'][site]: continue
            if len(cifDic[cif]['Sites'][site]['Angles']) > max_angle: continue
            xyz = cifDic[cif]['Sites'][site]["Coordinates"]
            planes = CoordinatesToPlanes(xyz[1:])
            Angle_list = (cif,cifDic[cif]['Name'], site, float(cifDic[cif]['Sites'][site]['CN']),\
                          float(cifDic[cif]['Sites'][site]['OS']),\
                          cifDic[cif]['Sites'][site]['Period'], cifDic[cif]['Sites'][site]['Group'], \
                          cifDic[cif]['Sites'][site]['SDofBV'], \
                          cifDic[cif]['Sites'][site]['Angles'], planes )
            Angle_table1.append(Angle_list)
headers = ['Cif','Name','Site','CN','OS', 'Period', 'Group','SDofBV','Angles', 'Planes']
df1 = pd.DataFrame.from_records(Angle_table1,columns=headers)

CN6_df1 = df1[df1['CN']==cn_num]
Angles1 = CN6_df1['Angles'].tolist()

# %%
df_all = [CN6_df,CN6_df1]
concatT = pd.concat(df_all).reset_index(drop=True)
d_index = concatT.astype(str).drop_duplicates().index
result = concatT.loc[d_index]
result_cation = result[result.OS > 0]
# %%
#result_cation['Angles'].to_csv("./output/CN6_Angles_all_cat_12492.csv")
result_cation.to_csv(".\output\CN6_table_all_cat_12613_Planes.csv")
# %%
with open("./output/Na_Y2020_cifDic.json") as json_file:
    cifDic = json.load(json_file)
    for cif in cifDic:
        for site in cifDic[cif]['Sites']:
            if ('Period' or 'Group') not in cifDic[cif]['Sites'][site]:
                print(cif,site)
# %%
# Testing 
with open("./output/cifDic_0413.json") as json_file:
    cifDic = json.load(json_file)
    for cif in cifDic:
        for site in cifDic[cif]['Sites']:
            if cifDic[cif]['Sites'][site]['CN'] != 6: continue
            if len(cifDic[cif]['Sites'][site]['Angles']) != 15: continue
            xyz = cifDic[cif]['Sites'][site]["Coordinates"]
            break
        break
print(xyz)
# %%


planes = CoordinatesToPlanes(xyz[1:])

    
# %%
