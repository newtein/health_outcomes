from read_brfss_file import ReadBRFSS
from read_acbs import ReadACBS
from config import CONFIG
import pandas as pd
from copy import copy


class AsthmaIncidenceRate:
    def __init__(self, year):
        # self.year = year
        self.years = CONFIG.get("analysis_years")
        self.brfss, self.acbs = pd.DataFrame(), pd.DataFrame()
        # for year in self.years:
        for year in [year]:
            self.brfss = self.brfss.append(ReadBRFSS(year).get_df())
            self.acbs = self.acbs.append(ReadACBS(year).get_df())
        self.brfss = self.brfss.reset_index()
        # self.original_brfss = copy(self.brfss)
        # self.brfss = self.brfss[self.brfss['SMOKE100'] == 2]
        self.acbs = self.acbs.reset_index()

    def get_never_asthma(self):
        # lifetime_asthma_ques = self.brfss.groupby(['_STATE', 'ASTHMA3'])['ASTHMA3'].agg(['count']).reset_index()
        # never_asthma = lifetime_asthma_ques["ASTHMA3"] == 2.0
        # never_asthma_df = lifetime_asthma_ques[never_asthma]
        never_asthma_f = self.brfss["ASTHMA3"] == 2.0
        never_asthma_df = self.brfss[never_asthma_f]
        never_asthma_df = never_asthma_df.groupby(['_STATE'])['_LLCPWT2'].sum().reset_index()
        never_asthma_df['count'] = never_asthma_df['_LLCPWT2']
        return never_asthma_df[["_STATE", "count"]]

    # def total_population_by_state(self):
    #     known_asthma = (self.original_brfss["ASTHMA3"] == 2.0) | (self.original_brfss["ASTHMA3"] == 1.0)
    #     known_asthma_df = self.original_brfss[known_asthma]
    #     known_asthma_df = known_asthma_df.groupby(['_STATE'])['_LLCPWT2'].sum().reset_index()
    #     known_asthma_df['pop'] = known_asthma_df['_LLCPWT2']
    #     return known_asthma_df[["_STATE", "pop"]]

    def get_numerator(self):
        valid_age = (self.acbs['AGEDX'] != 777) | (self.acbs['AGEDX'] != 999)
        last_12_months = self.acbs['INCIDNT'] == 1
        df2_valid_age = self.acbs[valid_age]
        # incidence_by_state = df2_valid_age[last_12_months].groupby(['_state'])['_state'].agg(['count']).reset_index()
        incidence_by_state = df2_valid_age[last_12_months].groupby(['_state'])['LLCPWT_F'].sum().reset_index()

        incidence_by_state['num'] = incidence_by_state['LLCPWT_F']
        return incidence_by_state[['_state', 'num']]

    def calculate_incidence(self, x):
        return (x['num'] * 1000) / (x['num']+x['count'])

    def incidence_for_usa(self):
        valid_age = (self.acbs['AGEDX'] != 777) | (self.acbs['AGEDX'] != 999)
        last_12_months = self.acbs['INCIDNT'] == 1
        df2_valid_age = self.acbs[valid_age]
        # incidence = df2_valid_age[last_12_months]['seqno'].agg(['count']).reset_index()['seqno'].tolist()[0]
        # LLCPWT_F is weighted column for adults
        incidence = df2_valid_age[last_12_months]['LLCPWT_F'].sum()
        print(incidence)
        # lifetime_asthma_ques = self.brfss.groupby(['ASTHMA3'])['ASTHMA3'].agg(['count']).reset_index()
        # never_asthma = lifetime_asthma_ques["ASTHMA3"] == 2.0
        # never_asthma = lifetime_asthma_ques[never_asthma]['count'].tolist()[0]
        never_asthma_f = self.brfss["ASTHMA3"] == 2.0
        never_asthma = self.brfss[never_asthma_f]['_LLCPWT2'].sum()
        print(never_asthma)
        return (incidence*1000)/(incidence+never_asthma)

    # def total_population(self):
    #     known_asthma = (self.original_brfss["ASTHMA3"] == 2.0) | (self.original_brfss["ASTHMA3"] == 1.0)
    #     total_pop = self.original_brfss[known_asthma]['_LLCPWT2'].sum()
    #     return total_pop

    def get_incidence_rate(self):
        never_asthma_df = self.get_never_asthma()
        numerator_df = self.get_numerator()
        print(never_asthma_df.columns)
        numerator_df = numerator_df.merge(never_asthma_df, left_on=["_state"], right_on=["_STATE"])
        # total_pop_df = self.total_population_by_state()
        # numerator_df = numerator_df.merge(total_pop_df, left_on=["_state"], right_on=["_STATE"])
        numerator_df['incidence_rate'] = numerator_df.apply(self.calculate_incidence, axis=1)
        return numerator_df, self.incidence_for_usa()


if __name__ == "__main__":
    obj = AsthmaIncidenceRate('2017')
    print(obj.get_incidence_rate())
