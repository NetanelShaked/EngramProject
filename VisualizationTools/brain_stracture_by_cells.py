import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import numpy as np

def visualization_all_brain_cells(image_path, csv_path):
    Image.MAX_IMAGE_PIXELS=10**9
    image=plt.imread(image_path)
    csv=pd.read_csv(csv_path)
    mean=csv['Channel 2'].mean()
    csv=csv[csv['Channel 2']>mean]
    print(mean)
    new_image=np.zeros((len(image[0]),len(image[1])))
    cell_size=4
    for idx,row in csv.iterrows():
        y_pixel=abs(int(row['y']))
        x_pixel=int(row['x'])
        new_image[y_pixel-cell_size:y_pixel+cell_size,x_pixel-cell_size:x_pixel+cell_size]=1
    plt.imshow(new_image , cmap='gray')
    plt.imsave("whole_brain_output_by_csvDetails.jpg",new_image, cmap='gray')
    plt.show()

if __name__ == '__main__':
    csv_path=r'D:\Lab\Data_from_lab\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-1255.csv'
    # csv_path=r'D:\Lab\Data_from_lab\N2-20210214T082519Z-012\N2\1h\csv files\separate files\NeunFilter\-1255_try_filtered.csv'
    image_path=r'D:\Lab\Data_from_lab\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-1255.jp2'
    visualization_all_brain_cells(image_path, csv_path)