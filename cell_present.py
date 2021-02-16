import matplotlib.pyplot as plt
import matplotlib.patches as ptc
from PIL import Image
import numpy as np
from math import sqrt
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
from skimage import filters
Image.MAX_IMAGE_PIXELS = 275727232

image = plt.imread(
    r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-2855.jp2')
# data=pn.read_csv(r'D:\engram\New_Converted_Folder\N3\1h\csv files\separate files\1345.csv')

x_pixel = 9400
y_pixel = 5906

distance = 200
# plt.imsave(r'C:\Users\owner\Desktop\dataset\test.jpg',
#            image[y_pixel - 20:y_pixel + 20, x_pixel - 20:x_pixel + 20, :])
#
cell_matrix = image[:, :, 0][y_pixel - distance:y_pixel + distance, x_pixel - distance:x_pixel + distance]
val = filters.threshold_otsu(cell_matrix)
plt.figure(figsize=(20, 20))
plt.subplot(131)
plt.title("NeuN")
ax = plt.gca()
plt.imshow(cell_matrix, cmap='gray')
rect = ptc.Rectangle((distance - 10, distance - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)


plt.subplot(132)
ax = plt.gca()
cell_matrix_2 = image[y_pixel - distance:y_pixel + distance, x_pixel - distance:x_pixel + distance, 1]
tt=rgb2gray(cell_matrix_2)
# blobs_log = blob_log(tt, max_sigma=8,  min_sigma=2, threshold=.03)
# blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
# for blob in blobs_log:
#     y, x, r = blob
#     print ("X: "+str(x)+" Y: "+str(y)+" R: "+str(r))
#     c = plt.Circle((x, y), r, color="Yellow", linewidth=2, fill=False)
#     ax.add_patch(c)

plt.title("C-fos")
plt.imshow(cell_matrix_2, cmap='gray')
rect = ptc.Rectangle((distance - 10, distance - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)


plt.subplot(133)
cell_matrix_3 = image[:, :, 2][y_pixel - distance:y_pixel + distance, x_pixel - distance:x_pixel + distance]
plt.title("Dapi")
ax = plt.gca()
# plt.imshow(cell_matrix_3, cmap='gray')
plt.imshow(cell_matrix, cmap='gray')
rect = ptc.Rectangle((distance - 10, distance - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)
# plt.savefig(r'C:\Users\owner\Desktop\try.jpg')
plt.show()
