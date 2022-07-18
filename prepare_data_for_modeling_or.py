from make_file_for_odds_ratio import GetData
import pandas as pd
from constants import *
from get_population_by_state import GetAgeSex
from calculate_poverty import POVERTY
from adjust_weights_for_or import AdjustWeightsForOR
import os
from copy import deepcopy
from config import CONFIG
import constants


class ModelingData:
    """
    TODO: make dynamic population year selection, currently use 2017 (median year of the current analysis)
    """
    def __init__(self):
        self.pop_type = 'ADULT'
        self.dfs = GetData().execute()

    def if_carb(self, x):
        if x in ZEV_STATES:
            return 1
        return 0

    def get_primary_risk(self, x):
        if x['ASTHMA3'] == 1:
            if x['ASTHNOW'] == 1:
                return 1
        return 0

    def get_poverty_level(self):
        pass

    def get_data(self):
        dfs = self.dfs
        mdf = pd.DataFrame()
        for i in range(len(dfs)):
            mdf = mdf.append(dfs[i])
        mdf = mdf[mdf['SMOKE100'] == 2]
        mdf['NONCARB'] = mdf['_STATE'].apply(self.if_carb)
        mdf = mdf[mdf['ASTHMA3'].isin([1, 2])]
        mdf['ASTHMA'] = mdf.apply(self.get_primary_risk, axis=1)
        mdf = POVERTY(mdf).process()
        return mdf

    def get_data_with_pop(self):
        dfs = self.dfs
        mdf = pd.DataFrame()
        for i in range(len(dfs)):
            mdf = mdf.append(dfs[i])
        mdf = mdf[mdf['SMOKE100'] == 2]
        mdf['NONCARB'] = mdf['_STATE'].apply(self.if_carb)
        mdf = mdf[mdf['ASTHMA3'].isin([1, 2])]
        mdf['ASTHMA'] = mdf.apply(self.get_primary_risk, axis=1)

        mdf = POVERTY(mdf).process()

        population__df = GetAgeSex('2017').read_file_by_population()
        population__df = population__df[population__df['STATE'] != 0]
        # population__df['POPEST2017_CIV'] = (population__df['POPEST2017_CIV'] - population__df[
        #     'POPEST2017_CIV'].mean()) / population__df['POPEST2017_CIV'].std()
        # mdf = mdf.merge(population__df[['STATE', 'POPEST2017_CIV']], left_on="_STATE", right_on="STATE", how="left")
        #
        population__df['DENSITY'] = (population__df['DENSITY'] - population__df[
            'DENSITY'].mean()) / population__df['DENSITY'].std()
        mdf = mdf.merge(population__df[['STATE', 'DENSITY']], left_on="_STATE", right_on="STATE", how="left")

        new_cols = ["POPEST2017_CIV"]
        # mdf = mdf[MODELING_COLUMNS+new_cols]
        return mdf

    def get_data_with_epa_region(self):
        """
        original_mdf is used for making the demographic tables, whereas mdf is filtered and used to calculate odds
        :return:
        """
        years = CONFIG.get("analysis_years")
        years_str = "_".join([str(i) for i in years])
        CONFIG.update({"analysis_years": years})
        DATA_ODDS_RATIO_MODULE = constants.DATA_ODDS_RATIO_MODULE + "/{}".format(years_str)
        fname = "{}/BRFSS_{}_OR.csv".format(DATA_ODDS_RATIO_MODULE, self.pop_type)
        # if os.path.exists(fname):
        #     return pd.read_csv(fname)
        dfs = self.dfs
        mdf = pd.DataFrame()
        for i in range(len(dfs)):
            mdf = mdf.append(dfs[i])
        original_mdf = deepcopy(mdf)
        mdf = mdf[mdf['SMOKE100'] == 2]

        mdf['NONCARB'] = mdf['_STATE'].apply(self.if_carb)
        original_mdf['NONCARB'] = original_mdf['_STATE'].apply(self.if_carb)

        mdf = mdf[mdf['ASTHMA3'].isin([1, 2])]
        mdf['ASTHMA'] = mdf.apply(self.get_primary_risk, axis=1)
        original_mdf['ASTHMA'] = original_mdf.apply(self.get_primary_risk, axis=1)


        mdf = POVERTY(mdf).process()

        population__df = GetAgeSex('2017').read_file_by_population()
        population__df = population__df[population__df['STATE'] != 0]
        # population__df['POPEST2017_CIV'] = (population__df['POPEST2017_CIV'] - population__df[
        #     'POPEST2017_CIV'].mean()) / population__df['POPEST2017_CIV'].std()
        # mdf = mdf.merge(population__df[['STATE', 'POPEST2017_CIV']], left_on="_STATE", right_on="STATE", how="left")
        population__df['DENSITY_RAW'] = population__df['DENSITY'].tolist()
        population__df['DENSITY'] = (population__df['DENSITY'] - population__df[
            'DENSITY'].mean()) / population__df['DENSITY'].std()
        mdf = mdf.merge(population__df[['STATE', 'DENSITY', 'DENSITY_RAW', 'surface_area', 'population']], left_on="_STATE", right_on="STATE", how="left")

        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name', 'State Code', "EPA Region"]]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        mdf = mdf.merge(epa_region, left_on="_STATE", right_on="State Code", how='left')

        new_cols = ["State Name", "_STATE", 'EPA Region']
        mdf = mdf[MODELING_COLUMNS + new_cols]
        mdf = AdjustWeightsForOR(mdf, self.pop_type).execute()
        # mdf.to_csv(fname, index=False)
        print("File written {}: {}".format(self.pop_type, fname))
        return mdf

