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


def exportPanelResults(image_path, csv_path, channel, distance=500, img_name=None, number_of_examples=None,
                       drow_treangle=True):
    """

    :param number_of_examples: how much images include in pannel
    :param image_path: path to image of specific bregma
    :param csv_path: path to csv file (DataFrame)
    :param channel: which channel focus on
    :param distance: how much pixels to take in each side from the coordinates taken from DataFrame
    :return: exoprt panel of all nucles found positive by the selected channel in DataFrame
    """

    Image.MAX_IMAGE_PIXELS = 10 ** 9

    csv = pd.read_csv(csv_path)
    image = plt.imread(image_path)

    if number_of_examples is None:
        number_of_examples = len(csv)
    pixel_to_mictoMeter = 0.203125  # For calculate real nucleus area
    csv = utils.shuffle(csv).reset_index().iloc[:number_of_examples]
    numberOfNucles = number_of_examples
    plt.figure(figsize=(200, 200))
    plotsize = int((numberOfNucles ** 0.5) + 1)
    for idx, row in csv.iterrows():
        x_pixel = int(row['x'])
        y_pixel = int(abs(row['y']))
        plt.subplot(plotsize, plotsize, idx + 1)
        plt.title(
            str(x_pixel) + "," + str(y_pixel) + " min " + "{:.2f}".format(int(row['minor radius'])*pixel_to_mictoMeter) + " max " + "{:.2f}".format(
                int(row['major radius'])*pixel_to_mictoMeter))
        # plt.title(str(x_pixel) + " , " + str(y_pixel)+" region : "+str(row['region']))
        plt.imshow(image[y_pixel - distance:y_pixel + distance,
                   x_pixel - distance:x_pixel + distance, channel])
        if drow_treangle:
            ax = plt.gca()
            rect = ptc.Rectangle((distance - 20, distance - 20), 40, 40, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
    plt.tight_layout()
    if img_name is None:
        img_name = csv_path.split('/')[-1][:-4]
    plt.savefig(img_name)


def export3ChannelsPanelResults(image_path, csv_path, distance=500, img_name=None, number_of_examples=None):
    """

    :param number_of_examples: how much images include in pannel :param image_path: path to image of specific bregma
    :param csv_path: path to csv file (DataFrame) :param channel: which channel focus on :param distance: how much
    pixels to take in each side from the coordinates taken from DataFrame :return: exoprt panel of all nucles found
    positive by the selected channel in DataFrame """

    Image.MAX_IMAGE_PIXELS = 10 ** 9

    csv = pd.read_csv(csv_path)
    image = plt.imread(image_path)

    if number_of_examples is None:
        number_of_examples = len(csv)

    csv = utils.shuffle(csv).reset_index().iloc[:number_of_examples]
    plt.figure(figsize=(25, min(5 * number_of_examples, (2 ** 16) / 100) - 1))
    for idx, row in csv.iterrows():
        x_pixel = int(row['x'])
        y_pixel = int(abs(row['y']))
        plt.subplot(number_of_examples, 4, 4 * idx + 1)
        plt.title(str(x_pixel) + " , " + str(y_pixel) + " Neun")
        # plt.title(str(x_pixel) + " , " + str(y_pixel)+" region : "+str(row['region']))
        plt.imshow(image[y_pixel - distance:y_pixel + distance,
                   x_pixel - distance:x_pixel + distance, 0])
        ax = plt.gca()
        rect = ptc.Rectangle((distance - 20, distance - 20), 40, 40, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        plt.subplot(number_of_examples, 4, 4 * idx + 2)
        plt.title(str(x_pixel) + " , " + str(y_pixel) + " C-fos")
        plt.imshow(image[y_pixel - distance:y_pixel + distance,
                   x_pixel - distance:x_pixel + distance, 1])
        ax = plt.gca()
        rect = ptc.Rectangle((distance - 20, distance - 20), 40, 40, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        plt.subplot(number_of_examples, 4, 4 * idx + 3)
        plt.title(str(x_pixel) + " , " + str(y_pixel) + " Dapi")
        plt.imshow(image[y_pixel - distance:y_pixel + distance,
                   x_pixel - distance:x_pixel + distance, 2])
        ax = plt.gca()
        rect = ptc.Rectangle((distance - 20, distance - 20), 40, 40, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

        plt.subplot(number_of_examples, 4, 4 * idx + 4)
        plt.title(" region : " + str(row['region']))
        plt.imshow(image[y_pixel - 3 * distance:y_pixel + 3 * distance,
                   x_pixel - 3 * distance:x_pixel + 3 * distance])
        ax = plt.gca()
        rect = ptc.Rectangle((3 * distance - 20, 3 * distance - 20), 40, 40, linewidth=1, edgecolor='r',
                             facecolor='none')
        ax.add_patch(rect)
    if img_name is None:
        img_name = csv_path.split('\\')[-1][:-4]
    plt.savefig(img_name)
