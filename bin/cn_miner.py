
import subprocess
import os
import glob
import numpy as np
import pandas as pd
import json
import time
from datetime import datetime

# Check the following addresses before running the script
FileNames = 'test/Na_Y2020/*.cif'
SaveAddress = '../output/Na_Y2020_cifDic.json'

print("Start time:", datetime.now())

cwd = os.getcwd()
cwd_exe =os.path.join(cwd,'softBV0405.exe')
all_files = glob.glob(os.path.join(cwd[:-4],FileNames))
file_num = len(all_files)

# Fuction to return database_unitary dataframe
def UnitaryDF():
    skipRow =[x for x in range(0,12)]+[13,14]+[x for x in range(206,217)]
    uni_df = pd.read_fwf("database_unitary.dat",skiprows=skipRow)
    return uni_df

# Fill unitary information to SiteDic
def fillUniInfo(SiteDic, uni_df):
    for site in SiteDic:
        period = uni_df[(uni_df['ty']== SiteDic[site]['Element']) & (uni_df['os']==int(SiteDic[site]['OS']))]['n'].tolist()
        if len(period) == 1:
            SiteDic[site]['Period'] = period[0]
        else:
            print("Element period is not found for",site,"!\n")
        group = uni_df[(uni_df['ty']== SiteDic[site]['Element']) & (uni_df['os']==int(SiteDic[site]['OS']))]['g'].tolist()
        if len(group) == 1:
            SiteDic[site]['Group'] = group[0]
        else:
            print("Element Group is not found for",site,"!\n")
    return SiteDic

def fillSitesFromStdout(stdout):    
    stdout_lines = stdout.split("\r\n")
    Sites = {}
    name = " "
    for line in stdout_lines:
        line = line.replace(" ",";").replace("=",";").split(";")
        line = ' '.join(line).split()
        if len(line)<2: continue
        if line[1] == 'name:':
            name = ' '.join(line[2:])
        if len(line)<9: continue
        if line[3] == "name":    
            if line[4] not in Sites:
                Sites[line[4]]= {}
                Sites[line[4]]['type'] = line[6]
                Sites[line[4]]['os'] = line[8]
            else:
                continue
    return Sites, name

def fillSiteDic(Sites,cwd_exe,cif):
    SiteDic = {}
    for site in Sites.keys():
        Coor = [[]]
        center = ""
        CalCNproc = subprocess.run([cwd_exe, "--cal-cn-bv", cif, site], cwd=cwd, capture_output=True)
        stdout = str(CalCNproc.stdout, "utf-8")
        stdout_lines = stdout.split("\r\n")
        for line in stdout_lines:
            line = line.split()
            if len(line) < 1: continue
            if line[1] == "Center":
                center = line[3]
            if line[1] == "XYZ:":
                Coor[0].append(center)
                Coor[0].append((float(line[3]),float(line[4]),float(line[5])))
            if line[1] == "Coordination":
                CN = float(line[3])
            if line[1] == "BVS:":
                SDofBV = float(line[6])
            if len(line) < 12: continue
            if line[5].isalpha(): continue
            if float(line[5]) <= CN:
                Coor.append([line[2]])
                Coor[-1].append((float(line[10]),float(line[11]),float(line[12])))
        if len(center) != 0: 
            SiteDic[center] = {}
            SiteDic[center]['CN'] = CN
            SiteDic[center]['SDofBV'] = SDofBV
            SiteDic[center]['Coordinates'] = Coor
            SiteDic[center]['Element'] = Sites[site]['type']
            SiteDic[center]['OS'] = Sites[site]['os']
        else: 
            print("Problematic cif:",cif,site)
    return SiteDic

def calAngleToSiteDic(SiteDic):
    for site in SiteDic:
        l = len(SiteDic[site]["Coordinates"])
        Angles = []
        for i in range(1,l-1):
            for j in range(i+1,l):
                Angles.append(calAngleDeg(SiteDic[site]["Coordinates"][0][1], SiteDic[site]["Coordinates"][i][1], SiteDic[site]["Coordinates"][j][1]))
        Angles.sort(reverse=True)
        SiteDic[site]["Angles"]= Angles
    return SiteDic

def calAngleCos(V0,V1,V2):
    V0 = np.asarray(V0)
    V1 = np.asarray(V1)
    V2 = np.asarray(V2)
    Va = V1 - V0   
    Vb = V2 - V0
    cos = np.dot(Va/np.linalg.norm(Va), Vb/np.linalg.norm(Vb))
    cos = round(cos, 4)
    cos = cos.tolist()
    return cos
# Calculate the angle radians
def calAngle(V0,V1,V2):
    V0 = np.asarray(V0)
    V1 = np.asarray(V1)
    V2 = np.asarray(V2)
    Va = V1 - V0   
    Vb = V2 - V0
    dot_product = round(np.dot(Va/np.linalg.norm(Va), Vb/np.linalg.norm(Vb)),4)
    angle = np.arccos(dot_product)
    angle = np.around(angle, 3)
    angle = angle.tolist()
    return angle

def calAngleDeg(V0,V1,V2):
    V0, V1, V2 = [np.asarray(i) for i in [V0,V1,V2]]
    Va = V1 - V0   
    Vb = V2 - V0
    dot_product = round(np.dot(Va/np.linalg.norm(Va), Vb/np.linalg.norm(Vb)),4)
    angle = np.arccos(dot_product)
    deg = np.rad2deg(angle)
    deg = np.around(deg,3)  
    deg = deg.tolist()
    return deg

# Load Unitary Database
uni_df = UnitaryDF()

# Main process to fill cifDic
cifDic = {}
for i,cif in enumerate(all_files):
    cif_name =cif.split("\\")[-1]
    print("Currently proccessing:", cif_name, " Status:", i, "/", file_num," Current Time:", datetime.now())
    cifDic[cif_name] = {}
    process = subprocess.run([cwd_exe, "--print-cell", cif], cwd=cwd, capture_output=True)
    stdout = str(process.stdout, "utf-8")
    Sites, name = fillSitesFromStdout(stdout)
    SiteDic = fillSiteDic(Sites,cwd_exe,cif)
    SiteDic = calAngleToSiteDic(SiteDic)
    SiteDic = fillUniInfo(SiteDic, uni_df)
    cifDic[cif_name]['Sites'] = SiteDic
    cifDic[cif_name]['Name'] = name
print("Processing Done!")

with open(SaveAddress, 'w') as fp:
    json.dump(cifDic,fp)

print("Saved to file:",SaveAddress)
    
