import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.utils import shuffle


def squere_info(image_path, csv_path):
    Image.MAX_IMAGE_PIXELS = 10 ** 9
    image = plt.imread(image_path)
    csv = pd.read_csv(csv_path)

    distance = 600
    cell_radius_in_pixel = 4
    channel = 0
    csv_iter = pd.DataFrame(shuffle(csv)).reset_index().iloc[:min(len(csv), 1000)]
    for idx_main, row_main in csv_iter.iterrows():
        x_pixel = int(row_main['x'])
        y_pixel = int(row_main['y'])
        relevant_csv = csv[(csv['y']>y_pixel-distance)&(csv['y']<y_pixel+distance)]
        relevant_csv = relevant_csv[(relevant_csv['x']>x_pixel-distance)&(relevant_csv['x']<x_pixel+distance)]
        summarize_list = []
        cell_locations = np.zeros((distance * 2, distance * 2))
        y_pixel = abs(int(y_pixel))
        for idx, row in relevant_csv.iterrows():
            x_cell = int(row['x'])
            y_cell = abs(int(row['y']))
            summarize_list.append(image[y_cell - cell_radius_in_pixel:y_cell + cell_radius_in_pixel,
                                  x_cell - cell_radius_in_pixel:x_cell + cell_radius_in_pixel, channel].mean())
            cell_locations[
            y_cell + distance - y_pixel - cell_radius_in_pixel:y_cell + distance - y_pixel + cell_radius_in_pixel,
            x_cell + distance - x_pixel - cell_radius_in_pixel:x_cell + distance - x_pixel + cell_radius_in_pixel] = 1
        print("found: ", len(summarize_list))
        print(len(cell_locations[cell_locations == 1]) / (cell_radius_in_pixel ** 2))
        plt.figure(figsize=(10, 10))
        plt.subplot(1, 2, 1)
        plt.hist(summarize_list, bins=int(max(summarize_list) + 1))
        plt.xlabel("Intensity")
        plt.ylabel("number of cells")
        plt.title("Histogram: " + str(abs(y_pixel)) + "," + str(x_pixel) + " distance: " + str(distance))
        plt.subplot(1, 2, 2)
        plt.title("found: " + str(len(summarize_list)))
        local_image = image[y_pixel - distance:y_pixel + distance,
                      x_pixel - distance:x_pixel + distance, channel]
        im=plt.imshow(local_image, cmap='gray')
        plt.imshow(cell_locations, cmap='copper', alpha=0.5)
        # im = plt.imshow(cell_locations, cmap='copper')
        plt.colorbar(im)
        plt.savefig(os.path.join(r'D:\Lab\4-3 talk_2', str(idx_main) + ".jpg"))
        plt.close()
    # plt.show()


if __name__ == '__main__':
    image = r'D:\Lab\Data_from_lab\N2-20210214T082519Z-012\N2\1h\csv files\separate files_2\-1255.jp2'
    csv = r'C:\Users\shako\PycharmProjects\EngramProject\Appendices\checking.csv'
    squere_info(image, csv)
