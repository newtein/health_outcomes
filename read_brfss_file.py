from config import CONFIG
from get_sas_df import ReadSAS
from constants import *
import pandas as pd
import os


class ReadBRFSS:
    def __init__(self, year):
        self.year = year
        self.keyword = "BRFSS"
        self.filename = self.get_filename_trunc()
        print(self.filename)

    def get_filename_trunc(self):
        return "data/{}/{}/{}".format(self.keyword, self.year, "BRFSS_health_data_{}_selected_columns.csv".format(self.year))

    def get_filename_original(self):
        return "data/{}/{}/{}".format(self.keyword, self.year, CONFIG.get(self.keyword).get(self.year))

    def make_file(self):
        f = self.get_filename_original()
        read_sas_df = ReadSAS().get_df(f)
        read_sas_df = read_sas_df[MANDATORY_BRFSS_COLUMNS]
        fw = self.get_filename_trunc()
        read_sas_df.to_csv(fw, index=False)

    def get_df(self, all=False):
        if not all:
            if not os.path.exists(self.filename):
                self.make_file()
                print("not making file")
            return pd.read_csv(self.filename)
        return False

if __name__ == "__main__":
    obj = ReadBRFSS('2017')
    print(obj.get_df().head(2))