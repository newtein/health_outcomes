import os
import pandas as pd


class ReadCountyCensus:
    def __init__(self):
        """
        https://www.census.gov/data/tables/time-series/demo/popest/2010s-counties-detail.html
        """
        self.path = "data/CENSUS/state_data"
        self.fname = "cc-est2019-agesex-{}.csv"
        self.children_columns = ['UNDER5_TOT', 'AGE513_TOT', 'AGE1417_TOT']
        self.year_dict = {i:j for i, j in zip(range(3, 13), range(2010, 2020))}

    def get_epa_region_df(self):
        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name', 'State Code']]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        return epa_region

    def get_children_pop(self, df):
        df['population'] = df['UNDER5_TOT'] + df['AGE513_TOT'] + df['AGE1417_TOT']
        return df

    def get_county_fips(self, x):
        x = str(x)
        if len(x) == 1:
            return "00{}".format(x)
        elif len(x) == 2:
            return "0{}".format(x)
        else:
            return x

    def get_fips(self, df):
        df['county_fips'] = df['COUNTY'].apply(self.get_county_fips)
        df['STATE'] = df['STATE'].astype(str)
        df['fips'] = df['STATE'] + df['county_fips']
        return df

    def cal_cols(self, df):
        df = self.get_children_pop(df)
        df = self.get_fips(df)
        df['year'] = df['YEAR'].replace(self.year_dict)
        df = df[~df['year'].isin([1,2])]
        df = df[['fips', 'state_code', 'year', 'population']]
        return df

    def get_df(self):
        epa_region_df = self.get_epa_region_df()
        df = pd.DataFrame()
        for state_code in epa_region_df['State Code'].tolist():
            sc_file_id = "0{}".format(state_code) if len(str(state_code)) == 1 else state_code
            fname = "{}/{}".format(self.path, self.fname.format(sc_file_id))
            if os.path.exists(fname):
                print(fname)
                tdf = pd.read_csv(fname, engine='python',encoding='latin1')
                tdf['state_code'] = state_code
                tdf = self.cal_cols(tdf)
                df = df.append(tdf)
        # print(df[(df['state_code']==6) & (df['year'] == 2019)]['population'].sum())
        return df

if __name__ == "__main__":
    obj = ReadCountyCensus()
    print(obj.get_df())
