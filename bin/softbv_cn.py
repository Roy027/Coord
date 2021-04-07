import subprocess
import os
import glob
import numpy as np
from datetime import datetime

save_address = "../test/cifDic_20210407.npy"

print("Start time:", datetime.now())

cwd = os.getcwd()
cwd_exe =os.path.join(cwd,'softBV0405.exe')
all_files = glob.glob(os.path.join(cwd[:-4],'test/Li_database_CN4_occ1/*.cif'))

def fillSitesFromStdout(stdout):    
    stdout_lines = stdout.split("\r\n")
    Sites = set()
    for line in stdout_lines:
        line = line.replace(" ",";").split(";")
        line = ' '.join(line).split()
        if len(line)<10: continue
        if line[3] == "name=":
            Sites.add(line[4])
    return Sites

def fillSiteDic(Sites,cwd_exe,cif):
    SiteDic = {}
    for site in Sites:
        Coor = [[]]
        center = ""
        CalCNproc = subprocess.run([cwd_exe, "--cal-cn-bv", cif, site], cwd=r'd:\Study\softBV_mix\GitHub\projects\Coord\bin', capture_output=True)
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
                SiteDic[center] = [CN]
            if len(line) < 12: continue
            if line[5].isalpha(): continue
            if float(line[5]) <= CN:
                Coor.append([line[2]])
                Coor[-1].append((float(line[10]),float(line[11]),float(line[12])))
        if len(center) != 0: 
            SiteDic[center].append(Coor)
        else: 
            print("Problematic cif:",cif,Sites,"\n")
    return SiteDic

def calAngleToSiteDic(SiteDic):
    for site in SiteDic:
        l = len(SiteDic[site][1])
        SiteDic[site].append([])
        for i in range(1,l-1):
            for j in range(i+1,l):
                SiteDic[site][2].append(calAngleDeg(SiteDic[site][1][0][1], SiteDic[site][1][i][1], SiteDic[site][1][j][1]))
        SiteDic[site][2]=np.sort(SiteDic[site][2])[::-1]
    return SiteDic

def calAngleCos(V0,V1,V2):
    V0 = np.asarray(V0)
    V1 = np.asarray(V1)
    V2 = np.asarray(V2)
    Va = V1 - V0   
    Vb = V2 - V0
    cos = np.dot(Va/np.linalg.norm(Va), Vb/np.linalg.norm(Vb))
    return round(cos, 4)
# Calculate the angle radians
def calAngle(V0,V1,V2):
    V0 = np.asarray(V0)
    V1 = np.asarray(V1)
    V2 = np.asarray(V2)
    Va = V1 - V0   
    Vb = V2 - V0
    dot_product = round(np.dot(Va/np.linalg.norm(Va), Vb/np.linalg.norm(Vb)),4)
    angle = np.arccos(dot_product)
    return angle

def calAngleDeg(V0,V1,V2):
    V0, V1, V2 = [np.asarray(i) for i in [V0,V1,V2]]
    Va = V1 - V0   
    Vb = V2 - V0
    dot_product = round(np.dot(Va/np.linalg.norm(Va), Vb/np.linalg.norm(Vb)),4)
    angle = np.arccos(dot_product)
    deg = np.rad2deg(angle)
    return deg

# Main Process
cifDic = {}
for cif in all_files:
    cif_name = cif[68:]
    print("Currently proccessing:", cif_name, ";  Current Time:", datetime.now())
    cifDic[cif_name] = []
    process = subprocess.run([cwd_exe, "--print-cell", cif], cwd=r'd:\Study\softBV_mix\GitHub\projects\Coord\bin', capture_output=True)
    stdout = str(process.stdout, "utf-8")
    Sites = fillSitesFromStdout(stdout)
    SiteDic = fillSiteDic(Sites,cwd_exe,cif)
    SiteDic = calAngleToSiteDic(SiteDic)
    cifDic[cif_name].append(SiteDic)

np.save(save_address, cifDic)
