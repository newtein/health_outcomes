from asthma_prevalance import AsthmaPrevalence
from asthma_incidence import AsthmaIncidenceRate
from asthma_incidence_child import AsthmaIncidenceRateChild
from get_population_by_state import GetAgeSex
from constants import *
from config import CONFIG
import numpy as np
from get_trap_incidences import TRAPIncidences
import pandas as pd


class WrapperClass:
    def __init__(self, year, disease, pop_type="ADULT"):
        self.year = year
        self.disease = disease
        self.pop_type = pop_type
        self.prevalence_df, self.incidence_df = None, None
        self.global_incidence = None
        self.population_df = GetAgeSex(self.year).read_file_by_age()
        if self.pop_type == 'ADULT':
            self.population_df = self.population_df[self.population_df['CHILD']==0]
        else:
            self.population_df = self.population_df[self.population_df['CHILD'] == 1]
        self.get_disease_df()
        self.pop_col = 'POPEST{}_CIV'.format(self.year)
        # self.pop_col = 'pop'
        self.trap_data = TRAPIncidences(of=self.pop_type).read()
        # print(self.population_df.columns)
        # print(self.prevalence_df.columns)
        # print(self.incidence_df.columns)

    def get_disease_df(self):
        if self.disease == 'ASTHMA':
            self.prevalence_df = AsthmaPrevalence(self.year, pop_type=self.pop_type).get_df()
            if self.pop_type == 'ADULT':
                self.incidence_df, self.global_incidence = AsthmaIncidenceRate(self.year).get_incidence_rate()
            else:
                self.incidence_df, self.global_incidence = AsthmaIncidenceRateChild(self.year).get_incidence_rate()

    def get_global(self, type="GLOBAL"):
        """
        type: GLOBAL, GLOBAL_HIGH, GLOBAL_LOW
        :param type:
        :return:
        """
        return CONFIG.get(self.disease).get(self.year).get(self.pop_type).get(type)

    def calculate_prevalance_cases(self, x):
        if not np.isnan(x['Prevalence']):
            return (x[self.pop_col]*x['Prevalence'])/100
        else:
            return (x[self.pop_col]*self.get_global(type='GLOBAL'))/100

    def calculate_prevalance_cases_high(self, x):
        if not np.isnan(x['high_CI']):
            return (x[self.pop_col]*x['high_CI'])/100
        else:
            return (x[self.pop_col] * self.get_global(type='GLOBAL_HIGH')) / 100

    def calculate_prevalance_cases_low(self, x):
        if not np.isnan(x['low_CI']):
            return (x[self.pop_col]*x['low_CI'])/100
        else:
            return (x[self.pop_col] * self.get_global(type='GLOBAL_LOW')) / 100

    def calculate_at_risk(self, x):
        return x[self.pop_col] - x['prevalence_cases']

    def calculate_at_risk_high(self, x):
        return x[self.pop_col] - x['prevalence_cases_high']

    def calculate_at_risk_low(self, x):
        return x[self.pop_col] - x['prevalence_cases_low']

    def calculate_incidence_cases(self, x):
        return (x['at_risk']*x['incidence_rate'])/1000

    def calculate_incidence_cases_high(self, x):
        return (x['at_risk_high']*x['incidence_rate'])/1000

    def calculate_incidence_cases_low(self, x):
        return (x['at_risk_low']*x['incidence_rate'])/1000

    def calculate_trap_incidence_cases(self, x):
        # print(x['incidence_cases'], x['AF'])
        return (x['incidence_cases']*x['AF'])

    def calculate_trap_incidence_cases_high(self, x):
        return (x['incidence_cases_high']*x['AF'])

    def calculate_trap_incidence_cases_low(self, x):
        return (x['incidence_cases_low']*x['AF'])

    def align_population_col(self, x):
        if x['STATE'] == 0:
            print("total pop")
            print(x)
            return round(self.total_pop)
        elif pd.isna(x['pop']):
            return x[self.pop_col_yr]
        else:
            return round(x['pop'])

    def calculate_prevalence_and_incidence_cases(self):
        self.prevalence_count = self.population_df.merge(self.prevalence_df, left_on='STATE', right_on='State Code', how='left')
        self.incident_count = self.prevalence_count.merge(self.incidence_df, right_on='_state', left_on='STATE', how='left')
        # self.incident_count[self.pop_col] = self.incident_count.apply(self.align_population_col, axis=1)

        self.incident_count['prevalence_cases'] = self.incident_count.apply(self.calculate_prevalance_cases, axis = 1)
        self.incident_count['prevalence_cases_high'] = self.incident_count.apply(self.calculate_prevalance_cases_high, axis = 1)
        self.incident_count['prevalence_cases_low'] = self.incident_count.apply(self.calculate_prevalance_cases_low, axis = 1)

        self.incident_count['at_risk'] = self.incident_count.apply(self.calculate_at_risk, axis = 1)
        self.incident_count['at_risk_high'] = self.incident_count.apply(self.calculate_at_risk_high, axis = 1)
        self.incident_count['at_risk_low'] = self.incident_count.apply(self.calculate_at_risk_low, axis = 1)

        self.incident_count['incidence_rate'] = self.incident_count['incidence_rate'].fillna(self.global_incidence)
        self.incident_count['incidence_cases'] = self.incident_count.apply(self.calculate_incidence_cases, axis = 1)
        self.incident_count['incidence_cases_high'] = self.incident_count.apply(self.calculate_incidence_cases_high, axis = 1)
        self.incident_count['incidence_cases_low'] = self.incident_count.apply(self.calculate_incidence_cases_low, axis = 1)

        self.incident_count = self.incident_count.merge(self.trap_data, left_on='State Name', right_on='State', how='left')
        trap_global = CONFIG.get("TRAP_GLOBAL").get("value")
        self.incident_count['AF'] = self.incident_count['AF'].fillna(trap_global)
        self.incident_count['AF'] = self.incident_count['AF'].astype(float)
        self.incident_count.to_csv("temp.csv", index=False)
        self.incident_count['trap_incidence_cases'] = self.incident_count.apply(self.calculate_trap_incidence_cases, axis=1)
        self.incident_count['trap_incidence_cases_high'] = self.incident_count.apply(self.calculate_trap_incidence_cases_high,
                                                                                axis=1)
        self.incident_count['trap_incidence_cases_low'] = self.incident_count.apply(self.calculate_trap_incidence_cases_low,
                                                                               axis=1)

        self.incident_count.drop(['95% CI', '_state', '_STATE', 'State'], axis=1, inplace=True)

        fw = "{}/{}".format(OUTPUT_FILE, "{}_{}_{}.csv".format(self.disease, self.year, self.pop_type))
        print("Written: {}".format(fw))
        self.incident_count.to_csv(fw, index=False)


if __name__ == "__main__":
    obj = WrapperClass('2017', "ASTHMA", pop_type='ADULT')
    print(obj.calculate_prevalence_and_incidence_cases())

    # obj = WrapperClass('2017', "ASTHMA", pop_type='CHILD')
    # print(obj.calculate_prevalence_and_incidence_cases())