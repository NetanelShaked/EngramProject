import pandas as pd


class Initialize_CSV_Files:
    """
    This class should be using after separate the point csv file that output from neuroInfo\n
    that initialize method get csv name of specific bregma and fill the column id_name and parents_name\n
    parameters:
    path: get the folder direction\n
    file_name: get the csv file name (with extension)

    \n\n
    After initialize the object use action method

    \n\n
    This operation using excel file that provided by NeuroInfo support - this excel describe which area belong to each id
    """

    def __init__(self, path, fileName):
        self.path = path
        self.fileName = fileName

    def action(self, is_main_csv=1, neun_limit=0):
        """
        If id doesnt appear in excel file that provided by NeuroInfo support- the method printing the number of the id
        :parameter is_main_csv: 1 if this function using for initialize the main csv file , 2 if its using for csv
        separate by bregma
        :parameter neun_limit: all Channel 2 values that smaller (include this value) will erase
        :return: list of mismatch id's
        """

        registration_csv = pd.read_csv(r'D:\Lab\ontology_api_2017.csv')
        if is_main_csv != 1:
            csv_data_file = pd.read_csv(self.path + "\\" + self.fileName)
        else:
            csv_data_file = pd.read_csv(self.path + "\\" + self.fileName, header=1)

        print(csv_data_file.columns)
        print(csv_data_file.shape)
        if(neun_limit!=0):
            csv_data_file = csv_data_file[csv_data_file["Channel 2"] > neun_limit]
        print(csv_data_file['Unnamed: 0'].unique())
        if is_main_csv == 1:
            csv_data_file[csv_data_file['Unnamed: 0'] == 'NeuN_region_check'].to_csv(self.path + "\\NeuN_Background.csv",
                                                                                     index=False)
            csv_data_file = csv_data_file[csv_data_file['Unnamed: 0'] == "DAPI"]
            # csv_data_file = csv_data_file[csv_data_file['strength'] >= 9]
        csv_data_file = csv_data_file[csv_data_file['id'] != 0]

        id_dict = {997.0: 'root'}
        parent_id_dict = {997.0: 997}
        final_dict = {}
        id_name = []
        parent_name = []
        region_name = []
        not_found_set = set()

        for index, row in registration_csv.iterrows():
            if row['id'] not in id_dict:
                id_dict[row['id']] = row['name']
                parent_id_dict[row['id']] = row['parent_structure_id']
        for key, value in id_dict.items():
            final_dict[key] = (value, id_dict[parent_id_dict[key]], id_dict[parent_id_dict[parent_id_dict[key]]])

        for index, row in csv_data_file.iterrows():
            if row['id'] in final_dict:
                id_name.append(final_dict[row['id']][0])
                parent_name.append(final_dict[row['id']][1])
                region_name.append(final_dict[row['id']][2])
            else:
                not_found_set.add(row['id'])
                id_name.append('??')
                parent_name.append('??')
                region_name.append('??')

        csv_data_file['id name'] = id_name
        csv_data_file['parent name'] = parent_name
        csv_data_file['region'] = region_name
        csv_data_file.to_csv(self.path + "\\" + self.fileName[:-4] + "_withNames.csv", index=False)
        return list(not_found_set)
