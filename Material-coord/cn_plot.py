#%%
import pandas as pd

df = pd.read_excel('.\Results_for_ternary_sample.xlsx',index_col=0,sheet_name='MC')

#%%
# Convert the list in loaded pandas
def convertfloat(list_):
    if not isinstance(list_,str): return list_
    for i in list_:
        i = float(i)
    return list_

for col in df:
    if col in ['ionType','r','occ','n','s','BVS','s_ave','s_det']:
        df[col] = df[col].apply(eval)
    if col in ['r','occ','n','s','BVS','s_ave','s_det']:
        df[col] = df[col].apply(convertfloat)

# %%
dfcn4 = df[(df['Coordination']==4) & (df['OS']>0)]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,7))
ax1 = fig.add_subplot(111)
ax1.xaxis.set_tick_params(labelsize=20)
ax1.yaxis.set_tick_params(labelsize=20)
ax1.set_xlim(0,11)
ax1.set_ylim(0,16)
ax1.set_xlabel('Running Coordination Number $N_{RCN}$', fontsize=18)
ax1.set_ylabel('Bond Valence Coordination Number \n Determinant $N_{det}$', fontsize=16)

#ax1.plot([0, 12], [6, 6], color='red',lw=5)
#ax1.plot([0, 12], [4, 4], color='blue',lw=5)
ax1.plot([4.5, 4.5], [-1, 17], color='blue',lw=1, ls='--')

for index, row in dfcn4.iterrows(): 
    ax1.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'],linewidths=5)
    ax1.legend(loc='right',bbox_to_anchor=(1.6,0.5))
    

plt.show()

# %%
dfcn4 = df[(df['Coordination']==6) & (df['OS']>0)]

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(7,7))
ax1 = fig.add_subplot(111)
ax1.xaxis.set_tick_params(labelsize=20)
ax1.yaxis.set_tick_params(labelsize=20)
ax1.set_xlim(0,11)
ax1.set_ylim(0,16)
ax1.set_xlabel('Running Coordination Number $N_{RCN}$', fontsize=18)
ax1.set_ylabel('Bond Valence Coordination Number \n Determinant $N_{det}$', fontsize=16)

#ax1.plot([0, 12], [6, 6], color='red',lw=5)
#ax1.plot([0, 12], [4, 4], color='blue',lw=5)
ax1.plot([6.5, 6.5], [-1, 17], color='blue',lw=1, ls='--')

for index, row in dfcn4.iterrows(): 
    ax1.scatter(row['n'],row['s_det'],label=row['Site']+", "+row['File'],linewidths=5)
    ax1.legend(loc='right',bbox_to_anchor=(1.6,0.5))
    

plt.show()
# %%
#dfcn4 = df[(df['Coordination']==12) & (df['OS']>0)]
dfcn4 = df[(df['Coordination']==4)]
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
df_cn425 = pd.read_excel('.\Results_for_ternary_sample_cn425.xlsx',index_col=0)

for col in df_cn425:
    if col in ['ionType','r','occ','n','s','BVS','s_ave','s_det']:
    #df[col] = df[col].apply(clean_alt_list)
        df_cn425[col] = df_cn425[col].apply(eval)
    if col in ['r','occ','n','s','BVS','s_ave','s_det']:
        df_cn425[col] = df_cn425[col].apply(convertfloat)

# %%
df_cn45 = pd.read_excel('.\Results_for_ternary_sample.xlsx',index_col=0,sheet_name='softBV')

for col in df_cn45:
    if col in ['ionType','r','occ','n','s','BVS','s_ave','s_det']:
        df_cn45[col] = df_cn45[col].apply(eval)
    if col in ['r','occ','n','s','BVS','s_ave','s_det']:
        df_cn45[col] = df_cn45[col].apply(convertfloat)
# %%
df_cn425.compare(df_cn45)
# %%
''' to find the col
i = 0
for x in df['File']:
    if x == 'TlAlF4_202453':
        print(i)
    i += 1  
'''  