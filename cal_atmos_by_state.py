import pandas as pd
from atmosphere_calculations.get_rh import RHbyState
from atmosphere_calculations.get_temperature import TempbyState
from atmosphere_calculations.get_air_pressure import AirPressureofStates
from get_population_by_state import GetAgeSex
from atmospheric_volume_calculator import AtmosphericVolumeCalculator
from constants import ATMOS_BY_STATE
import os


class AtmospherebyState:
    def __init__(self):
        pass

    def met_df(self):
        rh_df = RHbyState().get_df()
        temp_df = TempbyState().get_df()
        pres_df = AirPressureofStates().get_df()
        surface_df = GetAgeSex('2015', pop_type='CHILD').get_surface_area_with_state_code()
        met_df = surface_df.merge(rh_df, left_on='State Name', right_on='State', how='left')
        met_df = met_df.merge(temp_df, left_on='State Name', right_on='State', how='left')
        met_df = met_df.merge(pres_df, left_on='State Name', right_on='State', how='left')
        met_df = met_df[['State Code', 'State Name', 'RH', 'temp', 'air_pressure', 'surface_area']]
        # surface area in m3
        met_df['surface_area'] = met_df['surface_area'] * (10**6)
        return met_df

    def cal_vol(self, x):
        return AtmosphericVolumeCalculator(x['surface_area'], x['air_pressure'], x['temp'], x['RH']).get_volume()

    def get_df(self):
        if not os.path.exists(ATMOS_BY_STATE):
            met_df =  self.met_df()
            met_df['atmos_vol'] = met_df.apply(self.cal_vol, axis=1)
        else:
            met_df = pd.read_csv(ATMOS_BY_STATE)
        return met_df

if __name__ == "__main__":
    obj = AtmospherebyState()
    print(obj.get_df())