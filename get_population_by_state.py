from config import CONFIG
import pandas as pd
import numpy as np

class GetAgeSex:
    def __init__(self, year, pop_type='ADULT'):
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

    def calculate_population_using_weight(self, mdf):
        if self.pop_type == 'CHILD':
            weight_col = '_CLLCPWT'
        fname = "data/{}/{}".format(self.keyword, CONFIG.get(self.keyword).get("age_sex"))
        df = pd.read_csv(fname)
        if int(self.year) < 2010:
            year_col = "POPEST{}_CIV".format(2010)
        else:
            year_col = "POPEST{}_CIV".format(self.year)

        columns = ["STATE","NAME", "SEX", "AGE"] + [year_col]
        df = df[columns]
        df = df[(df['AGE'] != 999) & (df['SEX'] == 0)]
        if self.pop_type == 'CHILD':
            df = df[(df['AGE'] >= 0) & (df['AGE'] < 18)]
        pop_from_weight_df = mdf.groupby(["_STATE"]).agg({weight_col: 'sum'}).reset_index()
        pop_estimate = df.groupby(['STATE', "NAME", "SEX"]).agg({year_col: 'sum'}).reset_index()
        pop_estimate[year_col] = np.nan
        pop_estimate = pop_estimate.merge(pop_from_weight_df, left_on = 'STATE', right_on = '_STATE')
        pop_estimate[year_col] = pop_estimate[weight_col]
        surface_df = self.get_surface_area_for_density()
        pop_estimate = pop_estimate.merge(surface_df, left_on='NAME', right_on='State and other areas2', how='left')
        pop_estimate['DENSITY'] = pop_estimate[year_col] / pop_estimate['surface_area']
        pop_estimate['population'] = pop_estimate[year_col].tolist()
        return pop_estimate

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
        df = pd.read_excel("data/us_census/state_surface_area.xlsx")
        col = ['State and other areas2', 'surface_area']
        df['surface_area'] = df['Land_Area_km']
        return df[col]

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