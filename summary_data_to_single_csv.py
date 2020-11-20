import pandas as pn


class summery_data_to_single_csv:
    def __init__(self, path, file_name):
        self.__path = path
        self.__file_name = file_name

    def action(self):
        column='id name'
        data = pn.read_csv(self.__path + "\\" + self.__file_name)
        regions = data[column].unique()
        new_df = pn.DataFrame({'Region': [], 'Left Count': [], 'Right Count': [], 'Sum': []})
        for region in regions:
            new_df = new_df.append(
                {'Region': region, 'Left Count': len(
                    data[(data[column] == region) & (data['hemisphere'] == 'left')]),
                 'Right Count': len(data[(data[column] == region) & (data['hemisphere'] == 'right')]),
                 'Sum': len(data[(data[column] == region) & (data['hemisphere'] == 'right')]) + len(
                     data[(data[column] == region) & (data['hemisphere'] == 'left')])},
                ignore_index=True)
        new_df.to_csv(self.__path+"\\Summary.csv", index=False)