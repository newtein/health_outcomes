import pandas as pd
from config import CONFIG
import numpy as np


class AsthmaPrevalence:
    def __init__(self, year, pop_type='ADULT'):
        self.year = year
        self.keyword = 'BRFSS'
        self.pop_type = pop_type
        temp = CONFIG.get("ASTHMA").get(self.year).get(self.pop_type).get("Prevalence")
        self.fname = "data/BRFSS/{}/{}".format(self.year, temp)
        self.fregion = "data/states_and_counties.csv"
        print(self.fname)

    def get_low_CI(self, x):
        if not pd.isna(x):
            return float(x.split('–')[0].replace("(", ""))
        return None

    def get_high_CI(self, x):
        if not pd.isna(x):
            return float(x.split('–')[1].replace(")", ""))
        return None

    def get_df(self):
        df1 = pd.read_excel(self.fname, engine='openpyxl')
        region_df = pd.read_csv(self.fregion)
        region_df = region_df[region_df['State Code'] != 'CC']

        region_df = region_df.drop_duplicates(['State Code'], keep='first')
        prevalance_df = region_df.merge(df1, how='left', right_on='State', left_on='State Abbreviation')
        prevalance_df = prevalance_df[['State Code', 'State Name', 'EPA Region', 'Prevalence',
                                       'Standard', '95% CI']]
        prevalance_df['high_CI'] = prevalance_df['95% CI'].apply(self.get_high_CI)
        prevalance_df['low_CI'] = prevalance_df['95% CI'].apply(self.get_low_CI)
        prevalance_df['State Code'] = prevalance_df['State Code'].apply(int)
        return prevalance_df


if __name__ == "__main__":
    obj = AsthmaPrevalence('2017')
    print(obj.get_df())