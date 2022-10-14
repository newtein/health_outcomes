import pandas as pd
import matplotlib.pyplot as plt
from AF_calculations.combine_ambient_pollutants import CombineAmbientPollutants

class ReadLUR:
    def __init__(self, measurement_type='no2'):
        self.measurement_type = measurement_type
        path = "data/lur_{}".format(self.measurement_type)
        if self.measurement_type == 'no2':
            fname = "uwc16625203218040380eebdf79369d5d84edb6dba8eb6c1.csv"
        elif self.measurement_type == 'pm2.5':
            fname = "uwc16655418522749ef06de59472e48e6baf3639c9357f3f.csv"
        elif self.measurement_type == 'pm10':
            fname = "uwc1665541873940ce44ad12f5277708a508efa24d534775.csv"
        self.df = pd.read_csv("{}/{}".format(path, fname))

    def ppb_to_umgm3(self,x):
        """Unit is ppb: https://www.caces.us/_files/ugd/342c07_ebb72126333c4fd7859e1702f288bafb.pdf
        Conversion unit: 1.88 (WHO, 2005; Alotaibi et al., 2019"""
        return x*1.88

    def join_with_ambient_data(self, df):
        columns = ['fips', 'Year', 'Arithmetic Mean']
        replace_col_names = {'Year': 'year', 'Arithmetic Mean':'pred_wght'}
        ambient_df = CombineAmbientPollutants(syear = 2010, eyear = 2019, measurement_type=self.measurement_type).get_df()
        ambient_df = ambient_df[columns]
        ambient_df = ambient_df.rename(columns=replace_col_names)
        ambient_df['fips'] = ambient_df['fips'].astype(int)
        ambient_df['year'] = ambient_df['year'].astype(int)
        df = df.merge(ambient_df, how='outer', on=['fips', 'year'])
        return df

    def get_one_col(self, x):
        if not pd.isna(x['pred_wght_x']) and not pd.isna(x['pred_wght_y']):
            return max(x['pred_wght_x'], x['pred_wght_y'])
        elif not pd.isna(x['pred_wght_x']):
            return x['pred_wght_x']
        else:
            return x['pred_wght_y']

    def get_df(self):
        # self.df.boxplot(column=['pred_wght'], by='state_abbr')
        # plt.savefig("temp.png")
        # plt.show()
        self.df = self.join_with_ambient_data(self.df)
        self.df['pred_wght'] = self.df.apply(self.get_one_col, axis = 1)
        if self.measurement_type == 'no2':
            self.df['pred_wght'] = self.df['pred_wght'].apply(self.ppb_to_umgm3)
        return self.df


if __name__ == "__main__":
    obj = ReadLUR()
    print(obj.get_df())
