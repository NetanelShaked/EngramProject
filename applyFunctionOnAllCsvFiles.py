import os
from Filters.FilterCfosResults import filterNuclesByCfos

def applyFunctionOnAllCsvFiles(path, function):
    """

    :param path: path to folder contain all csv files
    :param function: function to apply on all csv files
    :return: depend on function was sent
    """
    files_names = []
    walk_os = os.walk(path)
    for root, dirs, file in walk_os:
        files_names = file
    result_list = []
    files_names = [i for i in filter(lambda file_name: '.csv' in file_name, files_names)]
    for file in files_names:
        file_name = file[:-4]
        print(file_name)
        result_list.append(function(path, file_name + ".jp2", file_name + ".csv"))
    return result_list

if __name__ == '__main__':
    path=r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files'
    applyFunctionOnAllCsvFiles(path,filterNuclesByCfos)