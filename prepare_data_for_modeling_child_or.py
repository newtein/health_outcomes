import math

from make_file_for_odds_ratio_child import GetData
import pandas as pd
from get_population_by_state import GetAgeSex
from calculate_poverty import POVERTY
from adjust_weights_for_or import AdjustWeightsForOR
from config import CONFIG
from constants import *
import constants
import numpy as np


class ModelingDataChild:
    """
    TODO: make dynamic population year selection, currently use 2017 (median year of the current analysis)
    """
    def __init__(self, state_code=None):
        self.state_code = state_code
        self.pop_type = 'CHILD'
        self.dfs = GetData().execute()

    def if_carb(self, x):
        if x in ZEV_STATES:
            return 1
        return 0

    def if_state(self, x):
        if x == self.state_code:
            return 1
        return 0

    def get_primary_risk(self, x):
        if x['CASTHDX2'] == 1:
            if x['CASTHNO2'] == 1:
                return 1
        return 0



    def get_data_with_epa_region(self):
        years = CONFIG.get("analysis_years")
        years_str = "_".join([str(i) for i in years])
        CONFIG.update({"analysis_years": years})
        DATA_ODDS_RATIO_MODULE = constants.DATA_ODDS_RATIO_MODULE + "/{}".format(years_str)
        fname = "{}/BRFSS_{}_OR.csv".format(DATA_ODDS_RATIO_MODULE, self.pop_type)
        dfs = self.dfs
        mdf = pd.DataFrame()
        for i, year in zip(range(len(dfs)), years):
            #population__df = GetAgeSex(str(year), pop_type=self.pop_type).read_file_by_population()
            population__df = GetAgeSex(str(year), pop_type=self.pop_type).calculate_population_using_weight(dfs[i])
            population__df = population__df[population__df['STATE'] != 0]
            print(population__df['DENSITY'].dtype)
            dfs[i] = dfs[i].merge(population__df[['STATE', 'DENSITY', 'surface_area', 'population']], left_on="_STATE",
                            right_on="STATE", how="left")

            dfs[i] = dfs[i][~pd.isna(dfs[i]["STATE"])]
            # dfs[i]['DENSITY'] = ((dfs[i]['DENSITY']-dfs[i]['DENSITY'].min()) / (dfs[i]['DENSITY'].max() - dfs[i]['DENSITY'].min()))*50
            # dfs[i]['DENSITY'] = (dfs[i]['DENSITY']-dfs[i]['DENSITY'].mean()) / dfs[i]['DENSITY'].std()
            # dfs[i]['DENSITY'] = dfs[i]['DENSITY'].apply(math.floor).astype(object)
            dfs[i]['year'] = int(year)
            mdf = mdf.append(dfs[i])
        # Children don't smoke assumption
        # mdf = mdf[mdf['SMOKE100'] == 2]
        if self.state_code:
            mdf['NONCARB'] = mdf['_STATE'].apply(self.if_state)
        else:
            mdf['NONCARB'] = mdf['_STATE'].apply(self.if_carb)
        mdf = mdf[mdf['CASTHDX2'].isin([1, 2])]
        mdf['ASTHMA'] = mdf.apply(self.get_primary_risk, axis=1)
        mdf = POVERTY(mdf).process()

        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name','State Code', "EPA Region"]]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        mdf = mdf.merge(epa_region, left_on="_STATE", right_on="State Code", how='left')
        new_cols = ["State Name", "_STATE", 'EPA Region', '_CLLCPWT', 'year']

        mdf = mdf[MODELING_COLUMNS_FOR_CHILD+new_cols]
        mdf = AdjustWeightsForOR(mdf, self.pop_type).execute()
        print("aa", mdf['year'].unique())
        # not writing the file to save up space
        # mdf.to_csv(fname, index=False)
        print("File written {}: {}".format(self.pop_type, fname))
        return mdf

