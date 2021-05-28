# Adapted from Roy Dai's code in GitHub

# %%
import pandas as pd
import numpy as np
import json
from math import sqrt
from math import comb
from math import floor

COORDno = 6.0

# Custom decimal floor function found online (since python does not have such function)
# Returns a value rounded down to a specific number of decimal places.
def round_decimals_down(number:float, decimals:int=2):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return floor(number)

    factor = 10 ** decimals
    return floor(number * factor) / factor

# Return the distinct normal vector of planes given by the coordinates from cifDic
def CoordinatesToPlanes(xyz):
    xyzList = []
    res = []
    for i in xyz:
        xyzList.append(i[1])
    num = len(xyzList)
    for j in range(1,num):
        for k in range(j+1,num):
            p1 = np.array(xyzList[0])
            p2 = np.array(xyzList[j])
            p3 = np.array(xyzList[k])
            v1 = p3 - p1
            v2 = p2 - p1
            # Normalised vectors into unit length
            n_v1 = v1 / sqrt(v1[0]**2 + v1[1]**2 + v1[2]**2)
            n_v2 = v2 / sqrt(v2[0]**2 + v2[1]**2 + v2[2]**2)
            vn = np.cross(n_v1,n_v2)
            # print(sqrt(vn[0]**2 + vn[1]**2 + vn[2]**2))
            # Check if cross product yields value x or higher.
            # If the product yields lower than x means it's not a plane.
            # Currently it's sin(175deg)=0.08715574274
            if sqrt(vn[0]**2 + vn[1]**2 + vn[2]**2) >= 0.08715574274 :
                res.append(vn)
            # else:
            #     print("OUT!")
    return res

def PlanesToProducts(Planes):
    num = len(Planes)
    unitPlanes = []
    dots = []
    for plane in Planes:
        unitPlanes.append(plane/np.linalg.norm(plane))
    for i in range(num-1):
        for j in range(i+1,num):
            # note : np.absolute(round_decimals_down(np.dot(unitPlanes[i],unitPlanes[j]),1))
            # actually gives a more irregular interval than the one below.
            # This is because of how "floor" treats negative values
            # It rounds the value to the LOWER value, which when turned into absolute value, gives disproportional results.
            # Ok I don't really know how to explain this well.
            dot = round_decimals_down(np.absolute(np.dot(unitPlanes[i],unitPlanes[j])),1)
            dots.append(dot)
    return dots

