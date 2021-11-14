from asthma_prevalance import AsthmaPrevalence
from asthma_incidence import AsthmaIncidenceRate
from asthma_incidence_child import AsthmaIncidenceRateChild
from get_population_by_state import GetAgeSex
from constants import *
from config import CONFIG
import numpy as np


class WrapperClass:
    def __init__(self, year, disease, pop_type="ADULT"):
        self.year = year
        self.disease = disease
        self.pop_type = pop_type
        self.prevalence_df, self.incidence_df = None, None
        self.global_incidence = None
        self.population_df = GetAgeSex(self.year).read_file_by_age()
        self.get_disease_df()
        print(self.population_df.columns)
        print(self.prevalence_df.columns)
        print(self.incidence_df.columns)

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
            return (x['POPEST2017_CIV']*x['Prevalence'])/1000
        else:
            return (x['POPEST2017_CIV']*self.get_global(type='GLOBAL'))/1000

    def calculate_prevalance_cases_high(self, x):
        if not np.isnan(x['high_CI']):
            return (x['POPEST2017_CIV']*x['high_CI'])/1000
        else:
            return (x['POPEST2017_CIV'] * self.get_global(type='GLOBAL_HIGH')) / 1000

    def calculate_prevalance_cases_low(self, x):
        if not np.isnan(x['low_CI']):
            return (x['POPEST2017_CIV']*x['low_CI'])/1000
        else:
            return (x['POPEST2017_CIV'] * self.get_global(type='GLOBAL_LOW')) / 1000

    def calculate_at_risk(self, x):
        return x['POPEST2017_CIV'] - x['prevalence_cases']

    def calculate_at_risk_high(self, x):
        return x['POPEST2017_CIV'] - x['prevalence_cases_high']

    def calculate_at_risk_low(self, x):
        return x['POPEST2017_CIV'] - x['prevalence_cases_low']

    def calculate_incidence_cases(self, x):
        return (x['at_risk']*x['incidence_rate'])/1000

    def calculate_incidence_cases_high(self, x):
        return (x['at_risk_high']*x['incidence_rate'])/1000

    def calculate_incidence_cases_low(self, x):
        return (x['at_risk_low']*x['incidence_rate'])/1000

    def calculate_prevalence_and_incidence_cases(self):
        self.prevalence_count = self.population_df.merge(self.prevalence_df, left_on='STATE', right_on='State Code', how='left')

        self.prevalence_count['prevalence_cases'] = self.prevalence_count.apply(self.calculate_prevalance_cases, axis = 1)
        self.prevalence_count['prevalence_cases_high'] = self.prevalence_count.apply(self.calculate_prevalance_cases_high, axis = 1)
        self.prevalence_count['prevalence_cases_low'] = self.prevalence_count.apply(self.calculate_prevalance_cases_low, axis = 1)

        self.prevalence_count['at_risk'] = self.prevalence_count.apply(self.calculate_at_risk, axis = 1)
        self.prevalence_count['at_risk_high'] = self.prevalence_count.apply(self.calculate_at_risk_high, axis = 1)
        self.prevalence_count['at_risk_low'] = self.prevalence_count.apply(self.calculate_at_risk_low, axis = 1)

        self.incident_count = self.prevalence_count.merge(self.incidence_df, right_on='_state', left_on='STATE', how='left')
        self.incident_count['incidence_rate'] = self.incident_count['incidence_rate'].fillna(self.global_incidence)
        self.incident_count['incidence_cases'] = self.incident_count.apply(self.calculate_incidence_cases, axis = 1)
        self.incident_count['incidence_cases_high'] = self.incident_count.apply(self.calculate_incidence_cases_high, axis = 1)
        self.incident_count['incidence_cases_low'] = self.incident_count.apply(self.calculate_incidence_cases_low, axis = 1)

        self.incident_count.drop(['95% CI', '_state', '_STATE'], axis=1, inplace=True)

        fw = "{}/{}".format(OUTPUT_FILE, "{}_{}_{}.csv".format(self.disease, self.year, self.pop_type))
        self.incident_count.to_csv(fw, index=False)


if __name__ == "__main__":
    obj = WrapperClass('2017', "ASTHMA", pop_type='ADULT')
    print(obj.calculate_prevalence_and_incidence_cases())