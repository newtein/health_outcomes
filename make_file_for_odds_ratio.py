import pandas as pd
from config import CONFIG
from constants import *
import os


class GetData:
    def __init__(self):
        self.years = CONFIG.get("analysis_years")

    def get_fname(self, year):
        f = "{}/{}.csv".format(DATA_ODDS_RATIO_MODULE,"BRFSS_{}_selected_cols".format(year))
        return f

    def execute(self):
        dfs = []
        for year in self.years:
            f = self.get_fname(year)
            if os.path.exists(f):
                df = pd.read_csv(f)
                print("File already exists: reading now...")
            else:
                fname = "data/{}/{}/{}".format("BRFSS", year, CONFIG.get('BRFSS').get(year))
                df = pd.read_sas(fname)
                for i, j in RENAME.items():
                    try:
                        df[j] = df[i]
                    except:
                        pass
                df = df[COLUMNS_FOR_ODD_RATIO]
                df = df[~df["_LLCPWT2"].isna()]
                df.to_csv(f, index=False)
                print(fname)
            dfs.append(df)
        return dfs


if __name__ == "__main__":
    obj = GetData()
    print(obj.execute())