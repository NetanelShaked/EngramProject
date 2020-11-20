import pandas as pn
import os


class Drop_Distrebutions:
    def __init__(self, path, main_file_name, delete_points_file):
        self.__path = path
        self.__file_name = main_file_name
        self.__delete_file = delete_points_file

    def drop(self):
        main_df = pn.read_csv(self.__path + "\\" + self.__file_name, skiprows=1)
        delete_file = pn.read_csv(self.__path + "\\" + self.__delete_file)
        for index, row in delete_file.iterrows():
            main_df.drop(
                main_df[(main_df['z'] == row['z']) & (main_df['x'] == row['x']) & (main_df['y'] == row['y'])].index,
                inplace=True)
        main_df.to_csv(self.__path + "\\" + self.__file_name[:-4] + "_after_delete.csv", index=False)

    def drop_by_folder(self, folder_path):
        to_detete = pn.read_csv(self.__path + "\\" + self.__delete_file)
        walk_os = os.walk(folder_path)
        change = False
        files_names = []
        for root, dirs, file in walk_os:
            files_names = file

        files_names = [i for i in filter(lambda file_name: '.csv' in file_name, files_names)]
        for file in files_names:
            bregma = file.split('_')[0]
            bregma = bregma.split('.')[0]
            bregma_csv = pn.read_csv(folder_path + "\\" + file)
            for index, row in to_detete[to_detete['z'] == int(bregma)].iterrows():
                bregma_csv.drop(bregma_csv[(bregma_csv['x'] == row['x']) & (bregma_csv['y'] == row['y'])].index,
                                inplace=True)
                change = True
            if change:
                bregma_csv.to_csv(folder_path + "\\" + file[:-4] + "_new.csv", index=False)

            change = False


        # bregma_df={}
        # to_detete=pn.read_csv(self.__path+"\\"+self.__delete_file)
        # for bregma in to_detete['Unnamed: 0'].unique():
        #     bregma_df[bregma]=pn.read_csv(folder_path+"\\"+bregma+".csv")
