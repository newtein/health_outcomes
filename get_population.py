import pandas as pd
from constants import *
from copy import copy


class USPopulation:
    def __init__(self, start_year=2010, end_year=2019):
        self.start_year = start_year
        self.end_year = end_year
        self.df = pd.read_csv(CENSUS_DATA_PATH)
        self.df['county_name'] = self.df['county_name'].apply(lambda x: x.lower())

    def init_lookup(self):
        return {i: None for i in range(self.start_year, self.end_year+1)}

    def extract_population(self, df):
        n = df.shape[0]
        if n == 1:
            return df['POP'].tolist()[0]
        elif n == 3:
            for index, row in df.iterrows():
                desc = row['DATE_DESC']
                data_type = desc.split()[1]
                if data_type == 'Census':
                    return row['POP']
        else:
            print(df)

    def extract_row(self, df):
        n = df.shape[0]
        if n == 1:
            return df.iloc[0]
        elif n == 3:
            for index, row in df.iterrows():
                desc = row['DATE_DESC']
                data_type = desc.split()[1]
                if data_type == 'Census':
                    return row
        else:
            print(df)

    def get(self, county_name, state_name):
        county_name = county_name.lower()
        f1 = (self.df['county_name'] == county_name)
        f2 = (self.df['state_name'] == state_name)
        df = copy(self.df[f1 & f2])
        population_lookup = self.init_lookup()
        for year in population_lookup:
            df_year = df[df['year'] == year]
            population = self.extract_population(df_year)
            population_lookup[year] = population
        return population_lookup

    def get_surface_area(self, county_name, state_name):
        county_name = county_name.lower()
        f1 = (self.df['county_name'] == county_name)
        f2 = (self.df['state_name'] == state_name)
        df = copy(self.df[f1 & f2])
        surface_area_lookup = self.init_lookup()
        for year in surface_area_lookup:
            df_year = df[df['year'] == year]
            row = self.extract_row(df_year)
            density, pop = row['DENSITY'], row['POP']
            surface_area_lookup[year] = pop/density
        return surface_area_lookup


if __name__ == "__main__":
    obj = USPopulation()
    print(obj.get('Cook County'))

