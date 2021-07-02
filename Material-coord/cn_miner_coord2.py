#%%
# This script is to get all the site for comparison for analysis of s_det
import subprocess
import os
from pathlib import Path
import glob
import numpy as np
import pandas as pd
import json
import time
from datetime import datetime

# Check the following addresses before running the script
FileDir = os.path.abspath(os.path.join('..','test/coord_cif/Ternary'))
GroupDir = [folder for folder in os.scandir(FileDir) if folder.is_dir()]
cifFile = []
for (r,d,f) in os.walk(FileDir):
    for fi in f:
        if fi.endswith('.cif'):
            cifFile.append(os.path.join(r,fi))
SaveAddress = './cifresults.csv'

print("Start time:", datetime.now())

cwd = os.path.abspath("../bin")
cwd_exe =os.path.join(cwd,'softBV_cn425.exe')

file_num = len(cifFile)

# Fuction to return database_unitary dataframe
def UnitaryDF():
    skipRow =[x for x in range(0,12)]+[13,14]+[x for x in range(206,217)]
    uni_df = pd.read_fwf("../bin/database_unitary.dat",skiprows=skipRow)
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

def fillSiteLists(Sites,cwd_exe,cif):
    SiteLists = []
    for site in Sites.keys():
        Coor = [[]]
        ionType, r, occ, n, s, BVS, s_ave, s_det = [], [], [], [], [], [], [], []
        center = ""
        CalCNproc = subprocess.run([cwd_exe, "--cal-cn-bv", cif, site], cwd=cwd, capture_output=True)
        #CalCNproc = subprocess.run([cwd_exe, "--cal-cn-bv", cif, site], cwd=cwd, stdout=subprocess.PIPE)
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
            ionType.append(line[2])
            r.append(float(line[3]))
            occ.append(float(line[4]))
            n.append(float(line[5]))
            s.append(float(line[6]))
            BVS.append(float(line[7]))
            s_ave.append(float(line[8]))
            s_det.append(float(line[9]))
        if len(center) != 0: 
            #SiteDic[center] = CN
            #SiteDic[center]['CN'] = CN
            #SiteDic[center]['SDofBV'] = SDofBV
            #SiteDic[center]['Coordinates'] = Coor
            #SiteDic[center]['Element'] = Sites[site]['type']
            #SiteDic[center]['OS'] = Sites[site]['os']
            row = [center, Sites[site]['type'], Sites[site]['os'], CN, ionType, r, occ, n, s, BVS, s_ave, s_det]
            SiteLists.append(row)
        else: 
            print("Problematic cif:",cif,site)
    return SiteLists

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

def appendSiteLists(SiteTable, SiteLists, cif_name):
    for sitelist in SiteLists:
        row = [cif_name]
        row.extend(sitelist)
        SiteTable.append(row)
    return SiteTable 

# Load Unitary Database
uni_df = UnitaryDF()

# Main process to fill SiteList
SiteTable = []
for i,cif in enumerate(cifFile):
    cif_name =cif.split("\\")[-1][:-4]
    print("Currently proccessing:", cif_name, " Status:", i, "/", file_num," Current Time:", datetime.now())
    process = subprocess.run([cwd_exe, "--print-cell", cif], cwd=cwd, capture_output=True)
    #process = subprocess.run([cwd_exe, "--print-cell", cif], cwd=cwd,stdout=subprocess.PIPE)
    stdout = str(process.stdout, "utf-8")
    Sites, name = fillSitesFromStdout(stdout)
    SiteLists = fillSiteLists(Sites,cwd_exe,cif)
    #SiteDic = calAngleToSiteDic(SiteDic)
    #SiteDic = fillUniInfo(SiteDic, uni_df)
    #SiteList[cif_name]['Sites'] = SiteDic
    #SiteList[cif_name]['Name'] = name
    SiteTable = appendSiteLists(SiteTable,SiteLists,cif_name)
print("Processing Done!")

