# %%
import pandas as pd
import numpy as np
import json

# Return the distinct normal vector of planes given by the coordinates from cifDic
def CoordinatesToPlanes(xyz):
    xyzList = []
    res = []
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
                vn = np.cross(v1,v2)
                res.append(vn)
    return res

def PlanesToProducts(Planes):
    num = len(Planes)
    unitPlanes = []
    dots = []
    for plane in Planes:
        unitPlanes.append(plane/np.linalg.norm(plane))
    for i in range(num-1):
        for j in range(i+1,num):
            dot = np.absolute(np.around(np.dot(unitPlanes[i],unitPlanes[j]),1))
            dots.append(dot)
    return dots

# %%
def resultForDots(cif):
    max_angle = 15
    cn_num = 6.0

    res = [cif]
    with open("./output/cifDic_0413.json") as json_file:
        cifDic = json.load(json_file) 
        if cif in cifDic:
            for site in cifDic[cif]['Sites']:
                if len(cifDic[cif]['Sites'][site]['Angles']) > max_angle: continue
                if float(cifDic[cif]['Sites'][site]['CN']) != 6.0: continue
                xyz = cifDic[cif]['Sites'][site]["Coordinates"]
                planes = CoordinatesToPlanes(xyz[1:])
                dots = PlanesToProducts(planes)
                res.extend([site,dots])

    with open("./output/Na_Y2020_cifDic.json") as json_file:
        cifDic = json.load(json_file)
        if cif in cifDic:
            for site in cifDic[cif]['Sites']:
                if len(cifDic[cif]['Sites'][site]['Angles']) > max_angle: continue
                if float(cifDic[cif]['Sites'][site]['CN']) != 6.0: continue
                xyz = cifDic[cif]['Sites'][site]["Coordinates"]
                planes = CoordinatesToPlanes(xyz[1:])
                dots = PlanesToProducts(planes)
                res.extend([site,dots])
    #print(res)
    return res
# %%
h_pl = ['250795.cif','258369.cif','67005.cif']
h_py = ['200026.cif','258376.cif','258378.cif','37304.cif']
Oct = ['164019.cif','186330.cif','186363.cif','187230.cif','237851.cif']
tri_p = ['150911.cif','151938.cif','153305.cif','196278.cif','405133.cif']
some = ['240263.cif','251666.cif','429556.cif']
# %%
import csv
dotResult=[]
dotResult.append(['Hexagonal Planae',h_pl])
dotResult.append(['Hexagonal Pyrimidal',h_py])
dotResult.append(['Otahedral',Oct])
dotResult.append(['Trigonal Prismatic',tri_p])
dotResult.append(['Others',some])


with open('.\output\dotResult_1.csv',mode='w') as dotfile:
    file_writer = csv.writer(dotfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for shape in dotResult:
        for cif in shape[1]:
            functionResults = resultForDots(cif)
            row = [shape[0]]
            row.append(functionResults[0])
            l = len(functionResults)
            for i in range(l//2):
                siteinfo = [functionResults[i*2+1],functionResults[i*2+2]]
                towrite = []
                towrite.append(row)
                towrite.extend(siteinfo)
                file_writer.writerow(towrite)

# %%
a = np.array([[1,2,3],[2,3,4]])
np.float32(a)
for i in range(2):
    a[i] = a[i]/np.linalg.norm(a[i])

# %%
