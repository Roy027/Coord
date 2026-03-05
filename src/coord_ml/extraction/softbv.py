import subprocess
import os
import pandas as pd
import numpy as np

class SoftBVExtractor:
    """
    Wrapper for softBV executables to extract coordination information.
    """
    def __init__(self, bin_dir: str):
        self.bin_dir = os.path.abspath(bin_dir)
        self.exe_path = os.path.join(self.bin_dir, 'softBV_cnprint2.exe')
        self.unitary_path = os.path.join(self.bin_dir, 'database_unitary.dat')

    def get_unitary_df(self):
        """
        Reads the database_unitary.dat file.
        """
        skip_rows = list(range(0, 12)) + [13, 14] + list(range(206, 217))
        return pd.read_fwf(self.unitary_path, skiprows=skip_rows)

    def fill_site_info_from_stdout(self, stdout: str):
        """
        Parses the output of softBV to extract site information.
        """
        stdout_lines = stdout.splitlines()
        sites = {}
        name = ""
        for line in stdout_lines:
            parts = line.replace(" ", ";").replace("=", ";").split(";")
            parts = ' '.join(parts).split()
            if len(parts) < 2:
                continue
            if parts[1] == 'name:':
                name = ' '.join(parts[2:])
            if len(parts) < 9:
                continue
            if parts[3] == "name":
                if parts[4] not in sites:
                    sites[parts[4]] = {
                        'type': parts[6],
                        'os': parts[8]
                    }
        return sites, name

    def extract_site_dic(self, cif_path: str, sites: dict):
        """
        Runs softBV for each site to get detailed coordination data.
        """
        site_dic = {}
        for site in sites.keys():
            coor = []
            center = ""
            # Note: This requires running the Windows .exe, might fail on Linux
            # In a professional setting, we'd handle OS compatibility.
            try:
                proc = subprocess.run(
                    [self.exe_path, "--cal-cn-bv", cif_path, site],
                    cwd=self.bin_dir,
                    capture_output=True,
                    text=True
                )
                stdout = proc.stdout
                lines = stdout.splitlines()
                
                cn = 0.0
                sd_bv = 0.0
                
                for line in lines:
                    parts = line.split()
                    if len(parts) < 1:
                        continue
                    if parts[1] == "Center":
                        center = parts[3]
                    if parts[1] == "XYZ:":
                        # Center atom coordinates
                        coor.append([center, (float(parts[3]), float(parts[4]), float(parts[5]))])
                    if parts[1] == "Coordination":
                        cn = float(parts[3])
                    if parts[1] == "BVS:":
                        sd_bv = float(parts[6])
                    
                    if len(parts) < 12:
                        continue
                    if parts[5].isalpha():
                        continue
                        
                    # Extract neighbors
                    if float(parts[5]) <= cn:
                        coor.append([parts[2], (float(parts[10]), float(parts[11]), float(parts[12]))])
                
                if center:
                    site_dic[center] = {
                        'cn': cn,
                        'sd_bv': sd_bv,
                        'coordinates': coor
                    }
            except Exception as e:
                print(f"Error processing site {site} in {cif_path}: {e}")
                
        return site_dic
