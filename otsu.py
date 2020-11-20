from skimage import filters
from skimage import exposure
from PIL import Image
import pandas as pn
import os

Image.MAX_IMAGE_PIXELS = Image.MAX_IMAGE_PIXELS = 245589084
from matplotlib import pyplot as plt

data = pn.read_csv(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\separate files\-3555.csv')
image = plt.imread(r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\separate files\-3555.jp2')
folder = r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\separate files\-3555V\positive'
dest = r'D:\engram\New_Converted_Folder\N2\0.5h\csv files\separate files\-3555V\positive_ready'

walkFiles = os.walk(folder)
filesNames = []
for root, dirs, file in walkFiles:
    filesNames = file
for file in filesNames:
    row = data.loc[int(file[:-4])]
    plt.imsave(dest + "\\" + file,
               image[int(abs(row['y'])) - 20:int(abs(row['y'])) + 20, int(row['x']) - 20:int(row['x']) + 20, :])
