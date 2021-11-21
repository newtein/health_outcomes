from prepare_data_for_modeling_or import ModelingData
from prepare_data_for_modeling_child_or import ModelingDataChild
import statsmodels.api as sm
import numpy as np
from constants import *
from sklearn.metrics import accuracy_score


class OddsRatio:
    def __init__(self, pop_type='ADULT'):
        self.pop_type = pop_type
        if self.pop_type == 'ADULT':
            self.data_obj = ModelingData()
        else:
            self.data_obj = ModelingDataChild()
        mdf = self.data_obj.get_data_with_epa_region()
        self.results = {}
        mdf = mdf[~mdf['_STATE'].isin(EXCLUDE_STATES)]
        self.df_carb = mdf[mdf['_STATE'].isin(CARB)]
        self.df_noncarb = mdf[~mdf['_STATE'].isin(CARB)]
        self.carb_regions = self.df_carb['EPA Region'].unique().tolist()
        self.noncarb_regions = self.df_noncarb['EPA Region'].unique().tolist()
        print(self.carb_regions)
        print(self.noncarb_regions)
        print(self.df_noncarb[self.df_noncarb['EPA Region'] == 2]['_STATE'].unique())
        self.mdf = mdf

    def process(self, mdf):
        if self.pop_type == 'ADULT':
            sc = MODELING_COLUMNS
        else:
            sc = MODELING_COLUMNS_FOR_CHILD
        mdf = mdf[sc]
        mdf = mdf.dropna()
        return mdf

    def get_results(self):
        odds_ratio = {}
        accuracy_dict = {}
        for index, epa_region in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
            if epa_region == 0 or (epa_region in self.carb_regions and epa_region in self.noncarb_regions):
                if epa_region == 0:
                    tdf = self.mdf
                else:
                    tdf = self.mdf[self.mdf['EPA Region'] == epa_region]
                tdf = self.process(tdf)
                # X = tdf.drop(['ASTHMA', 'POPEST2017_CIV'], axis=1)
                X = tdf.drop(['ASTHMA'], axis=1)
                y = tdf['ASTHMA']
                # print(epa_region)
                X = X.astype(float)
                result_df, accuracy = self.fit_logistic(X, y)
                accuracy_dict[epa_region] = accuracy
                fw = "{}/{}.csv".format(DATA_ODDS_RATIO_MODULE, "EPA Region {} Odds Ratio {}".format(epa_region, self.pop_type))
                odds_ratio[epa_region] = result_df
                result_df.to_csv(fw)
                print("Written file {}".format(fw))
                # print("EPA Region {}".format(epa_region))
        # obj = plt_error_bar(odds_ratio)
        # obj.execute()
        return odds_ratio, accuracy_dict

    def fit_logistic(self, X, y):
        res = sm.Logit(y, X).fit()
        params = res.params
        conf = res.conf_int()
        conf['Odds Ratio'] = params
        conf.columns = ['5%', '95%', 'Odds Ratio']
        y_pred = res.predict(X).apply(lambda x: 0 if x<0.5 else 1).tolist()
        accuracy = accuracy_score(y, y_pred)
        return np.exp(conf), accuracy

if __name__ == "__main__":
    obj = OddsRatio(pop_type='CHILD')
    obj.get_results()