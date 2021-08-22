import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import numpy as np

def visualization_all_brain_cells(image_path, csv_path):
    interest_region = pd.read_csv(r'D:\lab\interest _regions.csv')
    interest_region = interest_region[interest_region['Relevant'] == 'x']
    interest_region = interest_region['id']

    Image.MAX_IMAGE_PIXELS=10**9
    image=plt.imread(image_path)
    csv=pd.read_csv(csv_path)
    # csv = csv[csv['id'].isin(interest_region)]
    # mean=csv['Channel 2'].mean()
    # csv=csv[csv['Channel 2']>mean]
    # print(mean)
    new_image=np.zeros((len(image[0]),len(image[1])))
    cell_size=4
    for idx,row in csv.iterrows():
        y_pixel=abs(int(row['y']))
        x_pixel=int(row['x'])
        new_image[y_pixel-cell_size:y_pixel+cell_size,x_pixel-cell_size:x_pixel+cell_size]=1
    plt.imshow(new_image , cmap='gray')
    plt.imsave("whole_brain_output_after_NeuN_filter.jpg",new_image, cmap='gray')
    plt.show()

def visualization_all_brain_cells_from_fiji_results(image_path,csv_path):
    Image.MAX_IMAGE_PIXELS = 10 ** 9
    image = plt.imread(image_path)
    csv = pd.read_csv(csv_path)
    new_image=np.zeros((len(image[0]),len(image[1])))
    cell_size=4
    for idx,row in csv.iterrows():
        y_pixel=abs(int(row['YM']))
        x_pixel=int(row['XM'])
        new_image[y_pixel-cell_size:y_pixel+cell_size,x_pixel-cell_size:x_pixel+cell_size]=1
    plt.imshow(new_image , cmap='gray')
    plt.imsave("whole_brain_output_by_csvDetails_from_fiji.jpg",new_image, cmap='gray')
    plt.show()

if __name__ == '__main__':
    # csv_path=r'D:\Lab\Data_from_lab\N2-20210214T082519Z-012\N2\1h\csv files\separate files\-1255.csv'
    csv_path=r'D:\Lab\סלייס נסיון קונפוקל-20210505T154605Z-001\סלייס נסיון קונפוקל\there_test\test_points.csv'
    # csv_path=r'D:\Lab\Data_from_lab\N2-20210214T082519Z-012\N2\1h\csv files\separate files_2\-1255.csv'
    image_path=r'D:\Lab\סלייס נסיון קונפוקל-20210505T154605Z-001\סלייס נסיון קונפוקל\there_test\test_2.jp2'
    visualization_all_brain_cells(image_path, csv_path)
    # visualization_all_brain_cells_from_fiji_results(image_path,csv_path)