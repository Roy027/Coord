import subprocess
import sys
import os
import ast
import shutil
from pathlib import Path


# source folder of the cif files with a particular CN
directory = 'cif files with CN6'
softBV = "softBV"
cmds = "--cal-cn-bv"
ionname = "Li1"

# make a folder for the program to copy files to
path_to_storage_folder = os.path.join(os.getcwd(), directory + " and with full occupancy")
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
        # here is the second check on the occupancy, after checking for coordination number
        # from what I see in SoftBV output, the list of sites are listed from line 12 onwards
        # but we need to determine whether that line we're checking does actually contain the occupancy value or not
        # hence we split the single line into a list of items
        # the occupancy column is on the 5th column (hence the value 4) - we convert that string into float if it's not a letter
        # and then chenc whether it's above 0.99 or not.
        line_number = 0
        for line_item in string_splittoarraystring:
            line_number = line_number + 1
            if (line_number >= 12):
                splitline_detect_occupancy = line_item.split( )
                detect_occupancy_line = splitline_detect_occupancy[4]

                # this function below looks for any character that is a digit
                # cannot confuse with <string>.isnumeric() function because it checks whether ALL the characters is a number
                # in this case our data may have a decimal point, so it's also not considered as a number...
                is_number = any(chr.isdigit() for chr in detect_occupancy_line)
                if (is_number == True):
                    detect_occupancy = float(detect_occupancy_line)
                    if (detect_occupancy > 0.99):
                        copied_file = path_to_storage_folder + '/' + filename
                        shutil.copyfile(cifname,copied_file)