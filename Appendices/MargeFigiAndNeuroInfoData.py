import pandas as pd
from scipy.spatial.distance import euclidean


def find_closest_reagion(x_point, y_point, neuroinfo_as_dataframe):
    distance = 50
    neuroinfo_as_dataframe = pd.DataFrame(neuroinfo_as_dataframe)
    neuroinfo_as_dataframe = neuroinfo_as_dataframe[
        (neuroinfo_as_dataframe['x'] - distance < x_point) & (neuroinfo_as_dataframe['x'] + distance > x_point) & (
                neuroinfo_as_dataframe['y'] - distance < -1 * y_point) & (
                neuroinfo_as_dataframe['y'] + distance > -1 * y_point)]
    closet_region = neuroinfo_as_dataframe.T.apply(
        lambda row: [euclidean((row['x'], row['y']), (x_point, -y_point)), row['id'], row['hemisphere'], row['id name'],
                     row['parent name'], row['region']]).T
    if len(closet_region)==0:
        return None
    return closet_region[closet_region[0] == min(closet_region[0])]


def marge_figi_neuroinfo(data_figi_path, data_neuroinfo_path):
    figi_data = pd.read_csv(data_figi_path)
    neuroinfo_data = pd.read_csv(data_neuroinfo_path)
    new_neuroinfo_data=neuroinfo_data.copy()
    distance = 3
    for index, row in figi_data.iterrows():
        x_point = row['XM']
        y_point = row['YM']
        is_exist = neuroinfo_data[
            (neuroinfo_data['x'] - distance < x_point) & (neuroinfo_data['x'] + distance > x_point) & (
                    neuroinfo_data['y'] - distance < -1 * y_point) & (
                    neuroinfo_data['y'] + distance > -1 * y_point)]
        if len(is_exist) == 0:
            found_region = find_closest_reagion(x_point, y_point, neuroinfo_data)
            if not type(found_region) == pd.DataFrame:
                continue
            new_neuroinfo_data = new_neuroinfo_data.append(
                {'x': x_point, 'y': -1 * y_point, 'z': data_neuroinfo_path.split('\\')[-1][:-4], 'id': found_region[1].values[0],
                 'hemisphere': found_region[2].values[0], 'id name': found_region[3].values[0], 'parent name': found_region[4].values[0],
                 'region': found_region[5].values[0]}, ignore_index=True)
    new_neuroinfo_data.to_csv('checking.csv',index=False)

if __name__ == '__main__':
    # csv = pd.read_csv(r'D:\Lab\Data_from_lab\N2-20210214T082519Z-012\N2\1h\csv files\separate files_2\-1255.csv')
    # a = find_closest_reagion(10810, 10772, csv)
    # print(a)
    figi_path=r'C:\Users\shako\Desktop\Results.csv'
    neuroinfo_path=r'D:\Lab\Data_from_lab\N2-20210214T082519Z-012\N2\1h\csv files\separate files_2\-1255.csv'
    marge_figi_neuroinfo(figi_path,neuroinfo_path)