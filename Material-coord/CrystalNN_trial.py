#%%
from pymatgen.analysis.local_env import CrystalNN
from pymatgen import Structure
import os
import glob

path = os.path.abspath(os.path.join('..',"./test/Sample_json/BaAl2O4_21080.json"))
#%%
json = Structure.from_file(path)

Crystal=CrystalNN()
# %%

