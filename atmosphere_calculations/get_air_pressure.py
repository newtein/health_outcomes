import pandas as pd


class AirPressureofStates:
    def __init__(self):
        # pressure from sea level
        # returns in pascal
        path = "data/ATMOS_VOL"
        fname = 'above_sea_level.csv'
        self.sea_level_df = pd.read_csv("{}/{}".format(path, fname))

    def pressure_at_height_h(self, h):
        # h in meters
        p_at_sea_level = 101325
        p_at_h = p_at_sea_level * (1 - 2.2557710 *(10**-5) * h)**5.25588
        return p_at_h

    def feet_to_meter(self, x):
        # x format is num feets
        x = int(x.replace("feet", "").strip().replace(",", ""))
        return x*0.3048

    def get_df(self):
        self.sea_level_df['Elevation'] = self.sea_level_df['Elevation'].apply(self.feet_to_meter)
        self.sea_level_df['air_pressure'] = self.sea_level_df['Elevation'].apply(self.pressure_at_height_h)
        return self.sea_level_df[['State', 'air_pressure']]


if __name__ == "__main__":
    obj = AirPressureofStates()
    print(obj.get_df())
