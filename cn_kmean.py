# %%
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

%matplotlib inline
sns.set_context('notebook')
plt.style.use('fivethirtyeight')
from warnings import filterwarnings
filterwarnings('ignore')
# %%
# Import the data
df0 = pd.read_csv('./output/CN4_Angles.csv')
df1 = pd.read_csv('./output/Angles_5541.csv')
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

# %%
