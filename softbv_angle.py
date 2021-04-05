import subprocess
import os
import glob
cwd = os.getcwd()
cwd_exe =os.path.join(cwd,'bin/softBV0405.exe')
cwd_cif =os.path.join(cwd,'test/CsCl.cif')
cwd_bin = os.path.join(cwd,'bin')
process = subprocess.run([cwd_exe, "--cal-cn-bv", cwd_cif, "Cs1"], cwd=cwd_bin, capture_output=True)
print(process.stdout)