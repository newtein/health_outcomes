from config import CONFIG
import pandas as pd
import numpy as np

class GetAgeSex:
    def __init__(self, year, pop_type='CHILD'):
        self.year = year
        self.keyword = "CENSUS"
        self.pop_col = 'POPEST{}_CIV'.format(self.year)
        self.pop_type = pop_type

    def if_child(self, x):
        if x < 18:
            return 1
        else:
            return 0

    def read_file(self):
        fname = "data/{}/{}".format(self.keyword, CONFIG.get(self.keyword).get("age_sex"))
        df = pd.read_csv(fname)
        year_col = "POPEST{}_CIV".format(self.year)
        columns = ["STATE", "SEX", "AGE"] + [year_col]
        df = df[columns]
        df['CHILD'] = df['AGE'].apply(self.if_child)
        df = df[df['AGE'] != 999]
        pop_estimate_by_age_sex = df.groupby(['STATE', "SEX", "CHILD"]).agg({year_col: 'sum'}).reset_index()
        return pop_estimate_by_age_sex

    def read_file_by_age(self):
        fname = "data/{}/{}".format(self.keyword, CONFIG.get(self.keyword).get("age_sex"))
        df = pd.read_csv(fname)
        year_col = "POPEST{}_CIV".format(self.year)
        columns = ["STATE", "SEX", "AGE"] + [year_col]
        df = df[columns]
        df['CHILD'] = df['AGE'].apply(self.if_child)
        df = df[(df['AGE'] != 999) & (df['SEX'] == 0)]
        # if self.pop_type == 'CHILD':
        #     df = df[(0 <= df['AGE'] < 18)]
        pop_estimate_by_age = df.groupby(['STATE', "SEX", "CHILD"]).agg({year_col: 'sum'}).reset_index()
        return pop_estimate_by_age

    def merge_for_state(self, df):
        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name', 'State Code']]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        df = df.merge(epa_region, left_on="_STATE", right_on="State Code", how='left')
        return df
    def calculate_population_using_weight(self, mdf):
        if self.pop_type == 'CHILD':
            weight_col = '_CLLCPWT'
        fname = "data/{}/{}".format(self.keyword, CONFIG.get(self.keyword).get("age_sex"))
        df = pd.read_csv(fname)
        if int(self.year) < 2010:
            year_col = "POPEST{}_CIV".format(2010)
        else:
            year_col = "POPEST{}_CIV".format(self.year)

        pop_from_weight_df = mdf.groupby(["_STATE"]).agg({weight_col: 'sum'}).reset_index()
        surface_df = self.get_surface_area_for_density()
        pop_from_weight_df = self.merge_for_state(pop_from_weight_df)
        pop_from_weight_df = pop_from_weight_df.merge(surface_df, left_on='State Name', right_on='State and other areas2', how='left')
        pop_from_weight_df[year_col] = pop_from_weight_df[weight_col]
        pop_from_weight_df['DENSITY'] = pop_from_weight_df[year_col] / pop_from_weight_df['surface_area']
        pop_from_weight_df['population'] = pop_from_weight_df[year_col].tolist()
        return pop_from_weight_df

    def read_file_by_population(self):
        fname = "data/{}/{}".format(self.keyword, CONFIG.get(self.keyword).get("age_sex"))
        df = pd.read_csv(fname)
        year_col = "POPEST{}_CIV".format(self.year)
        columns = ["STATE","NAME", "SEX", "AGE"] + [year_col]
        df = df[columns]
        df = df[(df['AGE'] != 999) & (df['SEX'] == 0)]
        if self.pop_type == 'CHILD':
            df = df[(df['AGE'] >= 0) & (df['AGE'] < 18)]
        pop_estimate = df.groupby(['STATE', "NAME", "SEX"]).agg({year_col: 'sum'}).reset_index()
        surface_df = self.get_surface_area_for_density()
        pop_estimate = pop_estimate.merge(surface_df, left_on='NAME', right_on='State and other areas2', how='left')
        pop_estimate['DENSITY'] = pop_estimate[year_col] / pop_estimate['surface_area']
        pop_estimate['population'] = pop_estimate[year_col].tolist()
        return pop_estimate

    def get_surface_area_for_density(self):
        df = pd.read_excel("data/us_census/state_surface_area.xlsx", engine='openpyxl')
        col = ['State and other areas2', 'surface_area']
        df['surface_area'] = df['Land_Area_km']
        return df[col]

    def get_surface_area_with_state_code(self):
        df = pd.read_excel("data/us_census/state_surface_area.xlsx", engine='openpyxl')
        col = ['State and other areas2', 'surface_area']
        df['surface_area'] = df['Land_Area_km']
        epa_df = self.get_epa_region_df()
        mdf = epa_df.merge(df[col], left_on='State Name', right_on='State and other areas2', how='left')
        return mdf

    def get_epa_region_df(self):
        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name', 'State Code']]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        return epa_region

    def read_by_state(self, state_code):
        """
        SEX
            0: both sex
            1: male
            2: female
        CHILD
            1 < 18 years
        """
        df = self.read_file()
        a = df[df['STATE']==state_code]
        child_num = a[(a['SEX'] == 0) & (a['CHILD']==1)][self.pop_col].tolist()[0]
        adult_num = a[(a['SEX'] == 0) & (a['CHILD']==0)][self.pop_col].tolist()[0]
        return {"STATE": state_code, "ADULTS": adult_num, "CHILDREN": child_num, "YEAR": self.year}


if __name__ == "__main__":
    obj = GetAgeSex('2017')
    print(obj.read_by_state(1))