df1 = pd.DataFrame(SiteTable,columns=['File','Site','Type','OS','Coordination','ionType','r','occ','n','s','BVS','s_ave','s_det'],dtype=float)
#%%
dfcn4 = df1[df1['Coordination']==4]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,12))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.set_xlim(0,9)
ax2.set_xlim(0,9)
ax1.plot([0, 12], [4.5, 4.5], color='red')
ax2.plot([0, 12], [4.5, 4.5], color='red')

for index, row in dfcn4.iterrows(): 
    if index < 60:
        ax1.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'])
        ax1.legend(loc='right',bbox_to_anchor=(1.6,0.5))
    else:
        ax2.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'])
        ax2.legend(loc='right',bbox_to_anchor=(1.6,0.5))
#plt.legend(loc='right',bbox_to_anchor=(1.6,0.5));
plt.show()

# %%
dfcn6 = df1[df1['Coordination']==6]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,12))
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
ax1.set_xlim(0,11)
ax2.set_xlim(0,11)
ax1.plot([0, 12], [4.5, 4.5], color='red')
ax2.plot([0, 12], [4.5, 4.5], color='red')

for index, row in dfcn6.iterrows(): 
    if index < 55:
        ax1.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'])
        ax1.legend(loc='right',bbox_to_anchor=(1.6,0.5))
    else:
        ax2.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'])
        ax2.legend(loc='right',bbox_to_anchor=(1.6,0.5))

plt.show()

# %%
dfcn6 = df1[(df1['Coordination']==6) & (df1['OS']>0)]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,8.5))
ax1 = fig.add_subplot(111)
ax1.xaxis.set_tick_params(labelsize=20)
ax1.yaxis.set_tick_params(labelsize=20)
ax1.set_xlim(0,12)

ax1.plot([0, 12], [4.5, 4.5], color='red',lw=5)


for index, row in dfcn6.iterrows(): 
    ax1.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'],linewidths=5)
    ax1.legend(loc='right',bbox_to_anchor=(1.6,0.5))
    

plt.show()
# %%
dfcn4 = df1[(df1['Coordination']==4) & (df1['OS']>0)]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,8.5))
ax1 = fig.add_subplot(111)
ax1.xaxis.set_tick_params(labelsize=20)
ax1.yaxis.set_tick_params(labelsize=20)
ax1.set_xlim(0,11)

ax1.plot([0, 12], [4.5, 4.5], color='red',lw=5)


for index, row in dfcn4.iterrows(): 
    ax1.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'],linewidths=5)
    ax1.legend(loc='right',bbox_to_anchor=(1.6,0.5))
    

plt.show()

# %%
#'Coordination'==5
dfcn = df1[df1['Coordination']==5]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,8.5))
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Coodinating ions ranked by bond valence', fontsize=20)
ax1.set_ylabel('Bond Valence Determinant(s_det)', fontsize=20)
ax1.xaxis.set_tick_params(labelsize=20)
ax1.yaxis.set_tick_params(labelsize=20)
ax1.set_xlim(0,11)

ax1.plot([0, 12], [4.5, 4.5], color='red',lw=5)

for index, row in dfcn.iterrows(): 
    ax1.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'],linewidths=5)
    ax1.legend(loc='right',bbox_to_anchor=(1.6,0.5))

#plt.title("Bond Valence Determinant plot for sites with coordination number 5",fontsize=20)
plt.show()
# %%
dfcn = df1[df1['Coordination']==3]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,8.5))
ax1 = fig.add_subplot(111)
ax1.set_xlabel('Coodinating ions ranked by bond valence', fontsize=20)
ax1.set_ylabel('Bond Valence Determinant(s_det)', fontsize=20)
ax1.xaxis.set_tick_params(labelsize=20)
ax1.yaxis.set_tick_params(labelsize=20)
ax1.set_xlim(0,13)

ax1.plot([0, 12], [4.5, 4.5], color='red',lw=5)

for index, row in dfcn.iterrows(): 
    ax1.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'],linewidths=5)
    ax1.legend(loc='right',bbox_to_anchor=(1.6,0.5))

#plt.title("Bond Valence Determinant plot for sites with coordination number 5",fontsize=20)
plt.show()
# %%
