#%%
import matplotlib.pyplot as plt
from matplotlib.image import imread
import pandas as pd
import seaborn as sns
from sklearn.datasets.samples_generator import (make_blobs,
                                                make_circles,
                                                make_moons)
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_samples, silhouette_score

#%matplotlib inline
sns.set_context('notebook')
plt.style.use('fivethirtyeight')
from warnings import filterwarnings
filterwarnings('ignore')

# Import the data
df0 = pd.read_csv('./output/Angles_5541.csv')
df1 = pd.read_csv('./output/CN4_Angles_all_cat_9704.csv')
# Plot the data
fig, ax = plt.subplots(1, 2, figsize=(16, 8))

ax[0].scatter(df0.iloc[:, 0], df0.iloc[:, 1])
ax[0].set_xlabel('Largest angle')
ax[0].set_ylabel('Second largest angle')
ax[0].set_title('Data_1088')
ax[1].scatter(df1.iloc[:, 0], df1.iloc[:, 1])
ax[1].set_xlabel('Largest angle')
ax[1].set_ylabel('Second largest angle')
ax[1].set_title('Data_5541')


X_std = StandardScaler().fit_transform(df1)

#%%
km = KMeans(n_clusters=5)
km.fit(X_std)
labels = km.predict(X_std)
centroids = km.cluster_centers_

#%matplotlib notebook
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(df1.iloc[:, 0], df1.iloc[:, 1], df1.iloc[:, 2], c=labels)
ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], marker='o',
                c="white", alpha=1, s=200, edgecolor='k')
for i, c in enumerate(centroids):
    ax.scatter(c[0], c[1], c[2], marker='$%d$' % i, s=50, alpha=1, edgecolor='r')
plt.show()

# %%
import ipyvolume as ipv 

ipv.quickvolshow(df1.iloc[:,1:3],opacity=0.03, level_width=0.1, data_min=0, data_max=1)
# %%
