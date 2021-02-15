import pandas as pn
import threading
import os

"""
This class using for separate the csv_points file, each bregma get own file
"""


class separatePointCSVfile:
    """
    This class using for separate the csv_points file, each bregma get own file
    \nInitialize :
    \npath: get the csv folder diraction
    \nfile_name: get the csv file name (with extension)
    \n\n
    for action use separate method.
    """

    def __init__(self, path, file_name=""):
        self.__path = path
        self.file_name = file_name

    def merge(self):
        """

        :return: merge all csv's files to one
        """
        files_names = []
        walk_os = os.walk(self.__path)
        for root, dirs, file in walk_os:
            files_names = file

        files_names = [pn.read_csv(self.__path + "\\" + i) for i in
                       filter(lambda file_name: '.csv' in file_name, files_names)]
        pn.concat(files_names).to_csv(self.__path + "\\points.csv", index=False)

    def separate(self, NeuN_limits_file=None):
        """
        :return: All bregma's List
        """

        def separate_action(originalCSV, bregma, neun_limit):
            df = pn.DataFrame(originalCSV).copy()
            df = df[df['z'] == bregma]
            dff = df[df['Channel 2'] <= neun_limit]
            df = df[df['Channel 2'] > neun_limit]
            print(neun_limit)
            df.to_csv(self.__path + "\\separate files\\" + str(bregma) + '.csv', index=False)
            dff.to_csv(self.__path + "\\separate files lower neun\\" + str(bregma) + '.csv', index=False)

        bregma_limits = {}

        if not NeuN_limits_file is None:
            df_neun_limits = pn.read_csv(self.__path + "\\" + NeuN_limits_file)
            for bregma in df_neun_limits['z'].unique():
                bregma_limits[bregma] = max(df_neun_limits[df_neun_limits['z'] == bregma]['Channel 2'])

        originalCSV = pn.read_csv(self.__path + "\\" + self.file_name)
        originalCSV = originalCSV[originalCSV['id name'] != '??']
        # bregma1 = originalCSV[originalCSV['z'] == 85]
        print(originalCSV.columns)
        allBregmas = originalCSV['z'].unique()
        try:
            os.mkdir(self.__path + "\\separate files")
        except FileExistsError:
            None
        try:
            os.mkdir(self.__path + "\\separate files lower neun")
        except FileExistsError:
            None
        finally:
            for bregma in allBregmas:
                t = threading.Thread(target=separate_action,
                                     args=[originalCSV, int(bregma), bregma_limits.get(int(bregma), 0)])
                t.start()

        return allBregmas

    def separate_2(self, NeuN_limits_file=None):
        """
        :return: All bregma's List
        """

        def separate_action(originalCSV, bregma, neun_limit):
            df = pn.DataFrame(originalCSV).copy()
            df = df[df['z'] == bregma]
            dff = df[df['Channel 2'] <= neun_limit]
            df = df[df['Channel 2'] > neun_limit]
            df['Channel 3'] = df['Channel 3']
            # print(neun_limit)
            df.to_csv(self.__path + "\\separate files\\" + str(bregma) + '.csv', index=False)
            dff.to_csv(self.__path + "\\separate files lower neun\\" + str(bregma) + '.csv', index=False)
            print(str(bregma) + " : " + str(len(df) / len(df + dff)))

        bregma_limit = 0

        if not NeuN_limits_file is None:
            df_neun_limits = pn.read_csv(self.__path + "\\" + NeuN_limits_file)
            for bregma in df_neun_limits['z'].unique():
                bregma_limit += df_neun_limits[df_neun_limits['z'] == bregma]['Channel 2'].mean() + \
                                4 * df_neun_limits[df_neun_limits['z'] == bregma]['Channel 2'].std()
                # bregma_limits[bregma] = df_neun_limits[df_neun_limits['z'] == bregma]['Channel 2'].max()
        bregma_limit = int((bregma_limit / len(df_neun_limits['z'].unique())) + 0.5)

        originalCSV = pn.read_csv(self.__path + "\\" + self.file_name)
        originalCSV = originalCSV[originalCSV['id name'] != '??']
        # bregma1 = originalCSV[originalCSV['z'] == 85]
        print(originalCSV.columns)
        allBregmas = originalCSV['z'].unique()
        try:
            os.mkdir(self.__path + "\\separate files")
        except FileExistsError:
            None
        try:
            os.mkdir(self.__path + "\\separate files lower neun")
        except FileExistsError:
            None
        finally:
            print(bregma_limit)
            for bregma in allBregmas:
                t = threading.Thread(target=separate_action,
                                     args=[originalCSV, int(bregma), bregma_limit])
                t.start()

        return allBregmas
