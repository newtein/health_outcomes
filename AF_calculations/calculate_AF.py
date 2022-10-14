from AF_calculations.merge_no2_exposure_with_population import MergeExAndPop
import pandas as pd
import numpy as np
from config import CONFIG
from constants import *


class calculateAF:
    def __init__(self, pr_ir_df, national_avg_row, year, measurement_type='no2'):
        # years = CONFIG.get("analysis_years")
        # years_str = "_".join([str(i) for i in years])
        self.pr_ir_df = pr_ir_df
        self.national_avg_row = national_avg_row
        self.year = year
        self.measurement_type = measurement_type
        years = CONFIG.get("analysis_years")
        years_str = "_".join([str(i) for i in years])
        self.fw = DATA_ODDS_RATIO_MODULE + "/{}/PR_IR_AF_{}.csv".format(years_str, self.measurement_type)

    def calculate_AF(self, exposure_level):
        # CRF for NO2 Alotaibi et al 2019 Equation 3
        # NO2 was 1.05 (95% CI = 1.02–1.07) per 4 μg/m3,
        # for PM2.5 it was 1.03 (95% CI = 1.01–1.05) per 1 μg/m3,
        # and for PM10 it was 1.05 (95% CI = 1.02–1.08) per 2 μg/m3.
        if self.measurement_type == 'no2':
            RR_unit = 4
            RR = 1.05
        elif self.measurement_type == 'pm2.5':
            RR_unit = 1
            RR = 1.03
        elif self.measurement_type == 'pm10':
            RR_unit = 2
            RR = 1.05
        power = (np.log(RR)/RR_unit)*exposure_level
        RRdiff = np.e ** power
        AF = 1 - (1/RRdiff)
        return AF

    def cal_statewise_AF(self, df):
        columns = ['state_code', 'population', 'PR', 'at_risk','incidence_cases', 'AC', 'IR']
        agg_dict = {'population': 'sum',
                    'PR': 'first',
                    'at_risk': 'sum',
                    'incidence_cases': 'sum',
                    'AC': 'sum',
                    'IR': 'first'}
        sdf = df[columns].groupby('state_code').agg(agg_dict).reset_index()
        sdf['SAF'] = sdf['AC']/sdf['incidence_cases']
        return sdf

    def get_df(self):
        pop_df = MergeExAndPop(measurement_type=self.measurement_type).get_df(year=self.year)
        national_pr, national_ir = self.national_avg_row["PR"].item(), self.national_avg_row["IR"].item()
        pop_df['state_code'] = pop_df['state_code'].astype(float)
        df = pop_df.merge(self.pr_ir_df[['_STATE', 'PR', 'IR']], left_on='state_code', right_on='_STATE', how='left')
        df["PR"] = df["PR"].fillna(national_pr)
        df["IR"] = df["IR"].fillna(national_ir)
        df['at_risk'] = df['population'] - (df['population'] * df['PR'])
        df['incidence_cases'] = df['at_risk'] * df['IR']
        df['AF'] = df['pred_wght'].apply(self.calculate_AF)
        df['AC'] = df['incidence_cases'] * df['AF']
        sdf = self.cal_statewise_AF(df)
        sdf = sdf.dropna()
        sdf.to_csv(self.fw, index=False)
        return sdf

if __name__ == "__main__":
    obj = calculateAF()
    print(obj.cal_inc_cases())

