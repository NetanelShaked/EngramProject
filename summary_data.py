import pandas as pn
import os


class Summary_Data:
    def __init__(self, path, destination):
        self.__destination = destination
        self.__path = path

    def action(self):
        regions_dict = {}
        walkFiles = os.walk(self.__path)
        for root, dirs, file in walkFiles:
            files_names = file
        for file in files_names:
            file_name = file.split('_')[0]
            if file_name not in regions_dict:
                regions_dict[file_name] = []
            regions_dict[file_name].append(file)

        df_list = []

        for key in regions_dict.keys():
            for i in regions_dict[key]:
                df = pn.read_csv(self.__path + "\\" + i, usecols=[1, 2])
                df['Ratio_' + str(i).split('_')[1][:-4]] = df[df.columns[1]] / df[df.columns[0]]
                df_list.append(df)

            product_csv = df_list[0]
            for i in range(1, len(regions_dict[key])):
                product_csv = pn.merge(product_csv, df_list[i], left_index=True, right_index=True, how='outer')

            product_csv.to_csv(self.__destination + "\\" + key + ".csv", index=False)
            df_list = []
