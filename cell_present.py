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
    r'C:\Users\shako\Downloads\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-1255.jp2')
# data=pn.read_csv(r'D:\engram\New_Converted_Folder\N3\1h\csv files\separate files\1345.csv')

x_pixel = 8284
y_pixel = 6791

distance = 300
# plt.imsave(r'C:\Users\owner\Desktop\dataset\test.jpg',
#            image[y_pixel - 20:y_pixel + 20, x_pixel - 20:x_pixel + 20, :])
#
# cc=filters.threshold_otsu(image[:,:,0])

cell_matrix = image[:, :, 0][y_pixel - distance:y_pixel + distance, x_pixel - distance:x_pixel + distance]
x,y=cell_matrix.shape
pixel_to_mictoMeter=0.203125
val = filters.threshold_otsu(cell_matrix)
plt.figure(figsize=(20, 20))
plt.subplot(141)
plt.title("NeuN-otsu")
ax = plt.gca()

# print ("threshold whole image is : "+ str(cc))

print (cell_matrix.std())

threshold=val+1*cell_matrix.std()*1.5

print("threshold=",threshold)
plt.imshow(cell_matrix>threshold, cmap='gray')
print("ostu threshold is :",val)
print(image[y_pixel-4:y_pixel+4,x_pixel-4:x_pixel+4,0].mean())
rect = ptc.Rectangle((distance - 10, distance - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

plt.subplot(142)
ax = plt.gca()
plt.title("NeuN")
plt.imshow(cell_matrix, cmap='gray')
print(val)
print(image[y_pixel,x_pixel,0])
rect = ptc.Rectangle((distance - 10, distance - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)

plt.subplot(143)
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
plt.imshow(cell_matrix_2, cmap='gray',extent=(0,x*pixel_to_mictoMeter,0,y*pixel_to_mictoMeter))
rect = ptc.Rectangle((distance - 20, distance - 20), 40, 40, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)
plt.imshow(cell_matrix_2, cmap='gray',extent=(0,x*pixel_to_mictoMeter,0,y*pixel_to_mictoMeter))



plt.subplot(144)
cell_matrix_3 = image[:, :, 2][y_pixel - distance:y_pixel + distance, x_pixel - distance:x_pixel + distance]
plt.title("Dapi")
ax = plt.gca()
# plt.imshow(cell_matrix_3, cmap='gray')
plt.imshow(cell_matrix, cmap='gray',extent=(0,x*pixel_to_mictoMeter,0,y*pixel_to_mictoMeter))
rect = ptc.Rectangle((distance - 10, distance - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none')
ax.add_patch(rect)
# plt.savefig(r'C:\Users\owner\Desktop\try.jpg')
plt.savefig("example4.jpg")
plt.show()
