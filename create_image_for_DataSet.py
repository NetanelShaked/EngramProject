import pandas as pn
import matplotlib.pyplot as plt
import matplotlib.patches as ptc
import os
from PIL import Image
import sklearn.utils
from skimage.feature import blob_log
from math import sqrt
from skimage.color import rgb2gray
from scipy.spatial import distance


class create_images_for_DataSet:
    def __init__(self, path):
        self.__path = path

    def action(self):
        def act(file_name):
            try:
                os.mkdir(self.__path + "\\" + file_name[:-4])
            except FileExistsError:
                None
            try:
                os.mkdir(self.__path + "\\" + file_name[:-4] + "\\positive")
            except FileExistsError:
                None
            try:
                os.mkdir(self.__path + "\\" + file_name[:-4] + "\\negative")
            except FileExistsError:
                None

            data = pn.read_csv(self.__path + "\\" + file_name)
            image = plt.imread(self.__path + "\\" + file_name[:-4] + ".jp2")
            d = 20
            median = data['Channel 3'].median()
            std = data['Channel 3'].std()
            data = sklearn.utils.shuffle(data)
            data = data.head(min(len(data), 1000))
            verify = False
            for index, row in data.iterrows():
                verify = False
                cell_channels_images = image[abs(int(row['y'])) - d:abs(int(row['y'])) + d,
                                       abs(int(row['x'])) - d:int(row['x']) + d,
                                       :]
                cell_image = cell_channels_images[:, :, 1]
                gray_cell_image = rgb2gray(cell_image)
                blob_log_list = blob_log(gray_cell_image, max_sigma=8, min_sigma=2,
                                         threshold=.03)
                blob_log_list[:, 2] = blob_log_list[:, 2] * sqrt(2)
                for blob in blob_log_list:
                    x, y, r = blob
                    if distance.euclidean([d, d], [x, y]) <= r:
                        # or (25 >= x >= 15 and 25 >= y >= 15)
                        verify = True
                        break

                plt.clf()
                fig = plt.figure(figsize=(20, 20))
                plt.subplot(131)
                plt.title("C-fos")
                plt.imshow(cell_channels_images[:, :, 1])
                plt.gca().add_patch(
                    ptc.Rectangle((15, 15), 10, 10, linewidth=1, edgecolor='r', facecolor='none'))
                plt.subplot(132)
                plt.title("NeuN")
                plt.imshow(cell_channels_images[:, :, 0])
                plt.gca().add_patch(
                    ptc.Rectangle((15, 15), 10, 10, linewidth=1, edgecolor='r', facecolor='none'))
                plt.subplot(133)
                plt.title("Dapi")
                plt.imshow(cell_channels_images[:, :, 2])
                plt.gca().add_patch(
                    ptc.Rectangle((15, 15), 10, 10, linewidth=1, edgecolor='r', facecolor='none'))
                if (verify):
                    plt.savefig(self.__path + "\\" + file_name[:-4] + "\\positive\\" + str(
                        index) + ".jpg")
                else:
                    plt.savefig(self.__path + "\\" + file_name[:-4] + "\\negative\\" + str(
                        index) + ".jpg")
                plt.close(fig)

        Image.MAX_IMAGE_PIXELS = 10 ** 10
        walkFiles = os.walk(self.__path)
        filesNames = []
        for root, dirs, file in walkFiles:
            filesNames = file

        filesNames = [file for file in filter(lambda f: '.csv' in f, filesNames)]
        for file in filesNames:
            act(file)



