#%%
## This script is to analyse the different between min_percent 0.02 and 0.03
import subprocess
import os
from pathlib import Path
import glob
import numpy as np
import pandas as pd
import json
import time
from datetime import datetime

# Input parameter
BV_CUTOFF = [2.8,4.5]
BV_MIN_PCT = [0.01,0.02,0.03]
cumBVS_min_pct = [0.70]
Save_address = 'CN_compare_MC.xlsx'
softBV_exe = 'softBV_CN_break.exe'


La = len(BV_CUTOFF)
Lb = len(BV_MIN_PCT)
Lc = len(cumBVS_min_pct)

# Check the following addresses before running the script
FileDir = os.path.abspath(os.path.join('..','test/coord_cif'))
GroupDir = [folder for folder in os.scandir(FileDir) if folder.is_dir()]
cifFile = []
for (r,d,f) in os.walk(FileDir):
    for fi in f:
        if fi.endswith('.cif') and r.endswith(('Binary','A2BX4','ABX3','ABX4')):
            cifFile.append(os.path.join(r,fi))

print("Start time:", datetime.now())

cwd = os.path.abspath("../bin")
cwd_exe =os.path.join(cwd,softBV_exe)

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

def fillSiteLists(Sites, cwd_exe, cif, bv_cutoff, bv_min_pct, p_BVS):
    SiteLists = []
    for site in Sites.keys():
        Coor = [[]]
        ionType, r, occ, n, s, BVS, s_ave, s_det = [], [], [], [], [], [], [], []
        center = ""
        CalCNproc = subprocess.run([cwd_exe, "--cal-cn-bv", cif, site, str(bv_cutoff), str(bv_min_pct), str(p_BVS)], cwd=cwd, capture_output=True)
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
            row = [center, Sites[site]['type'], Sites[site]['os'], CN]
            SiteLists.append(row)
        else: 
            print("Problematic cif:",cif,site)
    return SiteLists

def appendSiteLists(SiteTable, SiteLists, cif_name):   
    for sitelist in SiteLists:
        row = [cif_name]
        row.extend(sitelist)
        SiteTable.append(row)
    return SiteTable 

# Load Unitary Database
uni_df = UnitaryDF()


# Main process to populate the 

#2D arrary stores the dataframe for various parameters
df_map = [[[0 for _ in range(Lc)] for _ in range(Lb)] for _ in range(La)]


for a in range(La):
    for b in range(Lb):
        for c in range(Lc):
        #if a < 4 or b < 4: continue
            SiteTable = []
            for i,cif in enumerate(cifFile):
                cif_name =cif.split("\\")[-1][:-4]
                print("Currently proccessing:", cif_name, " Status:", i, "/", file_num," Current Time:", datetime.now())
                process = subprocess.run([cwd_exe, "--print-cell", cif], cwd=cwd, capture_output=True)
                stdout = str(process.stdout, "utf-8")
                Sites, name = fillSitesFromStdout(stdout)
                SiteLists = fillSiteLists(Sites,cwd_exe,cif,BV_CUTOFF[a],BV_MIN_PCT[b], cumBVS_min_pct[c])
                SiteTable = appendSiteLists(SiteTable,SiteLists,cif_name)
            print("Processing Done for", "BV_CUTOFF:", BV_CUTOFF[a], " bv_min_pct:", BV_MIN_PCT[b])
            df_map[a][b][c] = pd.DataFrame(SiteTable,columns=['File','Site','Type','OS','CN_'+\
                                                               str(BV_CUTOFF[a])+'_'+\
                                                               str(BV_MIN_PCT[b])+'_'+\
                                                               str(cumBVS_min_pct[c])   ],dtype=float)

#%%
df_std = pd.read_excel('.\CN_by_material-coord.xlsx',index_col=0)

df_result = pd.DataFrame()
df_result = df_std[["File",'Type','OS','CN_by_MC']]
para_str_list, stddif_list,diffsite_list = [],[],[]
for a in range(La):
    for b in range(Lb):
        for c in range(Lc):
            para_str = str(BV_CUTOFF[a])+'_'+str(BV_MIN_PCT[b])+'_'+str(cumBVS_min_pct[c])
            para_str_list.append(para_str)
            df_result['softNV_CN_'+para_str] = df_map[a][b][c]['CN_'+para_str]
            stddif_list.append((df_map[a][b][c][df_map[a][b][c]['OS']>0]['CN_'+para_str] -\
                                df_std[df_std['OS']>0]["CN_by_MC"]).std())
            diffsite_list.append(len((df_map[a][b][c][df_map[a][b][c]['OS']>0]['CN_'+para_str] -\
                                      df_std[df_std['OS']>0]["CN_by_MC"]).to_numpy().nonzero()[0]))
df_result.to_excel("CN_MC_compared_softBV_break.xlsx")
df_compare =  pd.DataFrame(list(zip(para_str_list,stddif_list,diffsite_list)),
                            columns=['Parameters','Standard Difference','Number of different occurrence'])
df_compare.to_excel("CN_MC_compared_softBV_break_cal.xlsx")
# %%

