from calculateCfosIntensity import CalculateCfosIntensity
from create_image_for_DataSet import create_iamges_for_DataSet
from csv_section_initialize import Initialize_CSV_Files
from getCSVbyBregma import separatePointCSVfile
from export_region_csv import Export_Region_CSV
from separate_dorsal_ventral_hippocampus import separate_dorsal_ventral_hippocmapus
from separate_regions import Separate_Regions
from Dentate_Corpose import Create_csv_Dantate_Corpose
import os
import threading
import pandas as pn
from one_side import One_Side
from cfos_count import Cfos_Count
from drop_distrebutions import Drop_Distrebutions
from filterByBlobDetect import filterCellByBlobDetection


def initcsvFile(path, fileName, no_fit_list):
    print("?")
    returnList = Initialize_CSV_Files(path, fileName).action()
    no_fit_list.append(list(returnList))


def is_csv(file_name):
    return '.csv' in file_name and 'final' not in file_name and 'with' in file_name


def is_csv_for_second_stage(file_name):
    return '.csv' in file_name and 'final' not in file_name


def is_jp2(file_name):
    return '.jp2' in file_name


def get_csv_by_jp2(jp2_name, csv_list):
    for file in csv_list:
        if jp2_name[:-4] in file[:len(jp2_name[:-4])] and '.csv' in file and 'final' not in file and 'with' in file:
            return file


def calculateCfosThreading(path, image_name, csv_name):
    print(image_name + "  -  " + csv_name)
    CalculateCfosIntensity(path, image_name, csv_name).action(10)


def lastStage(folder_path):
    """
    use multi threading to calculate c-fos intensity and export csv files - using 'CalculateCfosIntensity' class
    :param folder_path: direction of the separate files (image and csv)
    """
    walkFiles = os.walk(folder_path)
    filesNames = []
    for root, dirs, file in walkFiles:
        filesNames = file

    print(filesNames)

    csv_files = [file for file in filter(is_csv, filesNames)]
    jp2_files = [file for file in filter(is_jp2, filesNames)]

    for image in jp2_files:
        image_name = image
        csv_name = get_csv_by_jp2(image_name, csv_files)
        # print(image_name + "  -  " + csv_name)
        threading.Thread(target=calculateCfosThreading, args=[folder_path, image_name, csv_name]).start()


def multi_thread_blob_filter(path):
    walkFiles = os.walk(path)
    filesNames = []
    for root, dirs, file in walkFiles:
        filesNames = file

    print(filesNames)

    csv_files = [file for file in filter(is_csv_for_second_stage, filesNames)]
    for file in csv_files:
        # threading.Thread(target=action_multi_checking, args=[path,file[:-4]+".jp2",file]).start()
        filterCellByBlobDetection(path, file[:-4]+".jp2", file).action(True)

def action_multi_checking(path,image,data):
    filterCellByBlobDetection(path, image, data).action()

path = r'D:\engram\New_Converted_Folder\N3\1h\csv files'

"""-----------------------"""

# export_region = Export_Region_CSV(r'D:\engram\New_Converted_Folder\N1\1h-Done\done\separate files')
# export_region.define_region('CA2')
# export_region.action(1)

"""------------------------"""
#
# s = Initialize_CSV_Files(path, "all_channels_1h_N3_points.csv")
# s.action()

"""----------------"""

# s = Separate_Regions(path, "Naive_N1", "all_channels_Naive_N1_points_withNames.csv", r'D:\engram\New_Converted_Folder\N1 - Copy\summary').action_parents()

"""-----------------------"""

# separatePointCSVfile(path,'all_channels_1h_N3_points_withNames.csv').separate_2('NeuN_Background.csv')
# separatePointCSVfile(path+"\\separate files").merge()

"""------------------"""

# f = Export_Region_CSV(path, "one", "1h_n2_points_withNames_1.5 std.csv")
# f.define_region("CA2")
# f.action_single_file(1)
# f.define_region("corpus callosum")
# f.action_single_file(2)

"""--------------"""

# Create_csv_Dantate_Corpose(path + "\\separate files", "-1255.csv").action()


"""----------------"""
# One_Side(path + "\\separate files").action(['-1455.csv','-3655.csv'], 2)
"""---------------"""

# Cfos_Count(path+"\\result", "points.csv").action_2(1.5)

"""-------------------------"""
# Drop_Distrebutions(r'D:\engram\New_Converted_Folder\N2\Naive', 'all_channel_Naive_N2_points.csv',
#                    'to_delete.csv').drop_by_folder(r'D:\engram\New_Converted_Folder\N2\Naive\csv files\separate files')


"""----------------------"""

# multi_thread_blob_filter(path+"\\separate files")
# filterCellByBlobDetection(r'C:\Users\owner\Desktop\New folder', '-3155.jp2', '-3155.csv').action()

create_iamges_for_DataSet(r'D:\engram\New_Converted_Folder\N2\1h\csv files\separate files').action()