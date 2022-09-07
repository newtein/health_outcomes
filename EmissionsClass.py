from SQLAlchemyCoreClass import CoreFunctions
import math
from get_population_by_state import GetAgeSex
import pandas as pd
import numpy as np
from constants import *
from cal_atmos_by_state import AtmospherebyState

class EmissionClass:
    """
    One-time run
    """
    def __init__(self):
        self.database = 'us_2008_2019_no2'
        self.movesouput_table = "movesoutput"
        self.core_obj = CoreFunctions(self.database, self.movesouput_table)
        # self.population_lookup = obj.get(county_name)

    def calculate_emission_by_pollutant_yearly(self, pollutant_id):
        # 33 No2
        pollutant_id = 33
        query = """SELECT stateID, yearID as year, emissionQuant as emission FROM `movesoutput` WHERE pollutantID={}"""
        query = query.format(pollutant_id)
        alias = ['stateID', 'year', 'emission']
        print(query)
        return alias, list(self.core_obj.execute_query(query, alias))

    def get_emission(self, pollutant_id):
        rs = self.calculate_emission_by_pollutant_yearly(pollutant_id)
        return rs

    def from_grams_to_ug_per_m3(self, row):
        "Using surface area * h = volume"
        emission = row['emission']
        surface_area = row['surface_area']
        num = emission * 10**6 # from grams to ugrams
        denum = surface_area * (10 **6) # from km2 to m2
        concentration = num/(denum*200)
        concentration_5 = num/(denum*150)
        concentration_95 = num/(denum*250)
        return concentration, concentration_5, concentration_95

    def from_grams_to_ug_per_m3_v2(self, row):
        """Using atmos volume"""
        emission = row['emission']
        emission_in_089_hour = emission # original unit is gs-1
        atmos_vol = row['atmos_vol']
        num = emission_in_089_hour  * (10**6) # from grams to ugrams
        denum = atmos_vol  # from km3
        concentration = 18.8 + (num/denum)
        concentration_5 = np.nan
        concentration_95 = np.nan
        return concentration, concentration_5, concentration_95

    def get_volume(self, state):
        atmos_vol_df = AtmospherebyState().get_df()
        return atmos_vol_df[atmos_vol_df["State"]]

    def calculate_AF(self, exposure_level):
        # CRF for NO2 Alotaibi et al 2019 Equation 3
        RR_unit = 4
        RR = 1.05
        power = (np.log(RR)/RR_unit)*exposure_level
        RRdiff = np.e ** power
        AF = 1 - (1/RRdiff)
        return AF

    def get_no2_exposure_dataframe(self):
        # 33 is polltant id for N02, taking 2015 arbitatry for surface area
        cols, data = self.get_emission(33)
        df = pd.DataFrame(columns=cols, data=data)
        atmos_vol_df = AtmospherebyState().get_df()
        # surface_df = us_pop_obj.get_surface_area_with_state_code()
        mdf = df.merge(atmos_vol_df, left_on = "stateID", right_on="State Code", how='left')


        mdf['concentration'], mdf['concentration_5'], mdf['concentration_95'] =\
            zip(*mdf.apply(self.from_grams_to_ug_per_m3_v2, axis=1))
        mdf['AF'] = mdf['concentration'].apply(self.calculate_AF)
        mdf['AF_5'] = mdf['concentration_5'].apply(self.calculate_AF)
        mdf['AF_95'] = mdf['concentration_95'].apply(self.calculate_AF)
        mdf.to_csv(TRAP_INCIDENCE_v2, index=False)
        return mdf

if __name__ == "__main__":
    obj = EmissionClass()
    print(obj.get_no2_exposure_dataframe())
    print()
