from Appendices.create_image_for_DataSet import create_images_for_DataSet
from Filters.filterByBlobDetect import filterCellByBlobDetection
import os

path = r'D:\engram\New_Converted_Folder\N1\Naive-Done\final\separate files'
# s=Export_Region_CSV(path)
# s.define_region('CA1')
# s.action(1)
#


# separate_dorsal_ventral_hippocmapus(path,'CA1_summary.csv').action(-1315)

# Summary_Data(r'D:\engram\New_Converted_Folder\N1\summary', r'D:\engram\New_Converted_Folder\N1\New folder').action()

# data = pn.read_csv(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\all_channels_0.5H_N2 _points.csv', skiprows=1)
# data[data['Unnamed: 0'].str.contains('NeuN_region_check')].to_csv(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\NeuN_Background.csv',
#                                                           index=False)

#
# df_before_filter = pn.read_csv(
#     r'D:\engram\New_Converted_Folder\N2\Naive\all_channel_Naive_N2_points_after_delete.csv')
# after_filter = len(pn.read_csv(
#     r'D:\engram\New_Converted_Folder\N2\Naive\all_channel_Naive_N2_points.csv'))
#
# # df_before_filter = df_before_filter[df_before_filter['Unnamed: 0'] == "DAPI"]
# before_filter = len(df_before_filter)
#
# print(after_filter / before_filter)
# print (after_filter)
# print (before_filter)


# df = pn.read_csv(r'D:\engram\New_Converted_Folder\N2\Naive\csv files\result\points_1.5 std.csv')
# bregma_counter = {}
# for bregma in df['z'].unique():
#     bregma_counter[bregma] = len(df[df['z'] == bregma])
# sorted_bregma=sorted(bregma_counter.keys(), key=lambda x: bregma_counter[x])
# print(sorted_bregma)
# print (bregma_counter)

def is_csv_for_second_stage(file_name):
    return '.csv' in file_name and 'final' not in file_name


def multi_thread_blob_filter(path):
    walkFiles = os.walk(path)
    filesNames = []
    for root, dirs, file in walkFiles:
        filesNames = file

    print(filesNames)

    csv_files = [file for file in filter(is_csv_for_second_stage, filesNames)]
    for file in csv_files:
        # threading.Thread(target=action_multi_checking, args=[path,file[:-4]+".jp2",file]).start()
        filterCellByBlobDetection(path, file[:-4] + ".jp2", file).action(True)


# filterCellByBlobDetection(r'C:\Users\owner\Desktop\New folder', '-1155.jp2', '-1155.csv').action(True)
# multi_thread_blob_filter(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\separate files')

# separatePointCSVfile(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\filtered').merge()
#
# summery_data_to_single_csv(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\filtered','points.csv').action()

create_images_for_DataSet(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\separate files').action()
