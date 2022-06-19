import pandas as pd
from prepare_data_for_modeling_or import ModelingData
from get_population_by_state import GetAgeSex
from constants import *


class PovertyModule:
    def __init__(self, pop_type):
        self.pop_type = pop_type
        obj = ModelingData()
        df = obj.get_data_with_epa_region()
        df = df[~df['_STATE'].isin(EXCLUDE_STATES)]
        if self.pop_type == 'ADULT':
            self.weighted_col = '_LLCPWT2'
        else:
            self.weighted_col = "_CLLCPWT"
        df = df[~pd.isna(df[self.weighted_col])]
        population_df = GetAgeSex('2017').read_file_by_population()
        t = population_df
        t = t[t["STATE"] == 0]
        self.us_population = t['POPEST2017_CIV'].loc[0]
        population_df = population_df[population_df['STATE'] != 0]
        self.df = df.merge(population_df[['STATE', 'POPEST2017_CIV']], left_on="_STATE", right_on="STATE", how="left")

    def get_data(self):
        carb = self.df[self.df['NONCARB'] == 0]
        noncarb = self.df[self.df['NONCARB'] == 1]

        carb_results = self.get_numbers(carb)
        carb_us = self.get_numbers_us(carb)
        carb_results.update(carb_us)

        noncarb_results = self.get_numbers(noncarb)
        noncarb_us = self.get_numbers_us(noncarb)
        noncarb_results.update(noncarb_us)
        return carb_results, noncarb_results

    def get_weighted_data(self):
        carb = self.df[self.df['NONCARB'] == 0]
        noncarb = self.df[self.df['NONCARB'] == 1]

        carb_results = self.get_weighted_numbers(carb)
        carb_us = self.get_weighted_numbers_us(carb)
        carb_results.update(carb_us)

        noncarb_results = self.get_weighted_numbers(noncarb)
        noncarb_us = self.get_weighted_numbers_us(noncarb)
        noncarb_results.update(noncarb_us)
        return carb_results, noncarb_results

    def get_numbers(self, df):
        results = {}
        for epa_region in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            f1 = (df['POVERTY'] == 1) & (df['EPA Region'] == epa_region)
            f1_bar = (df['EPA Region'] == epa_region)
            f2 = (df['ASTHMA'] == 1) & (df['POVERTY'] == 1) & (df['EPA Region'] == epa_region)
            f2_bar = (df['POVERTY'] == 1) & (df['EPA Region'] == epa_region)
            try:
                poverty_count = (df[f1][self.weighted_col].sum() * 100) / df[f1_bar][self.weighted_col].sum()
                poverty_with_asthma_count = (df[f2][self.weighted_col].sum()* 100) / df[f1_bar][self.weighted_col].sum()
                # print(epa_region, poverty_count, poverty_with_asthma_count)
            except:
                poverty_count, poverty_with_asthma_count = None, None

            temp = {
                "POVERTY%": poverty_count,
                "POVERTYASTHMA%": poverty_with_asthma_count
            }
            results[epa_region] = temp
        return results

    def get_numbers_us(self, df):
        results = {}
        f1 = (df['POVERTY'] == 1)
        f2 = (df['ASTHMA'] == 1) & (df['POVERTY'] == 1)
        f2_bar = (df['POVERTY'] == 1)
        try:
            poverty_count = (df[f1][self.weighted_col].sum() * 100) / df[self.weighted_col].sum()
            poverty_with_asthma_count = (df[f2][self.weighted_col].sum() * 100) / df[self.weighted_col].sum()
            # print(epa_region, poverty_count, poverty_with_asthma_count)
        except:
            poverty_count, poverty_with_asthma_count = None, None

        temp = {
            "POVERTY%": poverty_count,
            "POVERTYASTHMA%": poverty_with_asthma_count
        }
        results[0] = temp
        return results

    def get_weighted_numbers(self, df):
        results = {}
        for epa_region in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            f_pop = df['EPA Region'] == epa_region
            population = df[f_pop]["POPEST2017_CIV"].sum()
            f1 = (df['POVERTY'] == 1) & (df['EPA Region'] == epa_region)
            f1_bar = (df['EPA Region'] == epa_region)
            f2 = (df['ASTHMA'] == 1) & (df['POVERTY'] == 1) & (df['EPA Region'] == epa_region)
            f2_bar = (df['POVERTY'] == 1) & (df['EPA Region'] == epa_region)
            try:
                poverty_count = (df[f1].shape[0] * population) / df[f1_bar].shape[0]
                poverty_with_asthma_count = (df[f2].shape[0] * population) / df[f1_bar].shape[0]
                # print(epa_region, poverty_count, poverty_with_asthma_count)
            except:
                poverty_count, poverty_with_asthma_count = None, None

            temp = {
                "POVERTY%": poverty_count,
                "POVERTYASTHMA%": poverty_with_asthma_count
            }
            results[epa_region] = temp
        return results

    def get_weighted_numbers_us(self, df):
        results = {}
        population = self.us_population
        f1 = (df['POVERTY'] == 1)
        f2 = (df['ASTHMA'] == 1) & (df['POVERTY'] == 1)
        f2_bar = (df['POVERTY'] == 1)
        try:
            print(population)
            poverty_count = (df[f1].shape[0] * population) / df.shape[0]
            poverty_with_asthma_count = (df[f2].shape[0] * population) / df.shape[0]
            # print(epa_region, poverty_count, poverty_with_asthma_count)
        except:
            poverty_count, poverty_with_asthma_count = None, None

        temp = {
            "POVERTY%": poverty_count,
            "POVERTYASTHMA%": poverty_with_asthma_count
        }
        results[0] = temp
        return results