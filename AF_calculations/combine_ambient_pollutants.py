from AF_calculations.read_data import ReadData

import pandas as pd


class CombineAmbientPollutants:
    def __init__(self, syear=2010, eyear = 2019, measurement_type='no2'):
        self.syear = syear
        self.eyear = eyear
        self.measurement_type = measurement_type

    def get_df(self):
        df = pd.DataFrame()
        for year in range(self.syear, self.eyear+1):
            tdf = ReadData(self.measurement_type.upper(), year=str(year), county_level=True, measurement_type=self.measurement_type).get_pandas_obj()
            tdf['Year'] = year
            print(tdf.columns)
            print(year, tdf['State Code'].unique())
            df = df.append(tdf)
        df = df.sort_values(by='Year')
        df['pollutant'] = self.measurement_type
        return df


if __name__ == "__main__":
    obj = CombineAmbientPollutants()
    print (obj.get_df().head(2))