import subprocess
import sys
import os
import ast
import shutil
from pathlib import Path

#parameters that we want personally
CN="6"
i_want_this_CN = int(CN)

megadirectory = 'Li_database'
softBV = "softBV"
cmds = "--cal-cn-bv"
ionname = "Li1"

# make a folder for the program to copy files to
path_to_storage_folder = os.path.join(os.getcwd(), "cif files with CN" + CN)
pathcheck = Path(path_to_storage_folder)
if pathcheck.exists() == False:
    os.mkdir(path_to_storage_folder())

# os.listdir(<directory>) creates a list of every file in directory.
# Using a for-loop to iterate over the list, calling for os.path.join(directory, filename) to build a full path to each file name in the list, with <directory> from the previous step.
# call <command>(<path>) to execute command on the file

# in order to extract CN...
# firstly convert the output into a string.
# since the string is in the form of a huge paragraph, I can split the huge chunk of string into an array of strings.
# then identify the coordination number based on the similarities in the elements of the array
for foldername in os.listdir(megadirectory):
    directory = megadirectory + '/' + foldername
    print('****************************** Now checking for directory ' + foldername + ' ******************************')
    if os.path.isdir(directory):
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

                # check whether there exists a recorded coordination number
                # if there are no CN recorded, skip the item in the list
                # if there is, remove the text "CN: Coordination Number: ", convert the remaining contents into a float, and then round off the float to the nearest ones place.
                # if the endvalue equals to i_want_this_CN, then we extract the file name and do things with it.
                CN_check = 0
                occ_check = 0

                # defines CN variable in order to remove other parts of string to obtain a float
                # so that we can then round off the float to check the coordination number.
                CN_label = 0
                line_number = 0
                for line_item in string_splittoarraystring:
                    detect_CN = line_item.find("CN: Coordination Number: ")
                    if (detect_CN != -1):
                        CN_label = line_item                  
                        remove_label = CN_label.strip("CN: Coordination Number: ")
                        identified_CN = float(remove_label)
                        rounded_CN = round(identified_CN)
                        if (rounded_CN == i_want_this_CN):
                            copied_file = path_to_storage_folder + '/' + filename
                            print(byte_to_string)
                            shutil.copyfile(cifname,copied_file)
                        else:
                            continue
            else:
                continue
    else:
        print(foldername + " is not a folder...")