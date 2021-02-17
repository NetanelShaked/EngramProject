import imageio
from PIL import Image
import pandas as pd
import numpy as np

"""
    This class use after using 'separatePointCSVfile' and 'initCSVfiles'
    export csv file with average of intensity of cfos (red channel) 
"""


class CalculateCfosIntensity:
    """image and csv file should be in same folder

    \npath: the folder diraction - string
    \nimage_name: the jp2 name (with extension) - string
    \ncsv_name: same as image_name - csv file name with '.csv' extension - string
    """

    def __init__(self, path, image_name, csv_name):
        if type(path) != str or type(image_name) != str or type(csv_name) != str:
            raise TypeError("All the parameters have to be STRING  ")

        if not('csv' in csv_name and 'jp2' in image_name):
            raise ValueError("must get a csv file and jp2 file")

        self.__path = path
        self.__image_name = image_name
        self.__csv_name = csv_name

    def __getAverageSubMatrix(self, imageMatrix, yAxis, xAxis, distance):
        sub_matrix = imageMatrix[yAxis - distance:yAxis + distance + 1, xAxis - distance:xAxis + distance + 1, 0]
        return np.average(sub_matrix)

    def action(self, distance):
        """Action the object destiny, export csv_name + _final.csv FILE
         \ndistance: get the pixels number for calculate the average around DAPI pixel"""
        Image.MAX_IMAGE_PIXELS = 245589084
        # Load Section Image
        im = imageio.imread(self.__path + "\\" + self.__image_name)

        if im.shape[-1] == 4:
            raise ValueError(self.__image_name + " isn't in right format")

        sectionDF = pd.read_csv(self.__path + "\\" + self.__csv_name)
        print(sectionDF.columns)
        sectionDF.set_index('Unnamed: 0')

        intensity_single_pixel = []
        intensity_average = []

        for index, row in sectionDF.iterrows():
            intensity_single_pixel.append(im[np.abs(row['y'])][row['x']][0])
            intensity_average.append(self.__getAverageSubMatrix(im, np.abs(row['y']), row['x'], distance))

        sectionDF['intensity single pixel'] = intensity_single_pixel
        sectionDF['intensity average'] = intensity_average
        sectionDF['distance'] = np.asarray(intensity_single_pixel) - np.asarray(intensity_average)
        sectionDF.to_csv(self.__path + "\\" + self.__csv_name[:-4] + "_final.csv", index=False)
