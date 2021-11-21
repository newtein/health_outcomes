from make_file_for_odds_ratio_child import GetData
import pandas as pd
from config import CONFIG
from constants import *
from read_brfss_file import ReadBRFSS
from sklearn.linear_model import LogisticRegression
import numpy as np
from get_population_by_state import GetAgeSex
from calculate_poverty import POVERTY


class ModelingDataChild:
    """
    TODO: make dynamic population year selection, currently use 2017 (median year of the current analysis)
    """
    def __init__(self):
        self.dfs = GetData().execute()

    def if_carb(self, x):
        if x in CARB:
            return 1
        return 0

    def get_primary_risk(self, x):
        if x['CASTHDX2'] == 1:
            if x['CASTHNO2'] == 1:
                return 1
        return 0


    def get_data_with_epa_region(self):
        dfs = self.dfs
        mdf = pd.DataFrame()
        for i in range(len(dfs)):
            mdf = mdf.append(dfs[i])
        # Children don't smoke assumption
        # mdf = mdf[mdf['SMOKE100'] == 2]
        mdf['TAILPIPE'] = mdf['_STATE'].apply(self.if_carb)
        mdf = mdf[mdf['CASTHDX2'].isin([1, 2])]
        mdf['ASTHMA'] = mdf.apply(self.get_primary_risk, axis=1)
        mdf = POVERTY(mdf).process()

        population__df = GetAgeSex('2017').read_file_by_population()
        population__df = population__df[population__df['STATE'] != 0]
        # population__df['POPEST2017_CIV'] = (population__df['POPEST2017_CIV'] - population__df[
        #     'POPEST2017_CIV'].mean()) / population__df['POPEST2017_CIV'].std()
        # mdf = mdf.merge(population__df[['STATE', 'POPEST2017_CIV']], left_on="_STATE", right_on="STATE", how="left")
        population__df['DENSITY'] = (population__df['DENSITY'] - population__df[
            'DENSITY'].mean()) / population__df['DENSITY'].std()
        mdf = mdf.merge(population__df[['STATE', 'DENSITY']], left_on="_STATE", right_on="STATE", how="left")

        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Code', "EPA Region"]]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        mdf = mdf.merge(epa_region, left_on="_STATE", right_on="State Code", how='left')
        # new_cols = ["POPEST2017_CIV", 'EPA Region', '_STATE']
        # mdf = mdf[MODELING_COLUMNS+new_cols]
        return mdf

