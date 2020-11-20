import pandas as pn
import os


class Separate_Regions:
    """
        This class using for separate main csv file to regions csv's
    """

    def __init__(self, path, mouse_name, csv_file_name, destination_folder):
        """

        :param path: direction to folder that contain the main csv file
        :param mouse_name:  Mouse name (string)
        :param csv_file_name: csv file name with extension
        :param destination_folder: where the output will save
        """
        self.__destination_folder = destination_folder
        self.__path = path
        self.__mouse_name = mouse_name
        self.__csv_file_name = csv_file_name

    def action_separate_folders(self):
        """

        :return: export to destination folder csv files organize by regions folders
        """
        df = pn.read_csv(self.__path + "\\" + self.__csv_file_name)
        all_regions_parents = df['region'].unique()
        for parent_region in all_regions_parents:
            if parent_region == '??':
                continue
            os.mkdir(self.__destination_folder + "\\" + parent_region)
            id_names = df[df['region'] == parent_region]['id name'].unique()
            for region in id_names:
                df[df['id name'] == region][['z', 'Channel 1', 'Channel 2', 'Channel 3']].to_csv(
                    self.__destination_folder + "\\" + parent_region +
                    "\\" + str(region).replace('/',
                                               '-') + "_" + self.__mouse_name + ".csv", index=False)

    def action(self):
        """

        :return: export to destination folder csv file for each id name
        """
        df = pn.read_csv(self.__path + "\\" + self.__csv_file_name)
        df.rename(columns={'channel01': 'Channel 1', 'channel02': 'Channel 2'}, inplace=True)
        print(df.columns)
        all_regions_parents = df['id name'].unique()
        for region in all_regions_parents:
            if region == '??':
                continue
            df[df['id name'] == region][['z', 'Channel 1', 'Channel 2', 'Channel 3']].rename(
                columns={'Channel 1': 'Channel 1 ' + self.__mouse_name,
                         'Channel 2': 'Channel 2 ' + self.__mouse_name,
                         'Channel 3': 'Channel 3 ' + self.__mouse_name}).to_csv(
                self.__destination_folder + "\\" + \
                str(region).replace('/', '-') + "_" + self.__mouse_name + ".csv", index=False)

    def action_parents(self):
        """
        :return: export to destination folder csv file for each id parent name
        """
        df = pn.read_csv(self.__path + "\\" + self.__csv_file_name)
        df.rename(columns={'channel01': 'Channel 1', 'channel02': 'Channel 2'}, inplace=True)
        print(df.columns)
        all_regions_parents = df['parent name'].unique()
        for region in all_regions_parents:
            if region == '??':
                continue
            df[df['parent name'] == region][['z', 'Channel 1', 'Channel 2', 'Channel 3']].rename(
                columns={'Channel 1': 'Channel 1 ' + self.__mouse_name,
                         'Channel 2': 'Channel 2 ' + self.__mouse_name,
                         'Channel 3': 'Channel 3 ' + self.__mouse_name}).to_csv(
                self.__destination_folder + "\\" + \
                str(region).replace('/', '-') + "_" + self.__mouse_name + ".csv", index=False)
