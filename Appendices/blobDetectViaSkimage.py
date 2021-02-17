from math import sqrt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray
from PIL import Image
import matplotlib.pyplot as plt

# image = data.hubble_deep_field()[0:500, 0:500]
Image.MAX_IMAGE_PIXELS = 275727232
x = 3269
y = 4812
d = 50
im = plt.imread(
    r'C:\Users\owner\Desktop\New folder\PartialImage.jp2')
image=im[y - d:y + d, x - d:x + d, 1]
image_gray = rgb2gray(image)

blobs_log = blob_log(image_gray, max_sigma=10, num_sigma=4, threshold=.022)

# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.022)
blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.022)

blobs_list = [blobs_log, blobs_dog, blobs_doh]
colors = ['yellow', 'lime', 'red']
titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
          'Determinant of Hessian']
sequence = zip(blobs_list, colors, titles)

fig, axes = plt.subplots(1, 4, figsize=(9, 3), sharex=True, sharey=True)
ax = axes.ravel()

for idx, (blobs, color, title) in enumerate(sequence):
    ax[idx].set_title(title)
    ax[idx].imshow(image)
    for blob in blobs:
        y, x, r = blob
        if idx == 0:
            print("X:" + str(x) + " Y:" + str(y))
            ax[idx].add_patch(plt.Rectangle((d - 10, d - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none'))
        c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
        ax[idx].add_patch(c)
    ax[idx].set_axis_off()
ax[3].imshow(image)
ax[3].add_patch(plt.Rectangle((d - 10, d - 10), 20, 20, linewidth=1, edgecolor='r', facecolor='none'))
ax[3].set_axis_off()
plt.tight_layout()
plt.show()
