import pandas as pn


class separate_dorsal_ventral_hippocmapus:
    def __init__(self, path, file_name):
        self.__path = path
        self.__file_name = file_name

    def action(self, bregma_separate):
        """

        :param bregma_separate: the bregma value of the first ventral bregma
        :return: export 2 csv file , ventral and dorsal
        """
        df = pn.read_csv(self.__path + "\\" + self.__file_name)
        write=pn.ExcelWriter(self.__path+"\\"+self.__file_name[:-4]+"_seaparate.xlsx")
        # df[df['z'] <= bregma_separate].to_csv(self.__path + "\\" + self.__file_name + "_ventral.csv", index=False)
        df[df['z'] <= bregma_separate].to_excel(write, sheet_name='Ventral', index=False)
        # df[df['z'] > bregma_separate].to_csv(self.__path + "\\" + self.__file_name + "_dorsal.csv", index=False)
        df[df['z'] > bregma_separate].to_excel(write,sheet_name='Dorsal', index=False)
        write.save()