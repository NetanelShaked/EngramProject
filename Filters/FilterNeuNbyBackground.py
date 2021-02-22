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
        filter_NeuN_by_background(path, file_name + ".jp2", file_name + ".csv")


def parallelize(data, image, func, num_of_processes=multiprocessing.cpu_count() - 1):
    data_split = np.array_split(data, num_of_processes)
    # data_split = []
    #
    # for id in data['id'].unique():
    #     data_split.append(data[data['id'] == id])
    # print (str(len(data_split))+" regions found")
    pool = multiprocessing.Pool(num_of_processes)
    data = pd.concat(pool.map(func, zip([image for i in range(len(data_split))], data_split)))
    pool.close()
    pool.join()
    return data


def handle_df(data):
    """
    For using parallelize, each part of DF send to this function and apply decision function
    :param data: data[0] is image as numpy array and data [1] is pandas DataFrame contain info
    :return: DataFrame with True/False returned by decision function
    """
    image = data[0]
    df = data[1]
    return df.T.apply(lambda row: decision(image, int(row['x']), int(abs(row['y'])), 300))


def filter_NeuN_by_background(path, jp2_name, csv_name):
    """

    :param path: path to folder contain the image and DataFrame
    :param jp2_name: image file name
    :param csv_name: csv file name
    :return: create csv file for the csv file sent, contain only the NeuN positive nucleus.
    """
    Image.MAX_IMAGE_PIXELS = 10 ** 9
    image = plt.imread(path + "//" + jp2_name)
    csv = pd.read_csv(path + "//" + csv_name)

    interest_region = pd.read_csv(r'C:\Users\shako\Desktop\מעבדה\interest _regions.csv')
    interest_region = interest_region[interest_region['Relevant'] == 'x']
    interest_region = interest_region['id']

    csv = csv[csv['id'].isin(interest_region)]
    # new_csv = parallelize(csv, image, getmasho)
    csv['relevant'] = parallelize(csv, image, handle_df)
    # new_csv.to_csv(r'C:\Users\shako\Desktop\try1.csv', index=False)
    filtered_csv=csv[csv['relevant']==False]
    csv = csv[csv['relevant']]
    del csv['relevant']
    try:
        os.mkdir(os.path.join(path, "NeunFilter"))
    except FileExistsError:
        pass
    csv.to_csv(os.path.join(os.path.join(path, "NeunFilter"), csv_name[:-4] + "_try.csv"), index=False)
    filtered_csv.to_csv(os.path.join(os.path.join(path, "NeunFilter"), csv_name[:-4] + "_try_filtered.csv"), index=False)



def decision(image, x_coordinate, y_coordinate, distance):
    """

    :param image: image as numpy array
    :param x_coordinate: x coordinate of nucleus interest
    :param y_coordinate: y coordinate of nucleus interest
    :param distance: distance for local image for micro analyze
    :return:
    """
    channel = 0
    local_image_matrix = image[y_coordinate - distance:y_coordinate + distance,
                         x_coordinate - distance:x_coordinate + distance]
    local_image_matrix_one_channel = local_image_matrix[:, :, channel]
    limit = otsu(local_image_matrix_one_channel)
    std = local_image_matrix_one_channel.std()
    # print(limit,image[y_coordinate, x_coordinate],local_image_matrix.mean(),std)
    # std = 0
    neun_pixel_radius = 4
    # pixel_value = image[y_coordinate , x_coordinate,channel]
    pixel_value = image[y_coordinate - neun_pixel_radius:y_coordinate + neun_pixel_radius,
                  x_coordinate - neun_pixel_radius:x_coordinate + neun_pixel_radius, channel].mean()
    limit_addition=std

    if std < 1:  # in case there is no NeuN in local area
        return False

    if limit <= 10: # close to the end of the brain
        limit_addition *= 1.5

    threshold = limit + limit_addition

    if std < 4:  # low density in local image
        threshold = limit + 2 * limit_addition
    if std > 6.5:  # in case there is high density in local image
        threshold = limit + 0.5 * limit_addition
    if pixel_value >= threshold:
        return True
    else:
        # if pixel value is smaller then the background value calculate by otsu
        # we have to check if there is another reason to check this nucleus any way
        # we looking for c-fos so if cfos value (channel3) is bigger then mean+4*std of channel3 intensity
        # in local area we keep this coordinates

        # local_image_cfos = local_image_matrix[:, :, 1]
        # mean = local_image_cfos.mean()
        # std = local_image_cfos.std()
        # threshold = mean + 4 * std
        # if pixel_value[1] > threshold:
        #     return True
        return False


def getmasho(data):
    image, dataFrame, distance = data
    # dataFrame = pd.DataFrame(dataFrame[dataFrame['region'] == 'Hippocampal region'])
    # for row in interest_region.iterrows():
    threshold = dataFrame.T.apply(lambda row: otsu(image[int(abs(row['y'])) - distance:int(abs(row['y'])) + distance,
                                                   int(row['x']) - distance:int(row['x']) + distance, 0]))
    print(len(dataFrame))
    print(str(dataFrame['id name'].unique()) + " drop : " + str(
        len(dataFrame[dataFrame['Channel 2'] <= threshold.mean()])))

    return dataFrame[dataFrame['Channel 2'] > threshold.mean()]


if __name__ == '__main__':
    path = r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files'
    jp2 = '-1255.jp2'
    csv = '-1255.csv'
    Image.MAX_IMAGE_PIXELS = 10 ** 9
    filter_NeuN_by_background(path, jp2, csv)
    # image=plt.imread(os.path.join(path,jp2))
    # dataFrame=pd.read_csv(os.path.join(path,csv))
    # print (getmasho(image,dataFrame,500))
    # apply_action_on_path(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files')

    # interest_region=pd.read_csv(r'C:\Users\shako\Desktop\מעבדה\interest _regions.csv')
    # csv=pd.read_csv(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-2855.csv')
    # print(len(interest_region))
    # interest_region=interest_region[interest_region['Relevant']=='x']
    # interest_region=interest_region['id'].tolist()
    # print(len(interest_region))
    # print(len(csv))
    # print(len(csv[csv['id'].isin(interest_region)]))
