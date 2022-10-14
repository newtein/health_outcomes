from AF_calculations.read_county_population import ReadCountyCensus
from AF_calculations.read_lur_no2 import ReadLUR
import os
import pandas as pd


class MergeExAndPop:
    def __init__(self, measurement_type='no2'):
        self.measurement_type = measurement_type
        fw = "data/lur_no2/lur_{}_merged_with_pop_v5.csv".format(self.measurement_type)
        if os.path.exists(fw):
            self.df = pd.read_csv(fw)
        else:
            self.lur_df = ReadLUR(measurement_type=self.measurement_type).get_df()
            self.pop_df = ReadCountyCensus().get_df()
            self.lur_df['fips'] = self.lur_df['fips'].astype(str)
            # print(self.pop_df.shape)
            self.df = self.pop_df.merge(self.lur_df, on=['fips', 'year'], how='left')
            self.df.to_csv(fw, index=False)

    def get_df(self, year=None):
        if year:
            return self.df[self.df['year'] == year]
        else:
            return self.df


if __name__ == "__main__":
    obj = MergeExAndPop()
    print(obj.get_df(2011))
