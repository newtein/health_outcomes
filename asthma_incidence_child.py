from read_brfss_file import ReadBRFSS
from read_acbs import ReadACBS
from config import CONFIG
import pandas as pd


class AsthmaIncidenceRateChild:
    def __init__(self, year):
        self.years = CONFIG.get("analysis_years")
        self.brfss, self.acbs = pd.DataFrame(), pd.DataFrame()
        for year in self.years:
            self.brfss = self.brfss.append(ReadBRFSS(year).get_df())
            self.acbs = self.acbs.append(ReadACBS(year).get_df())
        self.brfss = self.brfss.reset_index()
        self.acbs = self.acbs.reset_index()

    def get_never_asthma(self):
        lifetime_asthma_ques = self.brfss.groupby(['_STATE', 'CASTHDX2'])['CASTHDX2'].agg(['count']).reset_index()
        never_asthma = lifetime_asthma_ques["CASTHDX2"] == 2.0
        never_asthma_df = lifetime_asthma_ques[never_asthma]
        return never_asthma_df[["_STATE", "count"]]

    def get_numerator(self):
        valid_age = (self.acbs['AGEDX'] != 777)
        last_12_months = self.acbs['INCIDNT'] == 1
        df2_valid_age = self.acbs[valid_age]
        incidence_by_state = df2_valid_age[last_12_months].groupby(['_state'])['_state'].agg(['count']).reset_index()
        incidence_by_state['num'] = incidence_by_state['count']
        return incidence_by_state[['_state', 'num']]

    def calculate_incidence(self, x):
        return (x['num'] * 1000) / (x['num']+x['count'])

    def incidence_for_usa(self):
        valid_age = (self.acbs['AGEDX'] != 777)
        last_12_months = self.acbs['INCIDNT'] == 1
        df2_valid_age = self.acbs[valid_age]
        incidence = df2_valid_age[last_12_months]['seqno'].agg(['count']).reset_index()['seqno'].tolist()[0]
        print(incidence)
        lifetime_asthma_ques = self.brfss.groupby(['CASTHDX2'])['CASTHDX2'].agg(['count']).reset_index()
        never_asthma = lifetime_asthma_ques["CASTHDX2"] == 2.0
        never_asthma = lifetime_asthma_ques[never_asthma]['count'].tolist()[0]
        print(never_asthma)
        return (incidence*1000)/(incidence+never_asthma)

    def get_incidence_rate(self):
        never_asthma_df = self.get_never_asthma()
        numerator_df = self.get_numerator()
        numerator_df = numerator_df.merge(never_asthma_df, left_on=["_state"], right_on=["_STATE"])
        numerator_df['incidence_rate'] = numerator_df.apply(self.calculate_incidence, axis=1)
        return numerator_df, self.incidence_for_usa()


if __name__ == "__main__":
    obj = AsthmaIncidenceRateChild('2017')
    print(obj.get_incidence_rate())
