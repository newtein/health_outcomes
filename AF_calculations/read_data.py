import pandas as pd
from copy import copy, deepcopy
import numpy as np

class ReadData:
    def __init__(self, pollutant, year='2020', observation_type="daily", filename=None, county_level=False,
                 county_identifier=None, measurement_type='no2'):
        """
        PM10 Ozone NO2 SO2 CO
        parameters = ["81102", "44201", "42602", "42401", "42101"]
        """
        self.measurement_type = measurement_type
        self.AMBIENT_AIR_DATA = "data/ambient_{}".format(measurement_type)
        self.year = year
        self.pollutant = pollutant
        self.observation_type = observation_type
        self.filename = filename
        self.county_level = county_level
        self.county_identifier = county_identifier
        self.pollutant_map = {
            "CO": "42101",
            "S02": "42401",
            "NO2": "42602",
            "O3": "44201",
            "PM10": "81102",
            "PM2.5": "88101",
            "WIND": "61103",
            "TEMP": "68105",
            "RH": "62201",
            "Pressue": "68108"
        }
        # {'Aqi': 'first','Method Code': 'first',  'First Max Hour': 'first',}
        self.agg_prototype = {
                             'Arithmetic Mean': 'first',
                             #'Cbsa Name': 'first',
                             #'Cbsa Code': 'first',
                             'City Name': 'first',
                             'County Name': 'first',
                             'County Code': 'first',
                             'Date of Last Change': 'first',
                             'Datum': 'first',
                             'Event Type': 'first',

                             '1st Max Value': 'first',
                             'Latitude': 'first',
                             'Local Site Name': 'first',
                             'Longitude': 'first',

                             'Observation Count': 'first',
                             'Observation Percent': 'first',
                             'Parameter Code': 'first',
                             'POC': 'first',
                             'Pollutant Standard': 'first',
                             'Site Num': 'first',
                             'State Name': 'first',
                             'State Code': 'first',
                             'Units of Measure': 'first',
        }
        # self.agg_prototype = {i.lower().replace(" ", "_"): j for i, j in self.agg_prototype.items()}

    def get_file_name(self):
        pollutant_code = self.pollutant_map.get(self.pollutant, self.pollutant)
        fname = "{}_{}_{}".format(self.observation_type, pollutant_code, self.year)
        if self.county_identifier:
            fname = "{}_{}".format(fname, self.county_identifier)
        return "{}/{}.csv".format(self.AMBIENT_AIR_DATA, fname)

    def create_id(self, x):
        if self.county_level:
            _id = "{}_{}".format(x['State Code'], x['County Code'])
            return _id
        _id = "{}_{}_{}".format(x['State Code'], x['County Code'], x['Site Num'])
        return _id


    def get_county_fips(self, x):
        x = str(x)
        if len(x) == 1:
            return "00{}".format(x)
        elif len(x) == 2:
            return "0{}".format(x)
        else:
            return x

    def get_fips(self, df):
        df['fips'] = df['State Code'].astype(str) + df['County Code'].apply(self.get_county_fips)

        return df

    def percentile(self, n):
        def percentile_(x):
            return np.percentile(x, n)

        percentile_.__name__ = 'percentile_%s' % n
        return percentile_

    def get_pandas_obj(self):
        """
        "State Code","County Code","Site Num"
        """
        filename = self.filename if self.filename else self.get_file_name()
        str_cols = ['State Code', 'County Code', 'Site Num']
        str_dict = {i: str for i in str_cols}
        try:
            df = pd.read_csv(filename, dtype=str_dict)
            df['id'] = df.apply(self.create_id, axis=1)
            sample_duration = ['24-HR BLK AVG', '24 HOUR']
            # df = df[df['Sample Duration'].isin(sample_duration)]
            if self.observation_type == 'daily':
                df['Date Local'] = pd.to_datetime(df['Date Local'], format='%Y-%m-%d')
                self.agg_prototype.update({'1st Max Value': self.percentile(90), 'Arithmetic Mean': self.percentile(90), 'AQI': 'max'})
                df = df.groupby(['id']).agg(self.agg_prototype).reset_index()
                # df = df.sort_values(by='Date Local')
            elif self.observation_type == 'annual':
                self.agg_prototype.update({'1st Max Value': 'max', 'Arithmetic Mean': 'max', 'State Code': 'first'})
                df = df.groupby(['id', 'Year']).agg(self.agg_prototype).reset_index()
                # df = df.sort_values(by='Year')
            df = self.get_fips(df)
            # self.agg_prototype.pop('Poc')
            # df = df[df['Sample Duration']=='24-HR BLK AVG']
        except Exception as e:
            print("File empty", e)
            df = pd.DataFrame()
        return df


if __name__ == "__main__":


    obj = ReadData('PM2.5', year='2019', county_level=True, measurement_type='pm2.5')
    print (obj.get_pandas_obj().head(2))
