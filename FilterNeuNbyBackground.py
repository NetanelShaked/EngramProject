import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from skimage.filters import threshold_otsu as otsu
import multiprocessing
import numpy as np


def parallelize(data, func, num_of_processes=multiprocessing.cpu_count()-1):
    data_split = np.array_split(data, num_of_processes)
    pool = multiprocessing.Pool(num_of_processes)
    data = pd.concat(pool.map(func, data_split))
    pool.close()
    pool.join()
    return data

def filter_by_background(path, jp2_name, csv_name, channel=None):
    image = plt.imread(path + "//" + jp2_name)
    csv = pd.read_csv(path + "//" + csv_name)
    relevent = csv.T.parallel_apply(lambda row: decision(image, int(row['x']), int(abs(row['y'])), 500))
    csv['relevant'] = relevent
    print(csv[csv['relevant']].head())


def decision(image, x_coordinate, y_coordinate, distance):
    channel=0
    local_image_matrix = image[y_coordinate - distance:y_coordinate + distance,
                         x_coordinate - distance:x_coordinate + distance, channel]
    limit = otsu(local_image_matrix)
    image_value = image[y_coordinate, x_coordinate,channel]
    if image_value >= limit:
        # need to expend with more checks
        print(image_value)
        return True
    else:
        return False

if __name__ == '__main__':
    Image.MAX_IMAGE_PIXELS=10**9
    path=r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files'
    jp2='945.jp2'
    csv='945.csv'
    filter_by_background(path,jp2,csv)
