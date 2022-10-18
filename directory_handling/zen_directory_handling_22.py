from time import strftime
from tkinter import *
from tkinter import * 
from tkinter.filedialog import askdirectory
import filecmp
import os
import csv
from datetime import datetime, timezone

# Global Variables
dcmp = None
diff_files = []
time_now = datetime.now()
time_now_format = time_now.strftime("%Y%m%d_%H%M")


def select_directory():
    return askdirectory(title="Choose your directory", mustexist=True)

def analyze_two_directories(dir_cmp_obj):
    # Creation of lists
    dir1_only = dir_cmp_obj.left_only
    dir2_only = dir_cmp_obj.right_only
    global diff_files
    diff_files = dir_cmp_obj.diff_files

    # Creation of filename according to time now
    folder_name_1 = dir_cmp_obj.left.split("/")
    folder_name_2 = dir_cmp_obj.right.split("/")
    
    filename = folder_name_1[len(folder_name_1)-1].replace(" ","_") + \
               "_vs_" + folder_name_2[len(folder_name_2) - 1].replace(" ", "_") + \
                "_at_" + time_now_format + ".txt"
    # print(filename)

    # Creation of a text file
    with open(filename, "w", encoding='utf-8') as file:
        file.write(dir_cmp_obj.left)
        file.write("\n")

        # To list out files that only exist in first directory
        if len(dir1_only) > 0:
            for _ in dir1_only:
                temp_name = dir_cmp_obj.left + "/" + _

                if os.path.isfile(temp_name) or os.path.isdir(temp_name):
                    if _[0] == ".":
                        output = "System File: " + _
                        file.write(output)
                    else:
                        file.write(_)

                    file.write("\n")     
        else:
            file.write("No distinct files found in 1st directory")
            file.write("\n")  
        
        file.write("\n")
        file.write(dir_cmp_obj.right)
        file.write("\n")

        # To list out files that only exist in second directory
        if len(dir2_only) > 0:
            for _ in dir2_only:
                temp_name = dir_cmp_obj.right + "/" + _

                if os.path.isfile(temp_name) or os.path.isdir(temp_name):
                    if _[0] == ".":
                        output = "System File: " + _
                        file.write(output)
                    else:
                        file.write(_)
                        
                    file.write("\n")
        else:
            file.write("No distinct files found in 2nd directory")
            file.write("\n")  

        file.write("\n")
        file.write("Different files here: \n")

        # To list down same filename but different content
        if len(diff_files) > 0:
            for _ in diff_files:
                file.write(_)
                file.write("\n")
        else:
            file.write("Hooray! No same filename of different stats :)")

def generate_csv_same_files(list_of_files, dir1, dir2):
    # Create a list of values 
    values = []

    for _ in list_of_files:
        # Create a dictionary
        temp = {}

        path1 = dir1 + "/" +_
        stat_1 = os.stat(path1)

        temp["filename"] = _
        temp["left_path"] = dir1
        file_size_1 = stat_1.st_size/1000
        temp["left_file_size(kb)"] = file_size_1
        

        modified_1 = datetime.fromtimestamp(stat_1.st_mtime, tz=timezone.utc)
        temp["left_modified_time"] = modified_1

        path2 = dir2 + "/" +_
        stat_2 = os.stat(path2)
        temp["right_path"] = dir2
        file_size_2 = stat_2.st_size/1000
        temp["right_file_size(kb)"] = file_size_2
        
        modified_2 = datetime.fromtimestamp(stat_2.st_mtime, tz=timezone.utc)
        temp["right_modified_time"] = modified_2

        if modified_1 < modified_2:
            temp["analyze_modification"] = "RIGHT is latest"
        else:
            temp["analyze_modification"] = "LEFT is latest"
        
        if file_size_1 < file_size_2:
            temp["analyze_file_size"] = "RIGHT is bigger"
        else:
            temp["analyze_file_size"] = "LEFT is bigger"
        
        values.append(temp)
    
    filename = "Different_Files_Same_Name_" + time_now_format +\
                ".csv"

    keys=["filename", "left_path", "left_file_size(kb)",
          "left_modified_time", "right_path", "right_file_size(kb)",
          "right_modified_time","analyze_modification",
          "analyze_file_size"]

    with open(filename,"w", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(values)

dir1 = select_directory()
dir2 = select_directory()
dcmp = filecmp.dircmp(dir1, dir2, ignore=filecmp.DEFAULT_IGNORES)
analyze_two_directories(dcmp)
generate_csv_same_files(diff_files, dir1, dir2)