import pandas as pn
import numpy as np
import matplotlib.pyplot as plt


class Cfos_Count:
    """
    This class using points with names file after filter cells by Channel 2 values \n
    and export a file by calculate median and standard deviation
    """

    def __init__(self, path, file_name):
        self.__path = path
        self.__file_name = file_name

    def action(self, std):
        """

        :return: export a file that contain only the cell thats bigger then median + the std parameter
        """
        data = pn.read_csv(self.__path + "\\" + self.__file_name)
        mean = data['Channel 3'].mean()
        median = data['Channel 3'].median()
        std_calc = data['Channel 3'].std()
        print("Median: ", median)
        print("Mean: ", mean)
        print("Std: ", std_calc)
        print (min(data['Channel 2']))
        data[data['Channel 3'] >= median + std_calc * std].to_csv(
            self.__path + "\\" + self.__file_name[:-4] + "_" + str(std) + " std.csv", index=False)

        plt.title("Channel 3 - all Data Histogram")
        plt.hist(data['Channel 3'], bins=100)
        numbers = [x for x in range(0, 101, 5)]
        labels = map(lambda x: str(x), numbers)
        plt.xticks(numbers, labels)
        plt.xlabel("intensity")
        plt.ylabel("frequency")
        plt.xlim(0, 100)
        # plt.axvline(median, color='k', ls='--')
        plt.axvline(mean, color='r', ls='--')
        plt.axvline(mean+std*std_calc, color='k', ls='--')
        plt.show()


    def action_2(self, std):
        """

        :return: export a file that contain only the cell thats bigger then median + the std parameter
        """
        data = pn.read_csv(self.__path + "\\" + self.__file_name)
        mean = data['Channel 3'].mean()
        median = data['Channel 3'].median()
        std_calc = data['Channel 3'].std()
        print("Median: ", median)
        print("Mean: ", mean)
        print("Std: ", std_calc)
        print (str(std)+"*"+str(std_calc)+"+"+str(mean)+"="+str(mean + std_calc * std))
        data[data['Channel 3'] >= mean + std_calc * std].to_csv(
            self.__path + "\\" + self.__file_name[:-4] + "_" + str(std) + " std.csv", index=False)

        plt.title("Channel 3 - all Data Histogram")
        plt.hist(data['Channel 3'], bins=100)
        numbers = [x for x in range(0, 3, 1)]
        labels = map(lambda x: str(x), numbers)
        plt.xticks(numbers, labels)
        plt.xlabel("intensity")
        plt.ylabel("frequency")
        plt.xlim(0, 3)
        # plt.axvline(median, color='k', ls='--')
        plt.axvline(mean, color='r', ls='--')
        plt.axvline(mean+std*std_calc, color='k', ls='--')
        plt.show()
