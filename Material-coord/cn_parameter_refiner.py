#%%
# This script is to get all the site for comparison for various bv_cutoff and min_percent
#
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
BV_CUTOFF = [4, 4.25, 4.5, 4.75, 5, 5.25, 5.5, 5.75, 6, 6.25, 6.5, 6.75, 7, 7.25, 7.5, 7.75, 8]
MIN_PERCENT = [0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05]
p_PVS_min = '0.80'
Save_address = 'bv_cutoff_min_percent_BVS80percent.xlsx'
variance_address = "variance_80percent.xlsx"

La = len(BV_CUTOFF)
Lb = len(MIN_PERCENT)

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
cwd_exe =os.path.join(cwd,'softBV_CN_test1.exe')

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

def fillSiteLists(Sites, cwd_exe, cif, bv_cutoff, min_percent, p_BVS):
    SiteLists = []
    for site in Sites.keys():
        Coor = [[]]
        ionType, r, occ, n, s, BVS, s_ave, s_det = [], [], [], [], [], [], [], []
        center = ""
        CalCNproc = subprocess.run([cwd_exe, "--cal-cn-bv", cif, site, str(bv_cutoff), str(min_percent), str(p_BVS)], cwd=cwd, capture_output=True)
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
df_map = [[i for i in range(Lb)] for _ in range(La)]


for a in range(La):
    for b in range(Lb):
        #if a < 4 or b < 4: continue
        SiteTable = []
        for i,cif in enumerate(cifFile):
            cif_name =cif.split("\\")[-1][:-4]
            print("Currently proccessing:", cif_name, " Status:", i, "/", file_num," Current Time:", datetime.now())
            process = subprocess.run([cwd_exe, "--print-cell", cif], cwd=cwd, capture_output=True)
            stdout = str(process.stdout, "utf-8")
            Sites, name = fillSitesFromStdout(stdout)
            SiteLists = fillSiteLists(Sites,cwd_exe,cif,BV_CUTOFF[a],MIN_PERCENT[b], p_PVS_min)
            SiteTable = appendSiteLists(SiteTable,SiteLists,cif_name)
        print("Processing Done for", "BV_CUTOFF:", BV_CUTOFF[a], " min_percent:", MIN_PERCENT[b])
        df_map[a][b] = pd.DataFrame(SiteTable,columns=['File','Site','Type','OS','CN_'+str(BV_CUTOFF[a])+'_'+str(MIN_PERCENT[b])],dtype=float)

df_std = pd.read_excel('.\softBV-coord_mix.xlsx',index_col=0)

df_result = pd.DataFrame()
df_result = df_std[["File",'Type','OS','MC_CN']].copy()
for a in range(La):
    for b in range(Lb):
        df_result['CN_'+str(BV_CUTOFF[a])+'_'+str(MIN_PERCENT[b])] = df_map[a][b]['CN_'+str(BV_CUTOFF[a])+'_'+str(MIN_PERCENT[b])]
df_result.to_excel(Save_address)
# %%

BV_CUTOFF_col = [str(i) for i in BV_CUTOFF]
MIN_PERCENT_row = [str(i) for i in MIN_PERCENT]
#variance_df = pd.DataFrame(variance_map,columns=BV_CUTOFF_col,index=MIN_PERCENT_row)
variance_cat_map = [[i for i in range(Lb)] for _ in range(La)]
diff_cat_map = [[i for i in range(Lb)] for _ in range(La)]
for a in range(La):
    for b in range(Lb):
        variance_cat_map[a][b] = (df_map[a][b][df_map[a][b]['OS']>0]['CN_'+str(BV_CUTOFF[a])+'_'+str(MIN_PERCENT[b])] - df_std[df_std['OS']>0]["MC_CN"]).pow(2).sum()
        diff_cat_map[a][b] = len((df_map[a][b][df_map[a][b]['OS']>0]['CN_'+str(BV_CUTOFF[a])+'_'+str(MIN_PERCENT[b])] - df_std[df_std['OS']>0]["MC_CN"]).to_numpy().nonzero()[0])
variance_cat_df = pd.DataFrame(variance_cat_map,columns=MIN_PERCENT_row,index=BV_CUTOFF_col)
diff_cat_df = pd.DataFrame(diff_cat_map,columns=MIN_PERCENT_row,index=BV_CUTOFF_col)

variance_map = [[i for i in range(Lb)] for _ in range(La)]
diff_map = [[i for i in range(Lb)] for _ in range(La)]
for a in range(La):
    for b in range(Lb):
        variance_map[a][b] = (df_map[a][b]['CN_'+str(BV_CUTOFF[a])+'_'+str(MIN_PERCENT[b])] - df_std["MC_CN"]).pow(2).sum()
        diff_map[a][b] = len((df_map[a][b]['CN_'+str(BV_CUTOFF[a])+'_'+str(MIN_PERCENT[b])] - df_std["MC_CN"]).to_numpy().nonzero()[0])
variance_df = pd.DataFrame(variance_map,columns=MIN_PERCENT_row,index=BV_CUTOFF_col)
diff_df = pd.DataFrame(diff_map,columns=MIN_PERCENT_row,index=BV_CUTOFF_col)

with pd.ExcelWriter(variance_address) as f:
    variance_cat_df.to_excel(f,sheet_name='variance_cat')
    variance_df.to_excel(f,sheet_name='variance_all')
    diff_cat_df.to_excel(f,sheet_name='diff_cat')
    diff_df.to_excel(f,sheet_name='diff_all')
