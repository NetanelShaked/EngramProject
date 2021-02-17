import pandas as pn


class Create_csv_Dantate_Corpose:
    def __init__(self, path, file_name):
        self.__path = path
        self.__file_name = file_name

    def action(self):
        df = pn.read_csv(self.__path + "\\" + self.__file_name)
        Dentate = df[df['parent name'] == "Dentate gyrus"]["Channel 2"]
        Corpose = (df[df['parent name'] == "corpus callosum"]["Channel 2"]).values
        new_df = pn.DataFrame()
        new_df["Channel 2-Dentate"] = Dentate.values
        c = pn.DataFrame()
        c["Channel 2-Corpus"] = Corpose
        new_df = pn.merge(c, new_df, right_index=True, left_index=True, how='outer')
        new_df.to_csv(self.__path + "\\" + "Dentate_Corpus.csv", index=False)
