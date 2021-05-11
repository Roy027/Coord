
import matplotlib.pyplot as plt
import pandas as pd

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

df = pd.read_csv('./output/CN4_Angles_all_cat_9704.csv')

ax.scatter(df.iloc[:,0], df.iloc[:,1], df.iloc[:,2], c= 'r', marker= 'o' )

ax.set_xlabel('Largest Angle')
ax.set_ylabel('2nd Largest Angle')
ax.set_zlabel('3rd Largest Angle')

plt.show()
# %%
