from make_file_for_odds_ratio_child import GetData
import pandas as pd
from constants import *
from get_population_by_state import GetAgeSex
from calculate_poverty import POVERTY
from adjust_weights_for_or import AdjustWeightsForOR


class ModelingDataChild:
    """
    TODO: make dynamic population year selection, currently use 2017 (median year of the current analysis)
    """
    def __init__(self):
        self.pop_type = 'CHILD'
        self.dfs = GetData().execute()

    def if_carb(self, x):
        if x in ZEV_STATES:
            return 1
        return 0

    def get_primary_risk(self, x):
        if x['CASTHDX2'] == 1:
            if x['CASTHNO2'] == 1:
                return 1
        return 0


    def get_data_with_epa_region(self):
        fname = "{}/BRFSS_{}_OR.csv".format(DATA_ODDS_RATIO_MODULE, self.pop_type)
        dfs = self.dfs
        mdf = pd.DataFrame()
        for i in range(len(dfs)):
            mdf = mdf.append(dfs[i])
        # Children don't smoke assumption
        # mdf = mdf[mdf['SMOKE100'] == 2]
        mdf['NONCARB'] = mdf['_STATE'].apply(self.if_carb)
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
        mdf = mdf.merge(population__df[['STATE', 'DENSITY', 'surface_area', 'population']], left_on="_STATE", right_on="STATE", how="left")

        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name','State Code', "EPA Region"]]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        mdf = mdf.merge(epa_region, left_on="_STATE", right_on="State Code", how='left')
        new_cols = ["State Name", "_STATE", 'EPA Region']
        mdf = mdf[MODELING_COLUMNS_FOR_CHILD+new_cols]
        mdf = AdjustWeightsForOR(mdf, self.pop_type).execute()
        mdf.to_csv(fname, index=False)
        print("File written {}: fname".format(self.pop_type, fname))
        return mdf

