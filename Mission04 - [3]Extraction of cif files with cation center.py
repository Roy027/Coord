import subprocess
import sys
import os
import ast
import shutil
from pathlib import Path


# source folder of the cif files with a particular CN
directory = 'cif files with CN6 and with full occupancy'
softBV = "softBV"
cmds = "--cal-cn-bv"
ionname = "Li1"

# make a folder for the program to copy files to
path_to_storage_folder = os.path.join(os.getcwd(), directory + " and cation only")
pathcheck = Path(path_to_storage_folder)
if pathcheck.exists() == False:
    os.mkdir(path_to_storage_folder)

# os.listdir(<directory>) creates a list of every file in directory.
# Using a for-loop to iterate over the list, calling for os.path.join(directory, filename) to build a full path to each file name in the list, with <directory> from the previous step.
# call <command>(<path>) to execute command on the file
for filename in os.listdir(directory):
    if filename.endswith(".cif"):
        print("NOW PROCESSING " + filename)
        cifname = directory + "/" + filename
        # subprocess.run([<program>, <program commands, akin to stuff you type in command prompt>], <keyword arguments, e.g. capture_output=True, text=True>)
        result = subprocess.run([softBV, cmds, cifname, ionname],capture_output=True)
        # conversion of stdout into string
        byte_data=result.stdout
        byte_to_string = byte_data.decode("utf-8")
        #split the string containing line breaks, into single-line strings with no line breaks. the "False" means to remove the line break commands, i.e. \r\n
        string_splittoarraystring = byte_to_string.splitlines(False)

        for line_item in string_splittoarraystring:
                # similar to checking whether there exists a recorded coordination number:
                # if there are no cation recorded, skip the item in the list
                # if there is, copy the file
                detect_cation_line = line_item.find("CN: Center atom: ")
                detect_cation = line_item.find("+)")
                if (detect_cation_line != -1 and detect_cation != -1):
                    copied_file = path_to_storage_folder + '/' + filename
                    shutil.copyfile(cifname,copied_file)
                else:
                    continue