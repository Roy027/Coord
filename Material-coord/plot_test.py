#%%
from pymatgen.analysis.local_env import BrunnerNN_reciprocal, EconNN, JmolNN, \
                                        MinimumDistanceNN, MinimumOKeeffeNN, MinimumVIRENN, \
                                        VoronoiNN, CrystalNN


nn_methods = [
    MinimumDistanceNN(),  MinimumOKeeffeNN(), MinimumVIRENN(), JmolNN(), 
    EconNN(tol=0.5), BrunnerNN_reciprocal(), VoronoiNN(tol=0.5), CrystalNN()
]


from materialscoord.core import Benchmark

structure_groups = ["A2BX4", "ABX3", "ABX4"]

bm = Benchmark.from_structure_group(structure_groups)


# %%
cation_score = bm.score(nn_methods, site_type="cation")
cation_score.to_excel("cation_score.xlsx")
# %%
import pandas as pd
import numpy as np
softBV_result = pd.read_excel('cation_score.xlsx',index_col=0,dtype={'softBV':np.float64})
# %%
from pathlib import Path
from materialscoord import structure_mapping
from materialscoord.plot import plot_benchmark_scores
nn_method_mapping = {"BrunnerNN_reciprocal": "BrunnerNN"}
plt = plot_benchmark_scores(softBV_result,structure_mapping=structure_mapping,nn_method_mapping=nn_method_mapping)
#plt.savefig(Path("plots", "ternary-cation.pdf"), bbox_inches='tight')
plt.show()
# %%
