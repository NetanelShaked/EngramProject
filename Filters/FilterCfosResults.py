import math

import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
from skimage.filters import threshold_otsu as otsu
import multiprocessing
import numpy as np
import os
import cv2
from skimage.measure import label, regionprops

def exportPanelResults(image,csv):
    """

    :param image: image of bregma
    :param csv: DataFrame of this bregma
    :return: exoprt panel of all nucles found cfos positive in DataFrame
    """
    csv=pd.DataFrame(csv)
    numberOfNucles=len(csv)
    images=[]
    plt.figure(figsize=(100, 100))
    plotsize = int((numberOfNucles ** 0.5) + 1)
    for idx,row in csv.iterrows():
        x_pixel=int(row['x'])
        y_pixel=int(abs(row['y']))
        distance=200
        plt.subplot(plotsize, plotsize, idx + 1)
        plt.title(str(idx))
        plt.imshow(image[y_pixel - distance:y_pixel + distance,
                         x_pixel - distance:x_pixel + distance,1])
    plt.savefig("there3.jpg")

def someplayswithpic(jp2_path):
    pixel_to_mictoMeter = 0.203125
    x_pixel = 10753
    y_pixel = 6022
    distance = 200
    kernel = np.ones((5, 5), np.uint8)
    image_cfos_channel = plt.imread(jp2_path)[:, :, 1][y_pixel - distance:y_pixel + distance,
                         x_pixel - distance:x_pixel + distance]
    # image_cfos_channel[image_cfos_channel<image_cfos_channel.mean()+3*image_cfos_channel.std()]=0
    # image=cv2.morphologyEx(image_cfos_channel,cv2.MORPH_CLOSE,kernel)

    # plt.imshow(image_cfos_channel)
    # plt.show()
    threshold = image_cfos_channel.mean() + 4 * image_cfos_channel.std()
    image = image_cfos_channel > threshold
    plt.imshow(image)
    plt.show()
    image = cv2.morphologyEx(np.float32(image), cv2.MORPH_CLOSE, kernel)
    label_image = label(image)
    region = regionprops(label_image)
    plt.imshow(image_cfos_channel)
    # plt.imshow(image_cfos_channel)
    # plt.show()
    fig, ax = plt.subplots()
    ax.imshow(image, cmap=plt.cm.gray)

    for props in region:

        # area have to be bigger the 50 pixels - means bigger the 10 microns lines have eccentricity close to 1,
        # circle have eccentricity close to 0, nucleus isn't perfect circle so if the eccentricity is bigger the 0.95
        # be can pass extent is how much the area of the region take from all the box its belong to minor and major
        # axis len represent the long and short Radius, we looking for radius of 4~8 micron
        # note that each pixel is 0.2~ micron
        if props.area < 50 or props.eccentricity > 0.95 or props.extent < 0.3 or props.minor_axis_length < 10 or props.major_axis_length > 60:
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
    # plt.savefig("there2.jpg")
    plt.show()
    # plt.imsave("there.jpg",image_cfos_channel)


def checkPositiveCfos(image, x_coordinate, y_coordinate, distance):
    x_pixel = x_coordinate
    y_pixel = y_coordinate
    kernel = np.ones((5, 5), np.uint8)
    image_cfos_channel = image[y_pixel - distance:y_pixel + distance,
                         x_pixel - distance:x_pixel + distance, 1]

    threshold = image_cfos_channel.mean() + 4 * image_cfos_channel.std()
    image = image_cfos_channel > threshold
    # plt.imshow(image)
    # plt.show()
    image = cv2.morphologyEx(np.float32(image), cv2.MORPH_CLOSE, kernel)

    label_image = label(image)
    region = regionprops(label_image)

    # plt.imshow(image_cfos_channel)
    # plt.show()

    for props in region:

        # area have to be bigger the 50 pixels - means bigger the 10 microns lines have eccentricity close to 1,
        # circle have eccentricity close to 0, nucleus isn't perfect circle so if the eccentricity is bigger the 0.95
        # be can pass extent is how much the area of the region take from all the box its belong to minor and major
        # axis len represent the long and short Radius, we looking for radius of 4~8 micron
        # note that each pixel is 0.2~ micron
        if props.area < 50 or props.eccentricity > 0.95 or props.extent < 0.3 or props.minor_axis_length < 10 or props.major_axis_length > 60:
            continue
        if abs(props.centroid[0] - distance) < 10 and abs(props.centroid[1] - distance) < 10:
            return True, (props.area, props.minor_axis_length, props.major_axis_length)
    return False, ()


def bridgeForParallelize(data):
    df = pd.DataFrame(data[1])
    image = data[0]
    is_cFos_positive=[]
    region_prop=[]
    result=pd.DataFrame()
    for idx,row in df.iterrows():
        res=checkPositiveCfos(image, int(row['x']), int(abs(row['y'])), 200)
        is_cFos_positive.append(res[0])
        region_prop.append(res[1])
    result['relevent']=is_cFos_positive
    result['region_prop']=region_prop
    return result



def parallelize(data, image, func, num_of_processes=multiprocessing.cpu_count() - 1):
    data_split = np.array_split(data, num_of_processes)
    pool = multiprocessing.Pool(num_of_processes)
    data = pd.concat(pool.map(func, zip([image for i in range(num_of_processes)], data_split)))
    pool.close()
    pool.join()
    return data


def filterNuclesByCfos(path, jp2_name, csv_name):
    Image.MAX_IMAGE_PIXELS=10**9
    csv = pd.read_csv(os.path.join(path, csv_name))
    jp2_image = plt.imread(os.path.join(path, jp2_name))
    relevant = parallelize(csv, jp2_image,bridgeForParallelize)
    csv['relevent'] = relevant['relevent'].values
    csv['region_prop'] = relevant['region_prop'].values
    csv = csv[csv['relevent']]

    del csv['relevent']
    for region_prop in csv['region_prop'].unique():
        if len(csv[csv['region_prop']==region_prop])>1:
            print("found")
            one_res=csv[csv['region_prop']==region_prop].values[0]
            csv.drop(index=csv[csv['region_prop']==region_prop].index, inplace=True)
            csv=csv.append(one_res,ignore_index=True)
    del csv['region_prop']
    try:
        os.mkdir(os.path.join(path, "cfos_filtered"))
    except FileExistsError:
        pass

    csv.to_csv(os.path.join(os.path.join(path, "cfos_filtered"), csv_name), index=False)


if __name__ == '__main__':
    # Image.MAX_IMAGE_PIXELS = 10 ** 9
    # someplayswithpic(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-1255.jp2')
    Image.MAX_IMAGE_PIXELS=10**9
    image=plt.imread(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-1055.jp2')
    df=pd.read_csv(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\cfos_filtered\-1055.csv')
    exportPanelResults(image,df)
