import matplotlib.pyplot as plt
import matplotlib.patches as ptc
from PIL import Image
from math import sqrt
from skimage.feature import blob_log
from skimage.color import rgb2gray
import pandas as pn
from scipy.spatial import distance
from os import mkdir


class filterCellByBlobDetection:
    def __init__(self, path, image_file_name, data_file_name):
        self.__data_file_name = data_file_name
        self.__image_file_name = image_file_name
        self.__path = path

    def action(self, export_images=False):
        """

        :param export_images: True for export detected and undetected images
        :return: csv file contain all the cell's are c-fos positive for given bregma
        """
        if export_images:
            try:
                mkdir(self.__path + "\\blob_filter_" + self.__data_file_name[:-4])
            except FileExistsError:
                None
            try:
                mkdir(self.__path + "\\blob_filter_not_found_" + self.__data_file_name[:-4])
            except FileExistsError:
                None

        Image.MAX_IMAGE_PIXELS = 275727232
        count_verify = 0

        image = plt.imread(self.__path + "\\" + self.__image_file_name)
        data = pn.read_csv(self.__path + "\\" + self.__data_file_name)
        mean_channel_3 = data['Channel 3'].mean()

        # data = data[data['id name'] == 'Field CA1']

        d = 20  # Represnting the pixels for each side
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

            if len(blob_log_list) == 0:
                data.drop(index, inplace=True)
                continue

            for blob in blob_log_list:
                x, y, r = blob
                if distance.euclidean([d, d], [x, y]) <= r:
                    # or (25 >= x >= 15 and 25 >= y >= 15)
                    verify = True
                    break
            if not verify:
                data.drop(index, inplace=True)
                if row['Channel 3'] > mean_channel_3:
                    if export_images:
                        plt.clf()
                        fig = plt.figure(figsize=(20, 20))
                        plt.subplot(131)
                        plt.title("C-fos")
                        plt.imshow(cell_image)
                        for blob in blob_log_list:
                            y, x, r = blob
                            # print("X: " + str(x) + " Y: " + str(y) + " R: " + str(r))
                            c = plt.Circle((x, y), r, color="Yellow", linewidth=1, fill=False)
                            plt.gca().add_patch(c)
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
                        plt.savefig(self.__path + "\\blob_filter_not_found_" + self.__data_file_name[:-4] + "\\" + str(
                            index) + ".jpg")
                        plt.close(fig)
            if verify:
                count_verify += 1
                if export_images:
                    fig = plt.figure(figsize=(20, 20))
                    plt.subplot(131)
                    plt.title("C-fos")
                    plt.imshow(cell_image)
                    plt.subplot(132)
                    plt.title("Dapi")
                    plt.imshow(cell_channels_images[:, :, 2])
                    plt.savefig(
                        self.__path + "\\blob_filter_" + self.__data_file_name[:-4] + "\\" + str(index) + ".jpg")
        data.to_csv(self.__path + "\\" + self.__data_file_name[:-4] + "filtered.csv", index=False)
        print(count_verify)
