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

def someplayswithpic(jp2_path):
    pixel_to_mictoMeter=0.203125
    x_pixel = 6571
    y_pixel = 7945
    distance = 200
    kernel = np.ones((5, 5), np.uint8)
    image_cfos_channel=plt.imread(jp2_path)[:,:,1][y_pixel - distance:y_pixel + distance, x_pixel - distance:x_pixel + distance]
    # image_cfos_channel[image_cfos_channel<image_cfos_channel.mean()+3*image_cfos_channel.std()]=0
    # image=cv2.morphologyEx(image_cfos_channel,cv2.MORPH_CLOSE,kernel)

    # plt.imshow(image_cfos_channel)
    # plt.show()
    image=image_cfos_channel>image_cfos_channel.mean()+3*image_cfos_channel.std()
    image = cv2.morphologyEx(np.float32(image), cv2.MORPH_CLOSE, kernel)
    label_image=label(image)
    region=regionprops(label_image)
    # plt.imshow(image_cfos_channel)
    # plt.show()
    fig, ax = plt.subplots()
    ax.imshow(image, cmap=plt.cm.gray)

    for props in region:
        if props.area<50 or props.eccentricity>0.95 or props.extent<0.3 or props.minor_axis_length<10:
            continue
        print(props.extent)
        print(props.minor_axis_length)
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

if __name__ == '__main__':
    Image.MAX_IMAGE_PIXELS=10**9
    someplayswithpic(r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-2855.jp2')

