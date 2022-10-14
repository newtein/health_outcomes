import pandas as pd
from constants import *
import numpy as np
import os
import sys
from constants import *


# In[9]:
class GetGroupTwoDataFrame:
    def __init__(self, mode='mul', syear=2008, eyear = 2020, group=2):
        # sin = single year
        # mul = three year window
        self.syear = syear
        self.eyear = eyear
        self.mode = mode
        self.group = group
        if self.group == 2:
            columns = ["state_code", "year", "Odds Ratio", "5%", "95%"]
        else:
            columns = ["year", "Odds Ratio", "5%", "95%"]
        data = self.init_data()
        self.df = pd.DataFrame(columns=columns, data=data)

    def init_data(self):
        if self.group == 2:
            if self.mode == 'sin':
                rows = [[state_code, year, np.nan, np.nan, np.nan] for year in range(self.syear, self.eyear+1) for
                        state_code in ZEV_STATES]
            else:
                rows = [[state_code, "{}_{}_{}".format(year, year+1, year+2), np.nan, np.nan, np.nan] for year in
                        range(self.syear, self.eyear+1) if year+2 <= self.eyear for state_code in ZEV_STATES]
        elif self.group == 1:
            if self.mode == 'sin':
                rows = [[year, np.nan, np.nan, np.nan] for year in range(self.syear, self.eyear + 1)]
            else:
                rows = [["{}_{}_{}".format(year, year + 1, year + 2), np.nan, np.nan, np.nan] for year in
                        range(self.syear, self.eyear + 1) if year + 2 <= self.eyear]
        return rows

    def read_data(self, year, fname, state_code=None):
        tdf = pd.read_csv(fname, index_col=0)
        zev = tdf.loc["NONCARB", "Odds Ratio"]
        zev_5 = tdf.loc["NONCARB", "5%"]
        zev_95 = tdf.loc["NONCARB", "95%"]
        if self.group == 2:
            filters = (self.df['year'] == year) & (self.df['state_code'] == state_code)
        else:
            filters = (self.df['year'] == year)
        self.df.loc[filters, "Odds Ratio"] = zev
        self.df.loc[filters, "5%"] = zev_5
        self.df.loc[filters, "95%"] = zev_95
        print(zev, zev_5)
        return tdf

    def merge_for_state_name(self):
        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name', 'State Code']]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        self.df = self.df.merge(epa_region, how="left", left_on="state_code", right_on="State Code")

    def execute_group_2(self):
        for state_code in ZEV_STATES:
            years = list(range(2008, 2020))
            dir_path = "odds_ratio_module/data/{}/{}"
            print(state_code)
            for year in years:
                if self.mode == 'mul':
                    year = "{}_{}_{}".format(year, year + 1, year + 2)
                    path = dir_path.format(year, "odds_ratio_CHILD_{}.csv".format(state_code))
                    print(path)
                elif self.mode == 'sin':
                    year = "{}".format(year)
                    path = dir_path.format(year, "odds_ratio_CHILD_{}.csv".format(state_code))
                    print(path)
                if os.path.exists(path):
                    print("ok")
                    self.read_data(state_code, year, path)
        return

    def execute_group_1(self):
        for state_code in [0]:
            years = list(range(2008, 2020))
            dir_path = "odds_ratio_module/data/{}/{}"
            print(state_code)
            for year in years:
                if self.mode == 'sin':
                    path = dir_path.format(year, "odds_ratio_CHILD_.csv".format(state_code))
                    if os.path.exists(path):
                         self.read_data(year, path)

    def execute(self):
        if self.group == 2:
            self.execute_group_2()
            self.merge_for_state_name()
        else:
            self.execute_group_1()
        f_dentifier = "three_year" if self.mode == 'mul' else "single_year"
        fname = "{}_group_{}.csv".format(f_dentifier, self.group)
        self.df.to_csv(DATA_ODDS_RATIO_MODULE + "/" + fname, index=False)

if __name__ == "__main__":
    mode = sys.argv[1]
    group = int(sys.argv[2])
    obj = GetGroupTwoDataFrame(mode=mode, group=group)
    obj.execute()
