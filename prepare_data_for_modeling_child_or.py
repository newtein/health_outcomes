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
    def __init__(self, state_code=None, other_filters={}):
        self.state_code = state_code
        self.pop_type = 'CHILD'
        self.other_filters = other_filters
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

    def filter_state_based_on_census_region(self, df):
        acceptable_region = df.loc[df["State Code"]==self.state_code, "region_code"].values[0]
        zev_states_but_not_our_state = [i for i in ZEV_STATES if i != self.state_code]
        df = df[~df['_STATE'].isin(zev_states_but_not_our_state)]
        df = df[df['region_code'] == acceptable_region].reset_index()
        print("Unique States: {}", df['State Name'].unique())
        return df

    def merge_for_density(self, df, year):
        population__df = GetAgeSex(str(year), pop_type=self.pop_type).calculate_population_using_weight(df)
        population__df = population__df[population__df['_STATE'] != 0]
        print(population__df['DENSITY'].dtype)
        df = df.merge(population__df[['_STATE', 'DENSITY', 'surface_area', 'population']], left_on="_STATE",
                              right_on="_STATE", how="left")
        return df

    def filtering_nan_state(self, df):
        print("No States Found for: {}", df[pd.isna(df["_STATE"])]["_STATE"].unique())
        print(df[pd.isna(df["_STATE"])])
        df = df[~pd.isna(df["_STATE"])]
        return df

    def merge_for_epa_region(self, df):
        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name','State Code', "EPA Region"]]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        df = df.merge(epa_region, left_on="_STATE", right_on="State Code", how='left')
        return df

    def merge_for_census_code(self, df):
        census_regions_df = pd.DataFrame(columns=["state_name", "region_code"], data=REGION_DATA)
        df = df.merge(census_regions_df, left_on="State Name", right_on="state_name", how='left')
        return df

    def get_primary_exposure(self, df):
        if self.state_code:
            df['NONCARB'] = df['_STATE'].apply(self.if_state)
            # mdf = self.filter_state_based_on_census_region(mdf)
        else:
            df['NONCARB'] = df['_STATE'].apply(self.if_carb)
        return df

    def get_primary_risk_wrap(self, df):
        df = df[df['CASTHDX2'].isin([1, 2])]
        df['ASTHMA'] = df.apply(self.get_primary_risk, axis=1)
        df = df[df['ASTHMA'].isin([0,1])]
        return df

    def group_race(self, df):
        race_dict = {1.0:1, 2.0:2, 3.0: 3, 4.0: 4, 5.0:5, 6.0:5, 7.0:5, 8.0: 5, 77.0:77, 99.0:77}
        df['_CPRACE'] = df['_CPRACE'].replace(race_dict)
        return df

    def apply_msa_filter(self, df, msa_value):
        return df[df["MSCODE"]==msa_value]

    def apply_other_filters(self, df):
        print("Before MSCODE: {}".format(df.shape))
        msa_value = self.other_filters.get("MSCODE")
        if msa_value:
            df = self.filter_metropolitan(df)
            df = self.apply_msa_filter(df, msa_value)
            print("After MSCODE: {}".format(df.shape))
        return df

    def filter_metropolitan(self, df):
        # 1: urbanized
        # 2, 3, 4: urban
        # 5: rural
        urban_dict = {1:1, 2:2, 3:2, 4:2, 5:3}
        df['MSCODE'] = df['MSCODE'].fillna(77)
        df['MSCODE'] = df['MSCODE'].replace(urban_dict)
        return df

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
            dfs[i] = self.merge_for_density(dfs[i], year)
            dfs[i] = self.filtering_nan_state(dfs[i])
            dfs[i]['year'] = int(year)
            mdf = mdf.append(dfs[i])

        mdf = self.merge_for_epa_region(mdf)
        mdf = self.merge_for_census_code(mdf)
        mdf = self.get_primary_exposure(mdf)
        mdf = self.get_primary_risk_wrap(mdf)
        mdf = self.group_race(mdf)
        mdf = self.apply_other_filters(mdf)
        mdf = POVERTY(mdf).process()

        new_cols = ["State Name", "_STATE", 'EPA Region', '_CLLCPWT', 'year']

        mdf = mdf[MODELING_COLUMNS_FOR_CHILD+new_cols]
        mdf = AdjustWeightsForOR(mdf, self.pop_type).execute()
        print("aa", mdf['year'].unique())
        # not writing the file to save up space
        # mdf.to_csv(fname, index=False)
        print("File written {}: {}".format(self.pop_type, fname))
        return mdf

