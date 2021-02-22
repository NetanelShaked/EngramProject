import math

import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from skimage.filters import threshold_otsu as otsu
import multiprocessing
import numpy as np
import os
import cv2
from skimage.filters import threshold_otsu as otsu
from skimage.measure import label, regionprops
import matplotlib.patches as ptc
from sklearn import utils



def exportPanelResults(image, csv):
    """

    :param image: image of bregma
    :param csv: DataFrame of this bregma
    :return: exoprt panel of all nucles found cfos positive in DataFrame
    """
    csv = pd.DataFrame(csv)
    numberOfNucles = len(csv)
    images = []
    plt.figure(figsize=(200, 200))
    plotsize = int((numberOfNucles ** 0.5) + 1)
    distance = 300
    for idx, row in csv.iterrows():
        x_pixel = int(row['x'])
        y_pixel = int(abs(row['y']))
        plt.subplot(plotsize, plotsize, idx + 1)
        plt.title(str(x_pixel) + " , " + str(y_pixel))
        # plt.title(str(x_pixel) + " , " + str(y_pixel)+" region : "+str(row['region']))
        plt.imshow(image[y_pixel - distance:y_pixel + distance,
                   x_pixel - distance:x_pixel + distance,0])
        ax = plt.gca()
        rect = ptc.Rectangle((distance - 10, distance - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
    plt.savefig("filtereNeuN-1255_2.jpg")


def someplayswithpic(jp2_path):
    """
    This function create for some test and manual definitions for some experience
    :param jp2_path: path for jp2 file
    :return: None
    """
    pixel_to_mictoMeter = 0.203125  # For calculate real nucleus area
    x_pixel = 6110
    y_pixel = 4739
    distance = 200
    kernel = np.ones((5, 5), np.uint8)
    image_cfos_channel = plt.imread(jp2_path)[:, :, 1][y_pixel - distance:y_pixel + distance,
                         x_pixel - distance:x_pixel + distance]
    threshold = otsu(image_cfos_channel)
    # threshold = image_cfos_channel.mean() + 1 * image_cfos_channel.std()
    image = image_cfos_channel >= threshold
    plt.imshow(image)
    plt.show()
    image = cv2.morphologyEx(np.float32(image), cv2.MORPH_CLOSE, kernel)
    label_image = label(image)
    region = regionprops(label_image)

    x,y=image.shape
    plt.imshow(image_cfos_channel, extent=(0,x*pixel_to_mictoMeter,0,y*pixel_to_mictoMeter))
    fig, ax = plt.subplots()
    ax.imshow(image, cmap=plt.cm.gray)

    for props in region:

        # area have to be bigger the 50 pixels - means bigger the 10 microns lines have eccentricity close to 1,
        # circle have eccentricity close to 0, nucleus isn't perfect circle so if the eccentricity is bigger the 0.95
        # be can pass extent is how much the area of the region take from all the box its belong to minor and major
        # axis len represent the long and short Radius, we looking for radius of 4~8 micron
        # note that each pixel is 0.2~ micron
        if props.area < 50 or props.eccentricity > 0.9 or props.extent < 0.3 or props.minor_axis_length < 5 or props.major_axis_length > 30:
            continue
        print("extent is : " + str(props.extent))
        print("minor axis len is : " + str(props.minor_axis_length))
        print("coordinates is : " + str(props.centroid))
        y0, x0 = props.centroid
        orientation = props.orientation
        x1 = x0 + math.cos(orientation) * 0.5 * props.minor_axis_length
        y1 = y0 - math.sin(orientation) * 0.5 * props.minor_axis_length
        x2 = x0 - math.sin(orientation) * 0.5 * props.major_axis_length
        y2 = y0 - math.cos(orientation) * 0.5 * props.major_axis_length

        ax.plot((x0, x1), (y0, y1), '-r', linewidth=0.5)
        ax.plot((x0, x2), (y0, y2), '-r', linewidth=0.5)
        ax.plot(x0, y0, '.g', markersize=5)

        minr, minc, maxr, maxc = props.bbox
        bx = (minc, maxc, maxc, minc, minc)
        by = (minr, minr, maxr, maxr, minr)
        ax.plot(bx, by, '-b', linewidth=0.5)

    ax.axis((0, 400, 400, 0))
    plt.show()


def checkPositiveCfos(image, x_coordinate, y_coordinate, distance):
    """

    :param image: image as numpy array
    :param x_coordinate: x coordinate of nucleus interest
    :param y_coordinate: y coordinate of nucleus interest
    :param distance: distance for local image for micro analyze
    :return: True and tuple of region area props if there is cfos positive, else : False and empty tuple
    """
    x_pixel = x_coordinate
    y_pixel = y_coordinate
    kernel = np.ones((5, 5), np.uint8)
    image_cfos_channel = image[y_pixel - distance:y_pixel + distance,
                         x_pixel - distance:x_pixel + distance, 1]

    # threshold = image_cfos_channel.mean() + 4 * image_cfos_channel.std()
    threshold = otsu(image_cfos_channel)

    image = image_cfos_channel > threshold
    image = cv2.morphologyEx(np.float32(image), cv2.MORPH_CLOSE, kernel)

    label_image = label(image)
    region = regionprops(label_image)
    for props in region:

        # area have to be bigger the 50 pixels - means bigger the 10 microns lines have eccentricity close to 1,
        # circle have eccentricity close to 0, nucleus isn't perfect circle so if the eccentricity is bigger the 0.95
        # be can pass extent is how much the area of the region take from all the box its belong to minor and major
        # axis len represent the long and short Radius, we looking for radius of 4~8 micron
        # note that each pixel is 0.2~ micron

        if props.area < 50 or props.eccentricity > 0.9 or props.extent < 0.3 or props.minor_axis_length < 5 or props.major_axis_length > 50:
            continue
        if abs(props.centroid[0] - distance) < 10 and abs(props.centroid[1] - distance) < 10:
            return True, (props.area, props.minor_axis_length, props.major_axis_length)
    return False, ()


def bridgeForParallelize(data):
    """

    :param data: tuple: first object is image numpy matrix, the other one is panda DataFrame contain list of nucleus
    :return:
    """
    df = pd.DataFrame(data[1])
    image = data[0]
    is_cFos_positive = []
    region_prop = []
    result = pd.DataFrame()
    for idx, row in df.iterrows():
        res = checkPositiveCfos(image, int(row['x']), int(abs(row['y'])), 800)
        is_cFos_positive.append(res[0])
        region_prop.append(res[1])
    result['relevent'] = is_cFos_positive
    result['region_prop'] = region_prop
    return result


def parallelize(data, image_as_array, func, num_of_processes=multiprocessing.cpu_count() - 1):
    data_split = np.array_split(data, num_of_processes)
    pool = multiprocessing.Pool(num_of_processes)
    data = pd.concat(pool.map(func, zip([image_as_array for i in range(num_of_processes)], data_split)))
    pool.close()
    pool.join()
    return data


def filter_nucleus_by_cfos(path, jp2_name, csv_name):
    """

    :param path: path to jp2 and csv files
    :param jp2_name: name of image
    :param csv_name: name of csv file
    :return: create new csv file in folder "cfos_filtered" for each bregma sent to this function
    """
    Image.MAX_IMAGE_PIXELS = 10 ** 9
    csv = pd.read_csv(os.path.join(path, csv_name))
    jp2_image = plt.imread(os.path.join(path, jp2_name))
    relevant = parallelize(csv, jp2_image, bridgeForParallelize)
    csv['relevent'] = relevant['relevent'].values
    csv['region_prop'] = relevant['region_prop'].values
    csv = csv[csv['relevent']]

    del csv['relevent']

    for region_prop in csv['region_prop'].unique():
        if len(csv[csv['region_prop'] == region_prop]) > 1:
            print("found")
            # one_res=csv[csv['region_prop']==region_prop].values[0]
            csv.drop(index=csv[csv['region_prop'] == region_prop].index[1:], inplace=True)
            # csv=csv.append(one_res,ignore_index=True)
    del csv['region_prop']
    try:
        os.mkdir(os.path.join(path, "cfos_filtered"))
    except FileExistsError:
        pass

    csv.to_csv(os.path.join(os.path.join(path, "cfos_filtered"), csv_name), index=False)


if __name__ == '__main__':
    # Image.MAX_IMAGE_PIXELS = 10 ** 9
    # someplayswithpic(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-2855.jp2')

    Image.MAX_IMAGE_PIXELS = 10 ** 9
    image = plt.imread(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-1255.jp2')

    df = pd.DataFrame(utils.shuffle(pd.read_csv(
        r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\NeunFilter\-1255_try.csv'))).reset_index().iloc[:2000]

    # df = pd.DataFrame(utils.shuffle(pd.read_csv(
    # r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\cfos_filtered\-2655_try1.csv'))).reset_index()
    exportPanelResults(image, df)
    # filter_nucleus_by_cfos(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files','-2655.jp2','-2655_try1.csv')