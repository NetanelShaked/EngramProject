import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from skimage.filters import threshold_otsu as otsu
import multiprocessing
import numpy as np
import os


def apply_action_on_path(path):
    files_names = []
    walk_os = os.walk(path)
    for root, dirs, file in walk_os:
        files_names = file

    files_names = [i for i in filter(lambda file_name: '.csv' in file_name, files_names)]
    for file in files_names:
        file_name = file[:-4]
        print(file_name)
        filter_by_background(path, file_name + ".jp2", file_name + ".csv")


def parallelize(data, image, func, num_of_processes=multiprocessing.cpu_count() - 1):
    # image_shared=manger.Namespace()
    # image_shared.data=image
    data_split = np.array_split(data, num_of_processes)
    pool = multiprocessing.Pool(num_of_processes)
    data = pd.concat(pool.map(func, zip([image for i in range(num_of_processes)], data_split)))
    pool.close()
    pool.join()
    return data


def handle_df(data):
    image = data[0]
    df = data[1]
    return df.T.apply(lambda row: decision(image, int(row['x']), int(abs(row['y'])), 200))




def filter_by_background(path, jp2_name, csv_name, channel=None):
    Image.MAX_IMAGE_PIXELS = 10 ** 9
    image = plt.imread(path + "//" + jp2_name)
    csv = pd.read_csv(path + "//" + csv_name)
    csv['relevant'] = parallelize(csv, image, handle_df)
    # relevent = csv.T.apply(lambda row: decision(image, int(row['x']), int(abs(row['y'])), 500))
    # csv['relevant'] = relevent
    csv = csv[csv['relevant']]
    del csv['relevant']
    csv.to_csv(path + "//" + csv_name[:-4] + "_new.csv", index=False)


def decision(image, x_coordinate, y_coordinate, distance):
    channel = 0
    local_image_matrix = image[y_coordinate - distance:y_coordinate + distance,
                         x_coordinate - distance:x_coordinate + distance]
    local_image_matrix_one_channel = local_image_matrix[:, :, channel]
    limit = otsu(local_image_matrix_one_channel)
    pixel_value = image[y_coordinate, x_coordinate]
    if pixel_value[channel] >= limit:
        # need to expend with more checks
        # print(pixel_value)
        return True
    else:
        local_image_cfos = local_image_matrix[:, :, 1]
        mean = local_image_cfos.mean()
        std = local_image_cfos.std()
        if pixel_value[1] > mean + 2 * std:
            return True
        return False


if __name__ == '__main__':
    # path = r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files'
    # jp2 = '-3055.jp2'
    # csv = '-3055.csv'
    # filter_by_background(path, jp2, csv)
    apply_action_on_path(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files')
