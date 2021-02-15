import os
import threading
import pandas as pn
import numpy


class Export_Region_CSV:
    """
    After export intensity csv for each regions, this class using for export data of specific region
    """

    def __init__(self, path, mouse_name, file_name):
        """

        :param path: direction to folder that contain csv's files
        """
        self.__path = path
        self.__region_name = None
        self.__mouse_name = mouse_name
        self.__file_name=file_name

    def define_region(self, region):
        """

        :param region: region name - string
        :return: None
        """
        self.__region_name = region

    def action_separate_files(self, child_or_parent=1):
        """
        :param child_or_parent: 1 -  for child , 2 - for parent <B>default choice is 1<B>
        :return: export csv file contain data about the chosen region
        """

        def using_thread(path, csv_name, csv_list, child_or_parent=1):
            df = pn.read_csv(self.__path + "\\" + csv_name)
            if child_or_parent == 1:
                df = df[df['id name'].str.contains(self.__region_name + "|" + self.__region_name.lower(), na=False)]
            else:
                df = df[df['parent name'] == self.__region_name]
            csv_list.append(df)

        threads_list = []
        walk_os = os.walk(self.__path)
        for root, dirs, file in walk_os:
            files_names = file

        files_names = [i for i in filter(lambda file_name: '.csv' in file_name and 'withNames' in file_name,
                                         files_names)]
        csv_list = []

        for file in files_names:
            t = threading.Thread(target=using_thread, args=[self.__path, file, csv_list, child_or_parent])
            t.start()
            threads_list.append(t)

        for t in threads_list:
            t.join()

        output_df = pn.concat(csv_list)
        output_df.to_csv(self.__path + "\\" + self.__region_name + "_summary.csv", index=False)

    def action_single_file(self, child_or_parent=1):
        df = pn.read_csv(self.__path + "\\" + self.__file_name)
        if (child_or_parent == 1):
            df = df[df['id name'].str.contains(self.__region_name + "|" + self.__region_name.lower(), na=False)]
        else:
            df = df[df['parent name'] == self.__region_name]
        df.to_csv(self.__path + "\\" + self.__region_name + "_" + self.__mouse_name + ".csv", index=False)
