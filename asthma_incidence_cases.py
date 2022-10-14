from read_acbs import ReadACBS
from config import CONFIG
import pandas as pd
from constants import *
import os


class AsthmaIncidenceCases:
    def __init__(self, years, pop_type='CHILD'):
        """
        TODO: Make for adults
        """
        self.pop_type = pop_type
        self.years = years
        self.df = pd.DataFrame()
        self.year_id = "_".join([str(i) for i in self.years])
        for year in self.years:
            try:
                tdf = ReadACBS(year, of='CHILD').get_df()
            except:
                tdf = pd.DataFrame()
            tdf['year'] = year
            self.df = self.df.append(tdf)
        self.resale_weights('CLLCPWT_F')

    def get_cases(self):
        fw = "{}/{}/incidence_num_from_acbs.csv".format(DATA_ODDS_RATIO_MODULE, self.year_id)
        if not os.path.exists(fw):
            last_12_months = self.df['INCIDNT'] == 1
            self.df = self.df[last_12_months].groupby(['_STATE'])['CLLCPWT_F'].sum().reset_index()
            self.df['num'] = self.df['CLLCPWT_F']
        else:
            self.df = pd.read_csv(fw)
        return self.df

    def resale_weights(self, weight_col):
        state_weight_df = self.df.groupby(['_STATE'])['year'].apply(set).apply(len).reset_index()
        state_weight_df['SWEIGHT'] = state_weight_df['year']
        self.df = self.df.merge(state_weight_df[['_STATE', 'SWEIGHT']], on='_STATE', how='left')
        self.df[weight_col] = self.df[weight_col] / self.df['SWEIGHT']


if __name__ == "__main__":
    obj = AsthmaIncidenceCases(["2008", "2009", "2010"])
    print(obj.get_cases())