# %%
def resultForDots(cif):
    cn_num = COORDno
    max_angle = comb(int(cn_num),2)
    max_plane = comb(max_angle,2)

    res = [cif]
    with open("./cifDic_0413.json") as json_file:
        cifDic = json.load(json_file)
        if cif in cifDic:
            for site in cifDic[cif]['Sites']:
                if len(cifDic[cif]['Sites'][site]['Angles']) > max_angle: continue
                if float(cifDic[cif]['Sites'][site]['CN']) != cn_num: continue
                xyz = cifDic[cif]['Sites'][site]["Coordinates"]
                angles = cifDic[cif]['Sites'][site]["Angles"]
                SDofBV = cifDic[cif]['Sites'][site]["SDofBV"]
                CooN = cifDic[cif]['Sites'][site]['CN']
                OxS = 9999
                Period = 9999
                Group = 9999
                # Had to be done this way because there are some .cif files with missing details...
                # ...causing this program to raise an error.
                if 'OS' in cifDic[cif]['Sites'][site].keys():
                    OxS = cifDic[cif]['Sites'][site]['OS']
                if 'Period' in cifDic[cif]['Sites'][site].keys():
                    Period = cifDic[cif]['Sites'][site]['Period']
                if 'Group' in cifDic[cif]['Sites'][site].keys():
                    Group = cifDic[cif]['Sites'][site]['Group']
                planes = CoordinatesToPlanes(xyz)
                dots = PlanesToProducts(planes)
                # Fill in the rest of the blanks as -1 if dot product is unavailable
                # Due to a lack of planes.
                if len(dots) != max_plane:
                    for i in range(max_plane - len(dots)):
                        dots.append(-1)
                res.extend([site,CooN,OxS,Period,Group,SDofBV,angles,dots])

    with open("./Na_Y2020_cifDic.json") as json_file:
        cifDic = json.load(json_file)
        if cif in cifDic:
            for site in cifDic[cif]['Sites']:
                if len(cifDic[cif]['Sites'][site]['Angles']) > max_angle: continue
                if float(cifDic[cif]['Sites'][site]['CN']) != cn_num: continue
                xyz = cifDic[cif]['Sites'][site]["Coordinates"]
                angles = cifDic[cif]['Sites'][site]["Angles"]
                SDofBV = cifDic[cif]['Sites'][site]["SDofBV"]
                CooN = cifDic[cif]['Sites'][site]['CN']
                OxS = 9999
                Period = 9999
                Group = 9999
                # Had to be done this way because there are some .cif files with missing details...
                # ...causing this program to raise an error.
                if 'OS' in cifDic[cif]['Sites'][site].keys():
                    OxS = cifDic[cif]['Sites'][site]['OS']
                if 'Period' in cifDic[cif]['Sites'][site].keys():
                    Period = cifDic[cif]['Sites'][site]['Period']
                if 'Group' in cifDic[cif]['Sites'][site].keys():
                    Group = cifDic[cif]['Sites'][site]['Group']
                planes = CoordinatesToPlanes(xyz)
                dots = PlanesToProducts(planes)
                # Fill in the rest of the blanks as -1 if dot product is unavailable
                # Due to a lack of planes.
                if len(dots) != max_plane:
                    for i in range(max_plane - len(dots)):
                        dots.append(-1)
                res.extend([site,CooN,OxS,Period,Group,SDofBV,angles,dots])
    
    return res
# %%
import csv

# Get a list of all the .cif files with the correct CN
dotResult=[]
with open("./cifDic_0413.json") as json_file:
    cifDic = json.load(json_file)
    for cif in cifDic:
        for site in cifDic[cif]['Sites']:
            if float(cifDic[cif]['Sites'][site]['CN']) != COORDno: continue
            dotResult.append(cif)

with open("./Na_Y2020_cifDic.json") as json_file:
    cifDic = json.load(json_file)
    for cif in cifDic:
        for site in cifDic[cif]['Sites']:
            if float(cifDic[cif]['Sites'][site]['CN']) != COORDno: continue
            dotResult.append(cif)

# Convert to and fro dictionary and list to remove duplicate entries
theList = list(dict.fromkeys(dotResult))

# Writing data into csv file.
# "towrite" variable contains the information to be written into csv file
# The variable contains "row" and "siteinfo"
# "row" contains .cif file name kind of like the label of the row
# "siteinfo" contains the site name as well as its dot products
with open('.\CN6_cifdata.csv',mode='w') as dotfile:
    file_writer = csv.writer(dotfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for cif in theList:
        functionResults = resultForDots(cif)
        # Put in .cif file name
        row = [cif]
        l = len(functionResults)
        # The "8" displays how many parameters to be added into the .csv file per site
        # the number of parameters can be found in resultForDots function
        for i in range(l//8):
            siteinfo = [functionResults[i*8+1],functionResults[i*8+2],functionResults[i*8+3],functionResults[i*8+4],functionResults[i*8+5],functionResults[i*8+6],functionResults[i*8+7],functionResults[i*8+8]]
            towrite = []
            towrite.append(row)
            towrite.extend(siteinfo)
            file_writer.writerow(towrite)
            print(towrite)
            towrite = None

# %%
# a = np.array([[1,2,3],[2,3,4]])
# np.float32(a)   
# for i in range(2):
#     a[i] = a[i]/np.linalg.norm(a[i])

# %%
