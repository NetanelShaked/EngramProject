import pandas as pn


class One_Side:
    def __init__(self, path):
        self.__path = path

    def action(self, files, left__or_right):
        """
        DO NOT FORGET  to get the right side you have to choose the left side from the output of NeuroInfo! \n

        :param files: list of files name
        :param left__or_right: 1- left , 2- right
        :return: Creating new csv file contain only the chosen hemisphere
        """
        for file in files:
            data = pn.read_csv(self.__path + "\\" + file)
            if (left__or_right == 1):
                data[data['hemisphere'] == 'left'].to_csv(self.__path + "\\" + file[:-4] + "_left.csv", index=False)
            else:
                data[data['hemisphere'] == 'right'].to_csv(self.__path + "\\" + file[:-4] + "_right.csv", index=False)
