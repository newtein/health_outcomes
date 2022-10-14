import os.path
import pandas as pd
from asthma_incidence_cases import AsthmaIncidenceCases
from constants import *
from config import CONFIG


class PRIR:
    def __init__(self, pop_type):
        self.pop_type = pop_type
        self.refresh = 1
        years = CONFIG.get("analysis_years")
        years_str = "_".join([str(i) for i in years])
        self.fw = DATA_ODDS_RATIO_MODULE + "/{}/PR_IR.csv".format(years_str)

    def get_epa_region_df(self):
        epa_region = pd.read_csv("data/states_and_counties.csv")
        epa_region = epa_region[['State Name', 'State Code']]
        epa_region = epa_region[epa_region['State Code'] != 'CC']
        epa_region['State Code'] = epa_region['State Code'].apply(int)
        epa_region = epa_region.drop_duplicates(['State Code'], keep='first')
        return epa_region

    def calculate_global_pr(self, df, ever_asthma, weight_col):
        return df[ever_asthma][weight_col].sum()/df[weight_col].sum()

    def calculate_PR_IR(self, df, weight_col):
        ## Calculating PR
        ever_asthma = (df['ASTHMA'] == 1)
        total_burden_df = df[ever_asthma].groupby(['_STATE'])[weight_col].sum().reset_index()
        total_burden_df['total_asthma_burden'] = total_burden_df[weight_col]

        total_pop_df = df.groupby(['_STATE'])[weight_col].sum().reset_index()
        total_pop_df['total_pop'] = total_pop_df[weight_col]

        prevelence_df = total_pop_df[['_STATE', 'total_pop']].merge(total_burden_df[['_STATE', 'total_asthma_burden']], how='left', on='_STATE')
        prevelence_df['PR'] = prevelence_df['total_asthma_burden']/prevelence_df['total_pop']
        us_average_pr = self.calculate_global_pr(df, ever_asthma, weight_col)
        ## At risk
        prevelence_df['at_risk'] = prevelence_df['total_pop'] - prevelence_df['total_asthma_burden']
        ## Calculating IR
        years = CONFIG.get("analysis_years")
        inc_years = years
        if len(years) == 1:
            inc_years = [years[0]-1, years[0], years[0]+1]
        incidence_df = AsthmaIncidenceCases(inc_years, pop_type=self.pop_type).get_cases()
        mdf = prevelence_df.merge(incidence_df[['_STATE', 'num']], on='_STATE', how='left')
        exp_df = mdf.dropna()
        national_incidence = exp_df['num'].sum()/exp_df['at_risk'].sum()
        mdf['IR'] = mdf['num']/mdf['at_risk']
        mdf['IR'] = mdf['IR'].fillna(national_incidence)
        mdf.to_csv(self.fw)
        # df = df.merge(mdf, how='left', on='_STATE')
        national_avg_row = {"_STATE": 0, "PR": us_average_pr, "IR": national_incidence}
        return mdf, national_avg_row

    def get_df(self, df, weight_col):
        if os.path.exists(self.fw) and not self.refresh:
            df = pd.read_csv(self.fw)
            national_average_row = df[df['_STATE'] == 0]
            return df[df['_STATE'] != 0], national_average_row
        else:
            df, national_average_row = self.calculate_PR_IR(df, weight_col)
            return df, national_average_row


